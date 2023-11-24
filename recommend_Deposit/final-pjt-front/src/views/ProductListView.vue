<template>
  <div class="container">
    <h1>상품 리스트</h1>
    <div class="input-group mb-3">
      <input type="text" class="query" placeholder="검색어 입력" aria-label="Query" aria-describedby="search" v-model="query">
      <button class="btn btn-secondary" type="button" id="search" @click="searchByBank">검색</button>
    </div>

    <ul class="list-group">
      <li class="list-group-item product-item" v-for="product in productList" :key="product.id" @click="goDetail(product.id)">
        <div class="product-info">
          <h3 class="bank-name">{{ product.kor_co_nm }}</h3>
          <p class="product-name">{{ product.fin_prdt_nm }}</p>
          <div class="details">
            <p class="detail">가입방법: {{ product.join_way }}</p>
            <p class="detail">참고사항: {{ product.etc_note }}</p>
            <p class="detail">특혜: {{ product.spcl_cnd }}</p>
            <p class="detail">가입 대상: {{ product.join_member }}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useProductStore } from '../stores/products';
import { useRouter } from 'vue-router';

const router = useRouter()
const store = useProductStore()
const query = ref(null)
const productList = ref([])

onMounted(() => {
  productList.value = store.products
})

const goDetail = function (productId) {
  router.push({ name: 'product_detail', params: { id: productId } })
}

const searchByBank = function () {
  productList.value = [];
  if (!query.value || query.value.trim() === '') {
    productList.value = store.products;
  } else {
    store.products.forEach(prod => {
      if (prod.kor_co_nm.includes(query.value)) {
        productList.value.push(prod);
      }
    })
  }
}
</script>

<style scoped>
.container {
  margin-left: 15px;
  margin-right: 15px;
}

.product-item {
  cursor: pointer;
  padding: 15px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
  border-radius: 10px;
  transition: background-color 0.3s;
}

.product-item:hover {
  background-color: rgb(95, 245, 208);
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