import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DetailView from '../views/DetailView.vue'
import ChannelView from '../views/ChannelView.vue'
import LaterView from '../views/LaterView.vue'
import SearchView from '../views/SearchView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/:videoId',
      name: 'detail',
      component: DetailView,
    },
    {
      path: '/channel',
      name: 'channel',
      component: ChannelView
    },
    {
      path: '/later',
      name: 'later',
      component: LaterView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
  ]
})

export default router
