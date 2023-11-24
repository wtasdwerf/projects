import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useProductStore = defineStore('product', () => {
  const products = ref([])
  const options = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const client_name = ref(null)
  const userObj = ref(null)
  const router = useRouter()
  const isLogin = computed(() => {
    return token.value != null
  })

  // API를 통해서 데이터를 가져온 후 DB에 저장
  const loadProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/save-products/`,
      // headers: {
      //   Authorization: `Token ${token.value}`
      // }
    })
      .then((res) => {
        console.log(res)
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 전체 예금 상품 조회
  const getAllProducts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/products/`,
      // headers: {
      //   Authorization: `Token ${token.value}`
      // }
    })
      .then((res) => {
        console.log(res)
        products.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const getAllOptions = function () {
    axios({
      method: 'get',
      url: `${API_URL}/products/options/`,
      // headers: {
      //   Authorization: `Token ${token.value}`
      // }
    })
      .then((res) => {
        console.log(res)
        options.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }

  // 상품 ID에 따라 상품 정보 빼오기
  const getProductById = function (productId) {
    let product = null
    products.value.forEach(prod => {
      if(prod.id === productId) {
        product = prod
      }
    })

    return product
  }

  // 회원 가입
  const signUp = function (payload) {
    const { username, email, password1, password2, nickname, age, money, salary } = payload
    console.log(payload)
    axios({
      method: 'post',
      url: `${API_URL}/dj_rest_auth/signup/`,
      data: {
        username, email, password1, password2, nickname, age, money, salary
      }
    })
      .then(response => {
        console.log(response)
        const password = password1
        login({username, password})
      })
      .catch(error => {
        console.log(error)
        window.alert('입력한 정보를 다시 확인해주세요.(중복되는 정보 및 비밀번호를 다시 확인해주세요)')
      })
  }

  // 로그인
  const login = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/dj_rest_auth/login/`,
      data: {
        username, password,
      }
    })
      .then(response => {
        console.log(response.data)
        token.value = response.data.key
        client_name.value = username
        console.log(client_name.value)
        getUserProfile()
        getAllProducts()
        getAllOptions()
        router.push({ name: 'main' })
      })
      .catch(error => {
        window.alert('아이디와 비밀번호를 확인해주세요.')
        console.log(error)
      })
  }

  // 로그아웃
  const logout = function () {
    axios({
      method: 'post',
      url: `${API_URL}/dj_rest_auth/logout/`,
    })
      .then(response => {
        console.log(response.data)
        token.value = null
        userObj.value = null
        client_name.value = null
        router.push({ name: 'main' })
      })
      .catch(error => {
        console.log(error)
      })
  }

  // 회원 정보 빼오기
  const getUserProfile = function () {
    axios({
      method: 'get',
      url: `${API_URL}/accounts/user/${client_name.value}`,
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        console.log(response.data)
        userObj.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }

  // 회원 정보 빼오기
  const updateUserProfile = function (payload) {
    const { username, email, first_name, last_name, nickname, age, money, salary } = payload
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/${username}/`,
      data: {
        username, email, first_name, last_name, nickname, age, money, salary
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        router.push({ name: 'profile', params: { id: userObj.value.username }})
      })
      .catch(error => {
        console.log(error)
      })
  }

  const addCart = function (productId) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/add_cart/`,
      data: {
        productId,
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        console.log(userObj.value.financial_products)
      })
      .catch(error => {
        console.log(error)
      })
  }

  const deleteCart = function (productId) {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/user/delete_cart/`,
      data: {
        productId,
      },
      headers: {
        Authorization: `Token ${token.value}`
      },
    })
      .then(response => {
        userObj.value = response.data
        console.log(response)
      })
      .catch(error => {
        console.log(error)
      })
  }
  
  return { getAllProducts, API_URL, products, getProductById, login, signUp, token, isLogin, logout, getUserProfile, userObj, updateUserProfile, addCart, deleteCart, loadProducts, options }
}, { persist: true })
