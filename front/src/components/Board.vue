<template>
  <v-container>
    <div class="zone-player-hand"><card v-for="card in zones.player.hand" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-lands"><card v-for="card in zones.player.CardType_Land" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-creatures"><card v-for="card in zones.player.CardType_Creature" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-planeswalkers"><card v-for="card in zones.player.CardType_Planeswalker" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-enchantments"><card v-for="card in zones.player.CardType_Enchantment" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-artifacts"><card v-for="card in zones.player.CardType_Artifact" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-library"><card v-for="card in zones.player.library" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-graveyard"><card v-for="card in zones.player.graveyard" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-exile"><card v-for="card in zones.player.exile" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-player-command"><card v-for="card in zones.player.command" :key="card.instanceId" :card="card"></card></div>

    <div class="zone-opponent-hand"><card v-for="card in zones.opponent.hand" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-lands"><card v-for="card in zones.opponent.CardType_Land" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-creatures"><card v-for="card in zones.opponent.CardType_Creature" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-planeswalkers"><card v-for="card in zones.opponent.CardType_Planeswalker" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-enchantments"><card v-for="card in zones.opponent.CardType_Enchantment" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-artifacts"><card v-for="card in zones.opponent.CardType_Artifact" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-library"><card v-for="card in zones.opponent.library" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-graveyard"><card v-for="card in zones.opponent.graveyard" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-exile"><card v-for="card in zones.opponent.exile" :key="card.instanceId" :card="card"></card></div>
    <div class="zone-opponent-command"><card v-for="card in zones.opponent.command" :key="card.instanceId" :card="card"></card></div>
  </v-container>
</template>

<script>
import Card from '@/components/Card.vue'
import cardBack from '../assets/card-back.jpg'

export default {

  name: 'Board',

  props: {
    gameState: Object,
    cardsMapping: Object,
  },

  data() {
    return {};
  },

  computed: {
    zones() {
      let zones = {
        player: {
          hand: this.gameState.zones.player.ZoneType_Hand.map(instanceId => this.getCard(instanceId)),
          library: this.gameState.zones.player.ZoneType_Library.map(instanceId => this.getCard(instanceId)),
          graveyard: this.gameState.zones.player.ZoneType_Graveyard.map(instanceId => this.getCard(instanceId)),
          exile: [],
          command: [],
          CardType_Land: [],
          CardType_Creature: [],
          CardType_Planeswalker: [],
          CardType_Enchantment: [],
          CardType_Artifact: [],
        },
        opponent: {
          hand: this.gameState.zones.opponent.ZoneType_Hand.map(instanceId => this.getCard(instanceId)),
          library: this.gameState.zones.opponent.ZoneType_Library.map(instanceId => this.getCard(instanceId)),
          graveyard: this.gameState.zones.opponent.ZoneType_Graveyard.map(instanceId => this.getCard(instanceId)),
          exile: [],
          command: [],
          CardType_Land: [],
          CardType_Creature: [],
          CardType_Planeswalker: [],
          CardType_Enchantment: [],
          CardType_Artifact: [],
        },
      };

      for (let instanceId of this.gameState.zones.neutral.ZoneType_Exile) {
        let card = this.getCard(instanceId);
        let controller = this.gameState.card_states.card_controller[instanceId] || card.owner;
        zones[controller].exile.push(card)
      }

      for (let instanceId of this.gameState.zones.neutral.ZoneType_Battlefield) {
        let card = this.getCard(instanceId);
        let controller = this.gameState.card_states.card_controller[instanceId] || card.owner;
        zones[controller][card.types[0]].push(card)
      }

      return zones;
    },
  },

  methods: {
    getCard(instanceId) {
      let card = this.cardsMapping[instanceId];
      if (card === undefined) {
        card = {
          instance_id: instanceId,
          owner: "player",
          types: [],
          subtypes: [],
          url_large: cardBack,
          url_normal: cardBack,
        };
      }

      if (this.gameState.card_states.attackers[instanceId]) {
        card.isAttacking = true;
      }
      if (this.gameState.card_states.tapped[instanceId]) {
        card.isTapped = true;
      }
      return card;
    },
  },

  components: {
    Card,
  },
}
</script>

<style scoped lang="scss">

</style>