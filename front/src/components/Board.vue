<template>
  <v-container class="zone-game">
    <cards class="zone-player-hand" :cards="zones.player.hand" @browse="cardsToBrowse = $event" :stacked="zones.player.hand.length > 10"></cards>
    <cards class="zone-player-lands" :cards="zones.player.CardType_Land" @browse="cardsToBrowse = $event" :stacked="zones.player.CardType_Land.length > 10"></cards>
    <cards class="zone-player-creatures" :cards="zones.player.CardType_Creature" @browse="cardsToBrowse = $event" :stacked="zones.player.CardType_Creature.length > 20"></cards>
    <cards class="zone-player-planeswalkers" :cards="zones.player.CardType_Planeswalker" @browse="cardsToBrowse = $event" :stacked="zones.player.CardType_Planeswalker.length > 5"></cards>
    <cards class="zone-player-enchantments" :cards="zones.player.CardType_Enchantment" @browse="cardsToBrowse = $event" :stacked="zones.player.CardType_Enchantment.length > 10"></cards>
    <cards class="zone-player-artifacts" :cards="zones.player.CardType_Artifact" @browse="cardsToBrowse = $event" :stacked="zones.player.CardType_Artifact.length > 10"></cards>
    <cards class="zone-player-library" :cards="zones.player.library" @browse="cardsToBrowse = $event" :stacked="zones.player.library.length > 1"></cards>
    <cards class="zone-player-graveyard" :cards="zones.player.graveyard" @browse="cardsToBrowse = $event" :stacked="zones.player.graveyard.length > 1"></cards>
    <cards class="zone-player-exile" :cards="zones.player.exile" @browse="cardsToBrowse = $event" :stacked="zones.player.exile.length > 1"></cards>
    <cards class="zone-player-command" :cards="zones.player.command" @browse="cardsToBrowse = $event" :stacked="false"></cards>
    <div class="zone-player-life">{{ gameState.player_state.player.lifeTotal }}</div>

    <cards class="zone-opponent-hand" :cards="zones.opponent.hand" @browse="cardsToBrowse = $event" :stacked="zones.opponent.hand.length > 10"></cards>
    <cards class="zone-opponent-lands" :cards="zones.opponent.CardType_Land" @browse="cardsToBrowse = $event" :stacked="zones.opponent.CardType_Land.length > 10"></cards>
    <cards class="zone-opponent-creatures" :cards="zones.opponent.CardType_Creature" @browse="cardsToBrowse = $event" :stacked="zones.opponent.CardType_Creature.length > 20"></cards>
    <cards class="zone-opponent-planeswalkers" :cards="zones.opponent.CardType_Planeswalker" @browse="cardsToBrowse = $event" :stacked="zones.opponent.CardType_Planeswalker.length > 5"></cards>
    <cards class="zone-opponent-enchantments" :cards="zones.opponent.CardType_Enchantment" @browse="cardsToBrowse = $event" :stacked="zones.opponent.CardType_Enchantment.length > 10"></cards>
    <cards class="zone-opponent-artifacts" :cards="zones.opponent.CardType_Artifact" @browse="cardsToBrowse = $event" :stacked="zones.opponent.CardType_Artifact.length > 10"></cards>
    <cards class="zone-opponent-library" :cards="zones.opponent.library" @browse="cardsToBrowse = $event" :stacked="zones.opponent.library.length > 1"></cards>
    <cards class="zone-opponent-graveyard" :cards="zones.opponent.graveyard" @browse="cardsToBrowse = $event" :stacked="zones.opponent.graveyard.length > 1"></cards>
    <cards class="zone-opponent-exile" :cards="zones.opponent.exile" @browse="cardsToBrowse = $event" :stacked="zones.opponent.exile.length > 1"></cards>
    <cards class="zone-opponent-command" :cards="zones.opponent.command" @browse="cardsToBrowse = $event" :stacked="false"></cards>
    <div class="zone-opponent-life">{{ gameState.player_state.opponent.lifeTotal }}</div>

    <cards class="zone-stack" :cards="zones.neutral.stack" @browse="cardsToBrowse = $event" :stacked="false"></cards>

    <div class="card-viewer elevation-24">
      <v-img v-if="cardsToBrowse.length === 1" :src="cardsToBrowse[0].url_large"></v-img>
    </div>

    <v-dialog width="50vw" v-model="showBrowser" @click:outside="cardsToBrowse = []">
      <card-browser :cards="cardsToBrowse"></card-browser>
    </v-dialog>
  </v-container>
