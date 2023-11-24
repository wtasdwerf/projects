<template>
  <div>
    <h1>나중에 볼 동영상</h1>
    <div v-if="saveVideoList.length > 0">
      <div v-for="video in saveVideoList"  class="video-container">
        <div class="video-card">
          <img :src="video._value.snippet.thumbnails.default.url" alt="">
          <p>{{ video._value.snippet.title }}</p>
        </div>
      </div>
    </div>
    <div v-else>
      <p>등록된 비디오 없음</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const saveVideoList = ref([])
saveVideoList.value = JSON.parse(localStorage.getItem('video')) || []
</script>

<style scoped>
.video-card {
  border: 1px red solid
}
</style>