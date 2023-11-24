<template>
  <div class="container">
    <div class="button-group">
      <a class="btn btn-primary" role="button" @click="goProfile">회원 정보</a>
      <a class="btn btn-disabled" role="button">추천 상품</a>
    </div>

    <h1>추천 상품 리스트</h1>
    <form @submit.prevent="getFilter" class="filter-form">
      <div class="radio-group">
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest1" value="단리" v-model="interest">
          <label class="form-check-label" for="interest1">단리</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="interest" id="interest2" value="복리" v-model="interest">
          <label class="form-check-label" for="interest2">복리</label>
        </div>
        <!-- <label><input type="radio" name="interest" value="단리" v-model="interest"> 단리</label>
        <label><input type="radio" name="interest" value="복리" v-model="interest"> 복리</label> -->
      </div>
      <div class="radio-group">
        <!-- <label><input type="radio" name="month" value="6" v-model="month"> 6개월</label>
        <label><input type="radio" name="month" value="12" v-model="month"> 12개월</label>
        <label><input type="radio" name="month" value="24" v-model="month"> 24개월</label>
        <label><input type="radio" name="month" value="36" v-model="month"> 36개월</label> -->
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month6" value="6" v-model="month">
          <label class="form-check-label" for="month6">6개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month12" value="12" v-model="month">
          <label class="form-check-label" for="month12">12개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month24" value="24" v-model="month">
          <label class="form-check-label" for="month24">24개월</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="month" id="month36" value="36" v-model="month">
          <label class="form-check-label" for="month36">36개월</label>
        </div>
      </div>
      <button type="submit" class="btn-submit">Submit</button>
    </form>

    <ul class="list-group">
      <li class="list-group-item product-item" v-for="product in recommendList" :key="product.id" @click="goDetail(product.id)">
        <div class="product-info">
          <h3 class="bank-name">{{ product.kor_co_nm }}</h3>
          <p class="product-name">{{ product.fin_prdt_nm }}</p>
          <div class="details">
            <p class="detail">가입방법: {{ product.join_way }}</p>
            <!-- <p class="detail">참고사항: {{ product.etc_note }}</p>
            <p class="detail">특혜: {{ product.spcl_cnd }}</p>
            <p class="detail">가입 대상: {{ product.join_member }}</p> -->
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useProductStore } from '../stores/products'
import { useRoute, useRouter } from 'vue-router';

const store = useProductStore()
const router = useRouter()
const route = useRoute()
const recommendList = ref([])

// 추천을 위해 사용할 값들
const interest = ref('')
const month = ref(0)

const goProfile = function () {
  router.push({ name: 'profile', params: {id: route.params.id } })
}

// 상품의 가입 제한 나이 범위 구하기
const getAgeInterval = function (product) {
  const str = product.join_member // 가입 제한
  const join_member = str.split(' ').join('') // 띄어쓰기 제거
  
  let minAge = 0
  let maxAge = 1000
  const len = join_member.length
  for(let i = 0; i < len; i++) {
    if(join_member[i] === '세') {
      if(i-1 >= 0 && 48 <= join_member[i-1].charCodeAt() && join_member[i-1].charCodeAt() <= 57) {
        let age = 0
        age += (i-2 >= 0 && 48 <= join_member[i-2].charCodeAt() && join_member[i-2].charCodeAt() <= 57) ? (join_member[i-2].charCodeAt()-48)*10 : 0
        age += join_member[i-1].charCodeAt()-48

        if(i+3 <= len && join_member.substring(i+1, i+3) === '이상') minAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '초과') minAge = age+1
        if(i+3 <= len && join_member.substring(i+1, i+3) === '이하') maxAge = age
        if(i+3 <= len && join_member.substring(i+1, i+3) === '미만') maxAge = age-1
        if(i+1 < len && join_member[i+1] === '~') minAge = age
        if(i-4 >= 0 && join_member.substring(i-4, i-1).indexOf('~') != -1) maxAge = age
      }
    }
  }

  return [minAge, maxAge]
}

// 상품들의 가입 제한 범위를 구해서 리스트에 모으기
const getAgeIntervalList = function () {
  const ret = [] // 반환할 배열
  for(let i = 0; i < store.products.length; i++) {
    const ageInterval = getAgeInterval(store.products[i]) // 나이 범위 추출
    ret.push(store.products[i].join_member, `${ageInterval[0]}~${ageInterval[1]}`) // 배열에 저장
    console.log(store.products[i].join_member + ' | ' + `${ageInterval[0]}~${ageInterval[1]}`) // 확인을 위해 콘솔에 출력
  }
}

const getFilter = function () {
  const filteredOptionList = []
  console.log(store.options)
  for(let i = 0; i < store.options.length; i++) {
    if(store.options[i].intr_rate_type_nm === interest.value && store.options[i].save_trm == month.value) {
      filteredOptionList.push({
        intr_rate: store.options[i].intr_rate,
        fin_prdt_cd: store.options[i].fin_prdt_cd,
      })
    }
  }

  filteredOptionList.sort(function(a, b) {
    return -a.intr_rate < -b.intr_rate
  })

  console.log(filteredOptionList)

  recommendList.value = []
  filteredOptionList.forEach(op => {
    if(recommendList.value.length < 10) {
      for(let i = 0; i < store.products.length; i++) {
        if(op.fin_prdt_cd === store.products[i].fin_prdt_cd) {
          const ageInterval = getAgeInterval(store.products[i])
          if(ageInterval[0] <= store.userObj.age && store.userObj.age <= ageInterval[1]) {
            recommendList.value.push(store.products[i])
          }
          break
        }
      }
    }
  })

  console.log(recommendList.value)
}

onMounted(() => {
  recommendList.value = []
  store.products.forEach(prod => {
    const ageInterval = getAgeInterval(prod)
    if(ageInterval[0] <= store.userObj.age && store.userObj.age <= ageInterval[1]) {
      recommendList.value.push(prod)
    }
  })
})

const goDetail = function (productId) {
  router.push({ name: 'product_detail', params: { id: productId } })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Roboto', sans-serif;
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

/* 나머지 스타일은 그대로 유지 */

.filter-form {
  margin-bottom: 20px;
  margin-bottom: 40px;
  max-width: 800px;
  margin: 20px auto; /* 화면 중앙에 위치하도록 수정 */
  background-color: #f8f8f8;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.radio-group {
  margin-bottom: 10px;

}

.btn-submit {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: #fff;
  cursor: pointer;
}

.product-item {
  cursor: pointer;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-family: 'Inter', 'Noto Sans KR', sans-serif;
}

.product-item:hover {
  background-color: rgb(95, 245, 208);
}

.radio-group {
  margin-bottom: 10px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

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