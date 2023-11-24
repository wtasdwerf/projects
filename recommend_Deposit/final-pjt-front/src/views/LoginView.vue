<template>
  <div class="login-container">
    <h1>로그인</h1>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">username : </label>
        <input type="text" v-model.trim="username" id="username" class="input-field">
      </div>
      <div class="form-group">
        <label for="password">password : </label>
        <input type="password" v-model.trim="password" id="password" class="input-field">
      </div>
      <div>
        <input type="submit" class="submit-button">
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProductStore } from '@/stores/products'

const store = useProductStore()
const username = ref(null)
const password = ref(null)

const login = function () {
    const payload = {
      username: username.value,
      password: password.value
    }
    store.login(payload)
  }
</script>

<style>
/* 컨테이너 정렬 및 패딩 */
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

/* 폼 정렬 및 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
}

/* 각 입력 폼을 그룹으로 묶기 */
.form-group {
  margin-bottom: 15px;
}

/* 라벨 스타일 */
label {
  font-size: 14px;
  margin-right: 10px;
  font-weight: bold;
}

/* 입력 필드 스타일 */
.input-field {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

/* 로그인 버튼 스타일 */
.submit-button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

/* 버튼 호버 효과 */
.submit-button:hover {
  background-color: #0056b3;
}

/* 추가적인 스타일링이 필요한 경우 여기에 추가하세요 */
</style>
