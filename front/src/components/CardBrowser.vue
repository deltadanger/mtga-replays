<template>
  <v-row ref="scroller" class="image-browser" @wheel="onWheel">
    <v-img
      v-for="(card, index) in cards"
      :key="card.instance_id"
      class="card-slide"
      :src="card.url_large"
      :lazy-src="cardBackSmall"
      @load="onLoad(index)"
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
      triggerOnLoad: true,
    }
  },

  watch: {
    cards() {
      this.triggerOnLoad = true;
    },
  },

  methods: {
    onWheel(event) {
      this.$refs.scroller.scrollLeft += event.deltaY * 30;
    },
    onLoad(position) {
      if (position === this.cards.length - 1) {
        this.triggerOnLoad = false;
      }

      if (this.triggerOnLoad) {
        this.$refs.scroller.scrollLeft = 99999
      }
    }
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