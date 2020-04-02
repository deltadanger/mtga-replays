<template>
  <div class="card">
    <v-img :src="card.url_normal" />
  </div>
</template>

<script>
export default {

  name: 'Card',

  props: {
    card: Object,
  },
}
</script>

<style scoped lang="scss">
</style>