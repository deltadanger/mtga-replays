<template>
  <div class="home">
    <Board
      game="games[0]"
    ></Board>
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
  }),

  components: {
    Board
  },

  created() {
    axios.get('/api/games').then(result => this.games = result.data.games);
  },
}
</script>
