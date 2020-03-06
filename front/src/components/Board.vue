<template>
  <v-container>
    <h1>Blah {{ result }}</h1>
  </v-container>
</template>

<script>

  import axios from 'axios';

  export default {

    name: 'Board',

    data: () => ({
      result: null,
    }),

    created() {
      axios.get('/api/board').then(result => this.result = result.data);
    },
  }
</script>
