
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Introduction',
    component: () => import('@/pages/Introduction/index.vue')
  },
  {
    path: '/songchord',
    name: 'SongChord',
    component: () => import('@/pages/SongChord/index.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router