<template>
  <div class="form-container">
    <form @submit.prevent="updateUserProfile" class="user-form">
      <p class="username">username : {{ store.userObj.username }}</p>

      <div class="form-group">
        <label for="email">e-mail : </label>
        <input type="text" id='email' v-model="email" class="input-field">
      </div>
      <div class="form-group">
        <label for="first_name">성 : </label>
        <input type="text" id='first_name' v-model="first_name" class="input-field">
      </div>
      <div class="form-group">
        <label for="last_name">이름 : </label>
        <input type="text" id='last_name' v-model="last_name" class="input-field">
      </div>
      <div class="form-group">
        <label for="nickname">닉네임 : </label>
        <input type="text" id='nickname' v-model="nickname" class="input-field">
      </div>
      <div class="form-group">
        <label for="age">나이 : </label>
        <input type="text" id='age' v-model="age" class="input-field">
      </div>
      <div class="form-group">
        <label for="money">자산 : </label>
        <input type="text" id='money' v-model="money" class="input-field">
      </div>
      <div class="form-group">
        <label for="salary">월급 : </label>
        <input type="text" id='salary' v-model="salary" class="input-field">
      </div>

      <input type='submit' value="수정" class="submit-button">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useProductStore } from '../stores/products';
import { useRoute } from 'vue-router';

const store = useProductStore()
const route = useRoute()

const email = ref(store.userObj.email)
const first_name = ref(store.userObj.first_name)
const last_name = ref(store.userObj.last_name)
const nickname = ref(store.userObj.nickname)
const age = ref(store.userObj.age)
const money = ref(store.userObj.money)
const salary = ref(store.userObj.salary)

const updateUserProfile = function () {
  const payload = {
    username: route.params.id,
    email: email.value,
    first_name: first_name.value,
    last_name: last_name.value,
    nickname: nickname.value,
    age: age.value,
    money: money.value,
    salary: salary.value
  }
  store.updateUserProfile(payload)
}

</script>

<style scoped>
/* 전체 폼을 감싸는 컨테이너 */
.form-container {
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  margin-bottom: 40px;
  max-width: 800px;
  margin: 20px auto; /* 화면 중앙에 위치하도록 수정 */
  background-color: #f8f8f8;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

/* 유저명 텍스트 스타일 */
.username {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 10px;
}

/* 각 입력 폼의 레이아웃을 정돈하는 클래스 */
.form-group {
  margin-bottom: 15px;
}

/* 라벨 디자인 */
label {
  font-size: 14px;
  margin-right: 10px;
  font-weight: bold;
}

/* 입력 필드 디자인 */
.input-field {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
  box-sizing: border-box;
}

/* 수정 버튼 스타일 */
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