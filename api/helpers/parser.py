import json
import logging
from copy import deepcopy

import requests

from api.models import Game
from api.resources.names import NAME_FROM_NAME_ID, NAME_FROM_CARD_ID


logger = logging.getLogger(__name__)


class ParserException(Exception):
    pass


class MtgaLogParser:
    _image_cache = {}

    def __init__(self, log_path):

        with open(log_path, 'r') as f:
            self.log_lines = f.readlines()

        self.current_game_index = 0

    def fetch_infos(self):
        game = None
        current_player_id = None

        i = 0
        try:
            while i < len(self.log_lines):
                line = self.log_lines[i]

                # Login, to identify current player
                if 'AuthenticateResponse' in line:
                    i += 1
                    payload = json.loads(self.log_lines[i])
                    current_player_id = payload['authenticateResponse']['clientId']

                # Game initialization
                if 'Event.MatchCreated' in line:
                    logger.info('Game Start')
                    game = Game()
                    self.current_game_index += 1

                # Get players info
                if 'MatchGameRoomStateChangedEvent' in line:
                    i += 1
                    payload = json.loads(self.log_lines[i])
                    game_room = payload['matchGameRoomStateChangedEvent']['gameRoomInfo']

                    if game_room.get('stateType') == 'MatchGameRoomStateType_Playing':
                        players = game_room['gameRoomConfig']['reservedPlayers']
                        if players[0]['userId'] == current_player_id:
                            game.player, game.opponent = players
                        else:
                            game.opponent, game.player = players

                    if game_room.get('stateType') == 'MatchGameRoomStateType_MatchCompleted':
                        game.save()
                        game = None
                        logger.info('Game End')

                # Any game event
                if 'GreToClientEvent' in line:
                    i += 1
                    if self.log_lines[i].strip() == "[Message summarized because one or more GameStateMessages exceeded the 50 GameObject or 50 Annotation limit.]":
                        logger.warning(f"Missing game state details: Game {self.current_game_index}, line {self.log_lines[i]}")
                        # TODO: Add game state anyway, with indication that details are missing
                        continue

                    payload = json.loads(self.log_lines[i])

                    for message in payload['greToClientEvent'].get('greToClientMessages', []):
                        if message['type'] == 'GREMessageType_ConnectResp':
                            game.player_deck = [
                                NAME_FROM_CARD_ID[card_id]
                                for card_id in message['connectResp']['deckMessage']['deckCards']
                            ]
                            continue

                        if message['type'] in [
                            'GREMessageType_GameStateMessage',
                            'GREMessageType_QueuedGameStateMessage',
                        ]:
                            self.parse_game_state(game, message)

                i += 1

        except Exception:
            logger.error(f"Game {self.current_game_index}, line {self.log_lines[i]}")
            raise

    def parse_game_state(self, game, message):
        """Return True when the game is over."""

        if message['type'] in ['GREMessageType_GameStateMessage', 'GREMessageType_QueuedGameStateMessage']:
            game_state_message = message['gameStateMessage']

            if game_state_message['type'] == 'GameStateType_Full':
                game_state = {
                    'zones': {
                        'player': {
                            'ZoneType_Library': [],
                            'ZoneType_Hand': [],
                            'ZoneType_Graveyard': [],
                            'ZoneType_Revealed': [],
                        },
                        'opponent': {
                            'ZoneType_Library': [],
                            'ZoneType_Hand': [],
                            'ZoneType_Graveyard': [],
                            'ZoneType_Revealed': [],
                        },
                        'neutral': {
                            'ZoneType_Exile': [],
                            'ZoneType_Battlefield': [],
                            'ZoneType_Stack': [],
                            'ZoneType_Pending': [],
                        },
                    },
                    'player_state': {
                        'player': {
                            'lifeTotal': 20,
                        },
                        'opponent': {
                            'lifeTotal': 20,
                        },
                    },
                    'card_states': {},
                }

            elif game_state_message['type'] == 'GameStateType_Diff':
                try:
                    game_state = deepcopy(game.game_states[-1])
                except KeyError:
                    raise ParserException(f"Got 'GameStateType_Diff' but no previous board states")

            else:
                raise ParserException(f"Got unhandled GameStateType: {game_state_message['type']}")

            # Set players state
            for player in game_state_message.get('players', []):
                if 'lifeTotal' in player:
                    if game.player['systemSeatId'] == player['systemSeatNumber']:
                        game_state['player_state']['player']['lifeTotal'] = player['lifeTotal']

                    if game.opponent['systemSeatId'] == player['systemSeatNumber']:
                        game_state['player_state']['opponent']['lifeTotal'] = player['lifeTotal']

            # Get zone card instances
            for zone in game_state_message.get('zones', []):
                player_key = 'neutral'
                if zone.get('ownerSeatId') == game.player['systemSeatId']:
                    player_key = 'player'
                if zone.get('ownerSeatId') == game.opponent['systemSeatId']:
                    player_key = 'opponent'

                game_state['zones'][player_key][zone['type']] = zone.get('objectInstanceIds', [])

            # Get card states
            game_state['card_states']['tapped'] = {}
            game_state['card_states']['summoning_sickness'] = {}
            game_state['card_states']['attackers'] = {}
            game_state['card_states']['blockers'] = {}
            game_state['card_states']['card_controller'] = {}
            # TODO: Add game_state['card_states']['targeting'] = {}
            for game_object in game_state_message.get('gameObjects', []):

                if game_object['type'] not in ['GameObjectType_Card']:  # TODO: Handle tokens: , 'GameObjectType_Token']:
                    continue

                if game_object.get('isTapped'):
                    game_state['card_states']['tapped'][game_object['instanceId']] = True

                if game_object.get('hasSummoningSickness'):
                    game_state['card_states']['summoning_sickness'][game_object['instanceId']] = True

                if game_object.get('attackState') == 'AttackState_Attacking':
                    game_state['card_states']['attackers'][game_object['instanceId']] = game_object['attackInfo']['targetId']

                if game_object.get('blockState') == 'BlockState_Declared':
                    game_state['card_states']['blockers'][game_object['instanceId']] = game_object['blockInfo']['attackerIds']

                if game_object['ownerSeatId'] != game_object['controllerSeatId']:
                    game_state['card_states']['card_controller'][game_object['instanceId']] = \
                        'player' if game.player['systemSeatId'] == game_object['controllerSeatId'] else 'opponent'

                self.add_cards_to_mapping(game, game_object)

            self.register_changes_in_instance_ids(game, game_state_message.get('annotations', []))

        else:
            raise ParserException(f"Got unhandled message type: {message['type']}")

        # Save board state
        if game.game_states == [] or game_state != game.game_states[-1]:
            game.game_states.append(game_state)

    def add_cards_to_mapping(self, game, game_object):
        if 'name' not in game_object:
            # Happens when a card is taken apart, face down
            return

        card_details = {
            'id': game_object['grpId'],
            'instance_id': game_object['instanceId'],
            'owner': 'player' if game.player['systemSeatId'] == game_object['ownerSeatId'] else 'opponent',
            'name': NAME_FROM_NAME_ID[game_object['name']],
            'types': game_object.get('cardTypes'),
            'subtypes': game_object.get('subtypes'),
            'url_normal': '',
            'url_large': '',
        }
        self.add_image(card_details)
        game.instance_mapping[game_object['instanceId']] = card_details

        if game_object['ownerSeatId'] == game.player['systemSeatId']:
            game.player_played_cards.append(card_details)

        if game_object['ownerSeatId'] == game.opponent['systemSeatId']:
            game.opponent_played_cards.append(card_details)

    def register_changes_in_instance_ids(self, game, annotations):
        for annotation in annotations:
            if 'AnnotationType_ObjectIdChanged' in annotation['type']:
                orig_id = new_id = None
                for detail in annotation.get('details', []):
                    if detail['key'] == 'orig_id':
                        orig_id = detail['valueInt32'][0]
                    if detail['key'] == 'new_id':
                        new_id = detail['valueInt32'][0]

                if game.instance_mapping.get(orig_id) and not game.instance_mapping.get(new_id):
                    game.instance_mapping[new_id] = game.instance_mapping[orig_id]

                elif game.instance_mapping.get(new_id) and not game.instance_mapping.get(orig_id):
                    game.instance_mapping[orig_id] = game.instance_mapping[new_id]

                elif not game.instance_mapping.get(orig_id) or game.instance_mapping.get(orig_id)['id'] == game.instance_mapping.get(new_id)['id']:
                    pass

                elif (
                        'SubType_Adventure' in game.instance_mapping.get(orig_id, {}).get('subtypes') or
                        'SubType_Adventure' in game.instance_mapping.get(new_id, {}).get('subtypes')
                ):
                    # Adventure cards have different arena ids, even though they are technically the same card.
                    pass

                else:
                    raise ParserException(
                        f"Mismatch of instance ids: "
                        f"mapping[orig_id({orig_id})]={game.instance_mapping.get(orig_id)} ; "
                        f"mapping[new_id({new_id})]={game.instance_mapping.get(new_id)}"
                    )

    def add_image(self, card):
        card_image_details = self.get_image_from_card(card)
        card['url_normal'] = card_image_details.get('normal', card_image_details.get('small'))
        card['url_large'] = card_image_details.get('large', card_image_details.get('normal', card_image_details.get('small')))

    def get_image_from_card(self, card):
        if card['id'] in self._image_cache:
            return self._image_cache[card['id']]

        if card['name'] in self._image_cache:
            return self._image_cache[card['name']]

        key = card['id']
        response = requests.get(f"https://api.scryfall.com/cards/arena/{key}")
        if response.status_code == 404:
            key = card['name']
            response = requests.get(f"https://api.scryfall.com/cards/named?exact={key}")

        try:
            self._image_cache[key] = response.json()['image_uris']
        except KeyError:
            logger.error(response.json())
            raise
        return self._image_cache[key]
