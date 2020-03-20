<template>
  <div class="home">

    <v-list shaped>
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
    currentGameStateIndex: 0,
  }),

  computed: {
    currentGameState() {
      if (!this.currentGame) {
        return null;
      }
      return this.currentGame.game_states[this.currentGameStateIndex];
    },
    currentGame() {
      if (!this.games) {
        return null;
      }
      return this.games[this.currentGameIndex];
    },
  },

  components: {
    Board
  },

  created() {
    axios.get('/api/games/').then(result => this.games = result.data);
  },
}
</script>
