<template>
  <div class="container">
    <div class="button-group">
      <a class="btn btn-disabled" role="button">회원 정보</a>
      <a class="btn btn-primary" role="button" @click="goRecommend">추천 상품</a>
    </div>

    <div class="user-info">
      <h1>회원 정보</h1>
      <div v-if="store.userObj.email === ''" class="empty-email">
        이메일을 입력해 주세요.
      </div>
      <div v-else>
        <p>아이디: {{ store.userObj.username }}</p>
        <p>이메일: {{ store.userObj.email }}</p>
        <p>성: {{ store.userObj.first_name }}</p>
        <p>이름: {{ store.userObj.last_name }}</p>
        <p>닉네임: {{ store.userObj.nickname }}</p>
        <p>나이: {{ store.userObj.age }}</p>
        <p>자산: {{ store.userObj.money }}</p>
        <p>월급: {{ store.userObj.salary }}</p>
      </div>

      <button @click="goUserUpdate" class="update-button">회원 정보 수정</button>
      <hr>
      <h1>가입한 상품 목록</h1>
      <div v-for="joinProduct of joinProductsList" :key="joinProduct" class="joined-product">
        <p>{{ joinProduct }}</p>
      </div>
    </div>
  </div>
</template>


<script setup>
import { onMounted, computed } from 'vue';
import { useProductStore } from '../stores/products'
import { useRoute, useRouter } from 'vue-router';

const store = useProductStore()
const router = useRouter()
const route = useRoute()

const joinProductsList = computed(() => {
  const ret = []
  store.userObj.financial_products.forEach(productId => {
    for(let i = 0; i < store.products.length; i++) {
      if(store.products[i].id === productId) {
        ret.push(store.products[i].fin_prdt_nm)
        break
      }
    }
  })
  return ret
})

const goRecommend = function () {
  router.push({ name: 'recommend', params: {id: route.params.id } })
}

const goUserUpdate = function () {
  router.push({ name: 'profile_update', params: { id: route.params.id }})
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  /* 다른 스타일링 */
  font-family: 'Roboto', sans-serif; /* 선택한 귀여운 폰트 적용 */
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.btn {
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 5px;
  font-weight: bold;
  cursor: pointer;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

.user-info {
  margin-bottom: 40px;
  max-width: 800px;
  margin: 20px auto; /* 화면 중앙에 위치하도록 수정 */
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.empty-email {
  font-style: italic;
  color: #ff0000;
}

.update-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #28a745;
  color: #fff;
  cursor: pointer;
}

.joined-product {
  margin-bottom: 5px;
  background-color: #f0f0f0;
  padding: 5px;
  border-radius: 5px;
}
</style>
