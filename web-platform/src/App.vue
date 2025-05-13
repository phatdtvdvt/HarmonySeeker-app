<template>
    <Menu />
</template>

<script setup>
import Menu from '@/components/Menu/index.vue'
</script>

<style scoped>
nav {
  padding: 20px;
  text-align: center;
}
nav a {
  font-weight: bold;
  color: #2c3e50;
  text-decoration: none;
  margin: 0 10px;
}
nav a.router-link-exact-active {
  color: #42b983;
}
</style>