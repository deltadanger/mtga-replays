<template>
  <v-container class="zone-game">
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
    <div class="zone-player-life">{{ gameState.player_state.player.lifeTotal }}</div>

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
    <div class="zone-opponent-life">{{ gameState.player_state.opponent.lifeTotal }}</div>
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
  @use "sass:math";
  $game-width: 75vw;
  $card-width: 5.5;
  $card-height: $card-width * 1.4;
  @mixin row-n($row) {
    > .card {
      transform: perspective(50vw) translateZ(-#{ $row * 1.4 }vw) rotateX(35deg);
    }
    bottom: #{ $card-height * $row * 0.91 + 0.4 }vw;
  }

  @mixin deck-shadow() {
    @for $i from 1 through 60 {
      @for $j from 1 through $i {
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: -#{$j / $i}vw -#{$j / $i / 2}vw;
        }
      }
    }
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

  .card {
    position: absolute;
    width: #{$card-width}vw;
    border-radius: 0.35vw;
    overflow: hidden;
  }

  .zone-player-life {
    left: 50%;
    translate: -50%;
    bottom: #{ $card-height * 1.2 }vw;
  }

  .zone-player-hand {
    > .card {
      width: #{ $card-width * 1.2 }vw;
    }

    bottom: #{ $card-height * 1.2 }vw;
    left: 50%;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
          translate: calc(-50% + #{($j - $i / 2) * 4.5 * (4/$i) }vw);
        }
      }
    }
  }

  .zone-player-creatures {
    @include row-n(3);

    //left: 50%;
    left: #{ $card-width * 2.2 }vw;

    @for $i from 1 through 20 {
      @for $j from 1 through $i {
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
    > .card {
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
    > .card {
      width: #{$card-width * 1}vw;
    }

    top: 0vw;
    left: 50%;

    @for $i from 1 through 10 {
      @for $j from 1 through $i {
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
        .card:nth-child( #{$j} ):nth-last-child( #{$i - $j} ) {
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
    > .card {
      width: #{$card-width * 1}vw;
    }

    top: 0vw;
    left: 20%;
  }

</style>