<template>
  <div>
    <h1>{{ currentVideo.snippet.title }}</h1>
    <p>{{ currentVideo.snippet.publishedAt }}</p>
    <iframe width=720 height=405 :src="videoURL" frameborder="0" allowfullscreen></iframe>
    <p>{{ currentVideo.snippet.description }}</p>
    <button v-if="isSave" @click="removeVideo">저장 취소</button>
    <button v-else @click="addVideo">동영상 저장</button>
    <button @click="addChannel">채널 저장</button>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRoute } from 'vue-router'

const URL = `https://www.googleapis.com/youtube/v3/videos`
const YOUTUBE_API_KEY = import.meta.env.VITE_YOUTUBE_API_KEY

// 라우터
const route = useRoute()
const currentVideo = ref(null)
const videoURL = ref('')
const isSave = ref(false)

axios({
  url: URL,
  method: 'get',
  params: {
    id: route.params.videoId,
    key: YOUTUBE_API_KEY,
    part: 'snippet',
  }
})
.then(response => {
  currentVideo.value = response.data.items[0]
  videoURL.value = `https://www.youtube.com/embed/${response.data.items[0].id}`
  
  const saveVideoList = JSON.parse(localStorage.getItem('video')) || []
  isSave.value = saveVideoList.length > 0 && saveVideoList.find((video) => video._value.id === currentVideo._value.id)
})
.catch(error => {
  console.error(error)
})

// 동영상 추가 저장
const addVideo = function () {
  const saveVideoList = JSON.parse(localStorage.getItem('video')) || []
  saveVideoList.push(currentVideo)
  localStorage.setItem('video', JSON.stringify(saveVideoList))
  isSave.value = true
}

// 저장된 동영상 취소
const removeVideo = function () {
  const saveVideoList = JSON.parse(localStorage.getItem('video')) || []
  const videoIdx = saveVideoList.findIndex(video => video._value.id === currentVideo._value.id)
  console.log(videoIdx)
  saveVideoList.splice(videoIdx, 1)
  console.log(saveVideoList)
  localStorage.setItem('video', JSON.stringify(saveVideoList))
  isSave.value = false
}

const addChannel = function () {
  console.log(currentVideo.value)
  const saveChannelList = JSON.parse(localStorage.getItem('channel')) || []
  saveChannelList.push(currentVideo.value.snippet.channelTitle)
  localStorage.setItem('channel', JSON.stringify(saveChannelList))
}

</script>

<style scoped>

</style>