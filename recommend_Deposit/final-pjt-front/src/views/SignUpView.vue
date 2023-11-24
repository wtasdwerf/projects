<template>
  <div class="signup-container">
    <h1>회원 가입</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <div class="form-group">
        <label for="username">username : </label>
        <input type="text" v-model.trim="username" id="username" class="form-input">
      </div>
      <div class="form-group">
        <label for="email">email : </label>
        <input type="text" v-model.trim="email" id="email" class="form-input">
      </div>
      <div class="form-group">
        <label for="password1">password : </label>
        <input type="password" v-model.trim="password1" id="password1" class="form-input">
      </div>
      <div class="form-group">
        <label for="password2">password confirm : </label>
        <input type="password" v-model.trim="password2" id="password2" class="form-input">
      </div>
      <div class="form-group">
        <label for="nickname">nickname : </label>
        <input type="text" v-model.trim="nickname" id="nickname" class="form-input">
      </div>
      <div class="form-group">
        <label for="age">age : </label>
        <input type="text" v-model.trim="age" id="age" class="form-input">
      </div>
      <div class="form-group">
        <label for="money">money : </label>
        <input type="text" v-model.trim="money" id="money" class="form-input">
      </div>
      <div class="form-group">
        <label for="salary">salary : </label>
        <input type="text" v-model.trim="salary" id="salary" class="form-input">
      </div>
      <div class="form-group">
        <input type="submit">
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useProductStore } from '@/stores/products'

const store = useProductStore()
const username = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const age = ref(null)
const money = ref(null)
const salary = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    age: age.value,
    money: money.value,
    salary: salary.value
  }
  store.signUp(payload)
}

</script>

<style scoped>
  .signup-container {
    max-width: 600px;
    margin: 20px auto; /* 화면 중앙에 위치하도록 수정 */
    background-color: #f8f8f8;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    text-align: center; /* 텍스트를 가운데 정렬 */
  }

  .signup-form {
    display: grid;
    gap: 15px;
  }

  .form-group {
    display: flex;
    align-items: center;
  }

  .form-label {
    width: 150px; /* 레이블의 고정 너비 설정 */
  }

  .form-input {
    margin-left: 10px;
    flex: 1; /* 입력 필드가 가능한 최대 너비를 차지하도록 설정 */
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 5px;
  }

  input[type="submit"] {
    background-color: #3498db;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
</style>

