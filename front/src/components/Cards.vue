<template>
  <div v-if="!stacked">
    <div
      v-for="card in cards"
      :key="card.instance_id"
      class="card browse-single"
      @mouseover="onHover(card)"
      @mouseleave="onLeave()"
    >
      <v-img :src="card.url_normal" :lazy-src="cardBackSmall" />
    </div>
  </div>

  <div v-else>
    <div
      v-for="card in cards"
      :key="card.instance_id"
      class="card browse-multiple"
      @click="onClick()"
    >
      <v-img :src="card.url_normal" :lazy-src="cardBackSmall" />
    </div>
  </div>
</template>

<script>
import cardBackSmall from '../assets/card-back-small.jpg'

export default {

  name: 'Card',

  props: {
    cards: Array,
    stacked: {
      type: Boolean,
      default: false,
    }
  },

  data() {
    return {
      cardBackSmall,
    }
  },

  methods: {
    onClick() {
      if (!this.stacked) {
        return;
      }
      this.browse(this.cards);
    },
    onHover(card) {
      if (this.stacked) {
        return;
      }
      this.browse([card])
    },
    onLeave() {
      if (this.stacked) {
        return;
      }
      this.browse([])
    },
    browse(cards) {
      this.$emit('browse', cards);
    },
  },
}
</script>

<style scoped lang="scss">
  .browse-multiple {
    cursor: pointer;
  }
</style>