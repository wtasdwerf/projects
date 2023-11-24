<template>
  <div class="container">
    <div class="product-info">
      <h3 class="bank-name">{{ product.kor_co_nm }}</h3>
      <p class="product-name">{{ product.fin_prdt_nm }}</p>
      <div class="details">
        <p class="detail">가입방법: {{ product.join_way }}</p>
        <p class="detail">참고사항: {{ product.etc_note }}</p>
        <p class="detail">특혜: {{ product.spcl_cnd }}</p>
        <p class="detail">가입 대상: {{ product.join_member }}</p>
      </div>
      <a v-show="!isJoin" class="btn btn-primary" role="button" @click="addCart">관심 상품 등록</a>
      <a v-show="isJoin" class="btn btn-danger" role="button" @click="deleteCart">해제</a>
    </div>
    <!-- <div class="product-info">
      <p>은행명 : {{ product.kor_co_nm }}</p>
      <p>상품명 : {{ product.fin_prdt_nm }}</p>
      <p>가입방법 : {{ product.join_way }}</p>
      <p>참고사항 : {{ product.etc_note }}</p>
      <p>특혜 : {{ product.spcl_cnd }}</p>
      <p>가입 대상 : {{ product.join_member }}</p>
      <a v-show="!isJoin" class="btn btn-primary" role="button" @click="addCart">가입하기</a>
      <a v-show="isJoin" class="btn btn-danger" role="button" @click="deleteCart">가입취소</a>
    </div> -->
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useProductStore } from '../stores/products';
import { useRoute } from 'vue-router';

const route = useRoute()
const store = useProductStore()
const product = store.getProductById(Number(route.params.id))
const isJoin = computed (() => {
  return store.userObj.financial_products.indexOf(product.id) != -1
})

const addCart = function () {
  store.addCart(Number(route.params.id))
}

const deleteCart = function () {
  store.deleteCart(Number(route.params.id))
}
</script>

<style scoped>
.container {
  margin-left: 15px; /* 왼쪽 여백 조정 */
  margin-right: 15px; /* 오른쪽 여백 조정 */
}

.product-info {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-family: 'Arial', sans-serif; /* 폰트 변경 */
  background-color: #f8f8f8;
  margin-top: 40px;
}

/* 버튼들 사이 여백 조정 */
.btn {
  margin-right: 10px;
}

.product-info {
  color: #333;
}

.bank-name {
  font-weight: bold;
  font-size: 24px;
  margin-bottom: 10px;
  font-family: 'Nanum Gothic', sans-serif;
}

.product-name {
  font-size: 18px;
  margin-bottom: 10px;
  font-family: 'Nanum Gothic', sans-serif;
}

.details {
  font-size: 16px;
}

.detail {
  margin-bottom: 5px;
  font-family: 'Nanum Gothic', sans-serif;
}

.query {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.btn-outline-secondary {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
</style>