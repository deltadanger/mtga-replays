<template>
  <div>
    <v-img :src="card.url_normal" height="100px" contain/>
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