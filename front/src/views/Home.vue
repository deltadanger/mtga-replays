<template>
  <div class="home">

    <v-list shaped v-if="!currentGame">
      <v-subheader>Games</v-subheader>
      <v-list-item-group v-model="currentGameIndex" color="primary">
        <v-list-item v-for="(game, i) in games" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ game.player.playerName }} VS {{ game.opponent.playerName }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>

    <Board
      v-if="currentGame"
      :game-state="currentGameState"
      :cards-mapping="currentGame.instance_mapping"
    ></Board>

    <v-slider
      v-if="currentGame"
      v-model="currentGameStateIndex"
      :min="0"
      :max="currentGame.game_states.length"
      thumb-label="always"
    ></v-slider>
  </div>
</template>

<script>

import axios from 'axios';
// @ is an alias to /src
import Board from '@/components/Board.vue'

export default {
  name: 'Home',

  data: () => ({
    games: null,
    currentGameIndex: null,
    currentGameStateIndex: null,
    currentGameState: null,
    sliderDebounce: null,
  }),

  computed: {
    currentGame() {
      if (!this.games) {
        return null;
      }
      return this.games[this.currentGameIndex];
    },
  },


  watch: {
    currentGameStateIndex() {
      if (!this.currentGame) {
        this.currentGameState = null;
        return;
      }

      if (this.sliderDebounce) {
        clearTimeout(this.sliderDebounce);
      }
      this.sliderDebounce = setTimeout(() => {
        this.currentGameState = this.currentGame.game_states[this.currentGameStateIndex];
      }, 200);
    },
    currentGame() { if (this.currentGame) setTimeout(() => {this.currentGameStateIndex = 119}, 200) },
  },

  components: {
    Board
  },

  created() {
    axios.get('/api/games/').then(result => this.games = result.data);
  },
}
</script>
