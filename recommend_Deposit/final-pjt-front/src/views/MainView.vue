<template>
  <div>
    <h1 class="main-title">Welcome ^^</h1>
    <div class="cat-container">
      <img v-if="catImage" :src="catImage" alt="Random Cat" class="cat-image">
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const catImage = ref(null);

const getRandomCat = async () => {
  try {
    const response = await axios.get('https://api.thecatapi.com/v1/images/search');
    const imageUrl = response.data[0].url;
    catImage.value = imageUrl;
  } catch (error) {
    console.error('Error fetching cat image:', error);
  }
};

onMounted(getRandomCat);
</script>

<style scoped>
.main-title {
  text-align: center; /* h1 태그를 가운데 정렬 */
  margin-top: 40px; /* 아래로 20px 내림 */
}

.cat-container {
  text-align: center; /* 이미지를 가운데 정렬 */
  margin-top: 40px; /* 아래로 20px 내림 */
}

.cat-image {
  max-width: 100%;
  max-height: 400px;
  border-radius: 10px;
  margin: 20px auto;
}
</style>
