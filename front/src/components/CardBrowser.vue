<template>
  <v-row ref="scroller" class="image-browser" @wheel="onWheel">
    <v-img
      v-for="card in cards"
      :key="card.instance_id"
      class="card-slide"
      :src="card.url_large"
      :lazy-src="cardBackSmall"
    ></v-img>
  </v-row>
</template>

<script>
import cardBackSmall from '../assets/card-back-small.jpg'

export default {
  name: 'CardBrowser',

  props: {
    cards: Array,
  },

  data() {
    return {
      cardBackSmall,
    }
  },

  watch: {
    cards() {
      console.log(123);
      this.$nextTick(() => this.$refs.scroller.scrollLeft = 99999);
    },
  },

  methods: {
    onWheel(event) {
      this.$refs.scroller.scrollLeft += event.deltaY * 30;
    },
  },
}
</script>

<style scoped lang="scss">
  @import '@/assets/constants.scss';

  .image-browser {
    overflow-x: auto;
    flex-wrap: nowrap;
    padding: 1vw 2vw;
    margin: 0;
    background-color: white;

    .card-slide {
      @include crop-card();
      width: 15vw;
      margin: 0.5vw -1.7vw 0.5vw 0.5vw;
      box-shadow: -1vw 0 2vw black;
    }
  }
</style>