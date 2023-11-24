import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import ProductDetailView from '@/views/ProductDetailView.vue'
import ProductListView from '@/views/ProductListView.vue'
import ProfileView from '@/views/ProfileView.vue'
import RecommendView from '@/views/RecommendView.vue'
import ProfileUpdateView from '@/views/ProfileUpdateView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
    {
      path: '/products/:id',
      name: 'product_detail',
      component: ProductDetailView,
    },
    {
      path: '/products',
      name: 'product_list',
      component: ProductListView,
    },
    {
      path: '/profile/recommend/:id?',
      name: 'recommend',
      component: RecommendView,
    },
    {
      path: '/profile/:id?',
      name: 'profile',
      component: ProfileView,
    },
    {
      path: '/profile/update/:id?',
      name: 'profile_update',
      component: ProfileUpdateView,
    },
  ]
})

import { useProductStore } from '@/stores/products'

router.beforeEach((to, from) => {
  const store = useProductStore()
  if(to.name !== 'main' && to.name !== 'login' && to.name !== 'signup' && !store.isLogin) {
    window.alert('로그인 해라')
    return { name: 'login' }
  }

  if((to.name === 'login' || to.name === 'signup') && store.isLogin) {
    window.alert('이미 로그인 함')
    return { name: 'product_list' }
  }
})

export default router
