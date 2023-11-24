<template>
  <div>
    <h1>비디오 검색</h1>
    <div class="search-bar">
      <input type="text" v-model="query">
      <button @click="searchVideo">찾기</button>
    </div>
    <div class="video-container">
      <div class="video-card" v-for="video in videoList" @click="goDetail(video)">
        <img :src="video.snippet.thumbnails.default.url" alt="">
        <p>{{ video.snippet.title }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const URL = "https://www.googleapis.com/youtube/v3/search"
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

// 영상 리스트
const videoList = ref([])
// 검색어
const query = ref('')
// 라우터
const router = useRouter()

// 검색 실시
const searchVideo = function () {
  axios({
    url: URL,
    method: 'get',
    params: {
      part: 'snippet',
      q: query.value,
      key: YOUTUBE_API_KEY,
      type: 'video',
      maxResults: 10,
    }
  })
  .then(response => {
    videoList.value = response.data.items
  })
  .catch(error => {
    console.error(error)
  })
}

// 영상 상세 페이지로 이동
const goDetail = function (video) {
  router.push(`/${video.id.videoId}`)
}
</script>

<style scoped>
.video-card {
  border: 1px red solid
}
</style>