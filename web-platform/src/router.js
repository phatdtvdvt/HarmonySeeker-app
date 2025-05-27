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
  },
  {
    path: '/voiceseparator',
    name: 'VoiceSeparator',
    component: () => import('@/pages/VoiceSeparator/index.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router