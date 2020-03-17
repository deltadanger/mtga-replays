<template>
  <v-container>
    <h1>Blah {{ result }}</h1>
  </v-container>
</template>

<script>
export default {

  name: 'Board',

  props: {
    game: Object,
  },
}
</script>
