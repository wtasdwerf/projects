<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <nav>
    <RouterLink to="/">Home</RouterLink>
    |
    <RouterLink to="/search">Search</RouterLink>
    |
    <RouterLink to="/later">Later</RouterLink>
    |
    <RouterLink to="/channel">Channel</RouterLink>
  </nav>

  <RouterView />
</template>

<style scoped>

</style>
