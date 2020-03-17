import json
import logging

import requests

from api.models import Game
from api.resources.names import NAME_FROM_NAME_ID, NAME_FROM_CARD_ID


logger = logging.getLogger(__name__)


class ParserException(Exception):
    pass


class MtgaLogParser:
    def __init__(self, log_path):

        with open(log_path, 'r') as f:
            self.log_lines = f.readlines()

        self.games = []

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

                # Get players info
                if 'MatchGameRoomStateChangedEvent' in line:
                    i += 1
                    payload = json.loads(self.log_lines[i])
                    game_room = payload['matchGameRoomStateChangedEvent']['gameRoomInfo']

                    if game_room.get('stateType') == 'MatchGameRoomStateType_Playing':
                        players = game_room['gameRoomConfig']['reservedPlayers']
                        if players[0]['userId'] == current_player_id:
                            game.current_player, game.opponent = players
                        else:
                            game.opponent, game.current_player = players

                    if game_room.get('stateType') == 'MatchGameRoomStateType_MatchCompleted':
                        self.games.append(game)
                        game = None
                        logger.info('Game End')

                # Any game event
                if 'GreToClientEvent' in line:
                    i += 1
                    if self.log_lines[i].strip() == "[Message summarized because one or more GameStateMessages exceeded the 50 GameObject or 50 Annotation limit.]":
                        logger.warning(f"Missing game state details: Game {len(self.games) + 1}, gameStateId {game.board_states[-1]['gameStateId'] if game else 'None'}")
                        continue

                    payload = json.loads(self.log_lines[i])

                    for message in payload['greToClientEvent'].get('greToClientMessages', []):
                        if message['type'] == 'GREMessageType_ConnectResp':
                            game.current_player_deck = [
                                NAME_FROM_CARD_ID[card_id]
                                for card_id in message['connectResp']['deckMessage']['deckCards']
                            ]
                            continue

                        if message['type'] in ['GREMessageType_GameStateMessage', 'GREMessageType_QueuedGameStateMessage']:
                            self.parse_game_state(game, message['gameStateMessage'])

                i += 1

        except Exception:
            logger.error(f"Game {len(self.games) + 1}, gameStateId {game.board_states[-1]['gameStateId'] if game else 'None'}")
            raise

        self.fetch_image_urls()

    def parse_game_state(self, game, game_state_message):
        """Return True when the game is over."""

        # Board update
        if game_state_message['type'] in ['GameStateType_Diff', 'GameStateType_Full']:
            # Check board state
            if len(game.board_states) > 0 and game_state_message['prevGameStateId'] != game.board_states[-1]['gameStateId']:
                logger.warning(
                    f"Previous game state do not match. Got {game_state_message['prevGameStateId']}, "
                    f"expected {game.board_states[-1]['gameStateId']}"
                )

            # Save board state
            game.board_states += [game_state_message]

            # Register mapping between instance id and name of card
            for game_object in game_state_message.get('gameObjects', []):

                if game_object['type'] != 'GameObjectType_Card':
                    continue

                card_details = {
                    'id': game_object['grpId'],
                    'name': NAME_FROM_NAME_ID[game_object['name']],
                    'types': game_object.get('cardTypes'),
                    'subtypes': game_object.get('subtypes'),
                }
                game.instance_mapping[game_object['instanceId']] = card_details

                if game_object['ownerSeatId'] == game.current_player['systemSeatId']:
                    game.current_player_played_cards.append(card_details)

                if game_object['ownerSeatId'] == game.opponent['systemSeatId']:
                    game.opponent_played_cards.append(card_details)

            # Register changes in instance ids, update name of card
            for annotation in game_state_message.get('annotations', []):
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

    def fetch_image_urls(self):
        logger.info("Fetching images...")
        for game in self.games:
            for card in game.instance_mapping.values():
                if card['id'] in game.image_mapping:
                    continue
                response = requests.get(f"https://api.scryfall.com/cards/arena/{card['id']}")
                if response.status_code == 404:
                    response = requests.get(f"https://api.scryfall.com/cards/named?exact={card['name']}")

                card_image_details = response.json()['image_uris']
                game.image_mapping[card['id']] = {
                    'normal': card_image_details.get('normal', card_image_details.get('small')),
                    'large': card_image_details.get('large', card_image_details.get('normal', card_image_details.get('small'))),
                }
        logger.info("Done.")

