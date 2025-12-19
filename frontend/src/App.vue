<template>
  <div id="app">
    <router-view v-if="localNeed"/>
  </div>
</template>

<script>
export default {
  name: 'App',
  provide () {
    return {
      reload: this.reload
    }
  },
  data () {
    return {
      localNeed: true
    }
  },
  methods: {
    reload () {
      this.localNeed = false
      this.$nextTick(() => {
        this.localNeed = true
      })
    }
  }
}
</script>

<style lang="less">
.size{
  width: 100%;
  height: 100%;
}
html,body{
  .size;
  overflow: hidden;
  margin: 0;
  padding: 0;
}
#app {
  .size;
}
</style>
