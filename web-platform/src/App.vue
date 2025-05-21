<template lang="pug">
  v-app
    v-main
        Menu
        .page-content
        router-view.mt-10
</template>

<script setup lang="ts">
import Menu from '@/components/Menu/index.vue'
</script>

<style lang="sass" scoped>
.app-layout
  display: flex
  min-height: 100vh

.page-content
  flex: 1
  padding: 5px
</style>