</template>

<script>
import Cards from '@/components/Cards.vue'
import CardBrowser from '@/components/CardBrowser.vue'

import cardBack from '../assets/card-back.jpg'

export default {

  name: 'Board',

  props: {
    gameState: Object,
    cardsMapping: Object,
  },

  data() {
    return {
      cardsToBrowse: [],
      showBrowser: false,
    };
  },

  computed: {
    zones() {
      let zones = {
        player: {
          hand: [],
          library: [],
          graveyard: [],
          exile: [],
          command: [],
          CardType_Land: [],
          CardType_Creature: [],
          CardType_Planeswalker: [],
          CardType_Enchantment: [],
          CardType_Artifact: [],
        },
        opponent: {
          hand: [],
          library: [],
          graveyard: [],
          exile: [],
          command: [],
          CardType_Land: [],
          CardType_Creature: [],
          CardType_Planeswalker: [],
          CardType_Enchantment: [],
          CardType_Artifact: [],
        },
        neutral: {
          stack: [],
        },
      };

      if (!this.gameState) {
        return zones;
      }

      zones.player.hand = this.gameState.zones.player.ZoneType_Hand.map(instanceId => this.getCard(instanceId));
      zones.player.library = this.gameState.zones.player.ZoneType_Library.map(instanceId => this.getCard(instanceId));
      zones.player.graveyard = this.gameState.zones.player.ZoneType_Graveyard.map(instanceId => this.getCard(instanceId));

      zones.opponent.hand = this.gameState.zones.opponent.ZoneType_Hand.map(instanceId => this.getCard(instanceId));
      zones.opponent.library = this.gameState.zones.opponent.ZoneType_Library.map(instanceId => this.getCard(instanceId));
      zones.opponent.graveyard = this.gameState.zones.opponent.ZoneType_Graveyard.map(instanceId => this.getCard(instanceId));

      for (let instanceId of this.gameState.zones.neutral.ZoneType_Exile) {
        let card = this.getCard(instanceId);
        let controller = this.gameState.card_states.card_controller[instanceId] || card.owner;
        zones[controller].exile.push(card);
      }

      for (let instanceId of this.gameState.zones.neutral.ZoneType_Battlefield) {
        let card = this.getCard(instanceId);
        let controller = this.gameState.card_states.card_controller[instanceId] || card.owner;
        zones[controller][card.types[0]].push(card);
      }

      for (let instanceId of this.gameState.zones.neutral.ZoneType_Stack) {
        let card = this.getCard(instanceId);
        let controller = this.gameState.card_states.card_controller[instanceId] || card.owner;
        zones.neutral.stack.push(card);
      }

      return zones;
    },
  },

  watch: {
    cardsToBrowse() {
      this.showBrowser = this.cardsToBrowse.length > 1;
    },
  },

  methods: {
    getCard(instanceId) {
      let card = this.cardsMapping[instanceId];
      if (card === undefined) {
        card = {
          // Using snake-case to match object returned by API
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
    Cards,
    CardBrowser,
  },
}
</script>

<style scoped lang="scss">
  @use "sass:math";
  @import '@/assets/constants.scss';

  .card-viewer {
    top: 50%;
    translate: 0 -50%;
    left: 10%;
    width: #{$card-width * 2}vw;
    @include crop-card();
  }

  .zone-game {
    border: 1px solid black;
    width: $game-width;
    height: calc(#{$game-width} * 0.5625);
    position: relative;
    padding: 0;

    > div {
      position: absolute;
    }
  }

  .zone-game-out-hidden {
    overflow: hidden;
  }

  ::v-deep .card {
    position: absolute;
    width: #{$card-width}vw;
    @include crop-card()
  }

  .zone-player-life {
    left: 50%;
    translate: -50%;
    bottom: #{ $card-height * 1.2 }vw;
  }

  .zone-player-hand {
    ::v-deep .card {
      width: #{ $card-width * 1.2 }vw;
    }

    bottom: #{ $card-height * 1.2 }vw;
    left: 50%;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          $offset: math.abs($j - $i / 2);
          transform: translate(calc(-50% + #{($j - $i / 2) * 4.5}vw), #{math.pow($offset, 2) * 0.35 + 2}vw) rotate(#{($j - $i / 2) * 7}deg);
        }
      }
    }
  }

  .zone-player-lands {
    @include row-n(2);

    left: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 20 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-creatures {
    @include row-n(3);

    left: 50%;

    @for $i from 1 through 20 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-planeswalkers {
    @include row-n(3);

    right: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 5 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-enchantments {
    @include row-n(2);

    right: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 5 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-artifacts {
    @include row-n(2);

    right: #{ $card-width * 4.2 }vw;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-library {
    @include row-n(1);
    left: #{ $card-width * 1.6 }vw;
    @include deck-shadow();
  }

  .zone-player-graveyard {
    @include row-n(1);
    left: 1.5vw;
    @include deck-shadow();
  }

  .zone-player-exile {
    @include row-n(1);
    left: #{ $card-width * 3 }vw;
    @include deck-shadow();
  }

  .zone-player-command {
    ::v-deep .card {
      width: #{ $card-width * 1.2 }vw;
    }

    bottom: #{ $card-height * 1.2 }vw;
    left: 80%;
  }

  .zone-opponent-life {
    left: 50%;
    translate: -50%;
    top: #{ $card-height * 0.9 }vw;
  }

  .zone-opponent-hand {
    ::v-deep .card {
      width: #{$card-width * 1}vw;
    }

    top: 0vw;
    left: 50%;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          $offset: math.abs($j - $i / 2);
          transform: translate(calc(-50% + #{($j - $i / 2) * -4.5}vw), #{math.pow($offset, 2) * -0.35 - 2}vw) rotate(#{180 + ($j - $i / 2) * 7}deg);
        }
      }
    }
  }

  .zone-opponent-lands {
    @include row-n(5);

    left: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 20 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-opponent-creatures {
    @include row-n(4);

    left: 50%;

    @for $i from 1 through 20 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-opponent-planeswalkers {
    @include row-n(4);

    right: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 5 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-opponent-enchantments {
    @include row-n(5);

    right: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 5 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-opponent-artifacts {
    @include row-n(5);

    right: #{ $card-width * 4.2 }vw;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        ::v-deep .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-opponent-library {
    @include row-n(6);

    right: #{ $card-width * 2.4 }vw;
    @include deck-shadow();
  }

  .zone-opponent-graveyard {
    @include row-n(6);
    right: #{ $card-width + 1 }vw;
    @include deck-shadow();
  }

  .zone-opponent-exile {
    @include row-n(6);
    left: #{ $card-width * 2.6 }vw;
    @include deck-shadow();
  }

  .zone-opponent-command {
    ::v-deep .card {
      width: #{$card-width * 1}vw;
    }

    top: 0vw;
    left: 20%;
  }

  .zone-stack {
    top: 50%;
    translate: 0 -50%;
    right: 10%;

    ::v-deep .card {
      position: relative;
      width: #{$card-width * 1.5}vw;
    }
  }

</style>