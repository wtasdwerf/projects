<template>
  <div>
    <h1>저장된 채널 목록</h1>
    <ul v-for="channel in saveChannelList">
      <li>
        {{ channel }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const saveChannelList = ref([])
saveChannelList.value = JSON.parse(localStorage.getItem('channel')) || []
</script>

<style scoped>

</style>