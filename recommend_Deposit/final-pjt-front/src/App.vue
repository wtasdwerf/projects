<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <button class="navbar-toggler ms-auto" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{ name: 'main' }">메인</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'product_list' }">전체 상품 목록</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'profile', params: { id: username } }">프로필</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <a class="nav-link" @click="store.logout()">로그아웃</a>
            </li>
            <li class="nav-item" v-if="!store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'login' }">로그인</RouterLink>
            </li>
            <li class="nav-item" v-if="!store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'signup' }">회원가입</RouterLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="background-container">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, onBeforeUnmount } from 'vue';
import { RouterLink, RouterView } from 'vue-router'
import { useProductStore } from './stores/products'

const store = useProductStore()
const username = computed(() => {
  if(store.userObj === null) return ''
  else return store.userObj.username
})

onMounted(() => {
  store.loadProducts()
})

</script>

<style scoped>
.background-container {
  background-image: url('@/assets/background.jpg'); /* 이미지 경로에 주의하세요. */
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  min-height: 100vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: background-size 0.5s; /* 부드러운 효과를 위한 transition 추가 */
}

</style>