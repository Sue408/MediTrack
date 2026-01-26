import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    redirect: '/auth'
  },
  {
    path: '/auth',
    name: 'Auth',
    component: () => import('@/views/Auth.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const isAuthenticated = userStore.isAuthenticated()

  // 需要认证的页面
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth')
  }
  // 已登录用户访问登录页，重定向到首页
  else if (to.path === '/auth' && isAuthenticated) {
    next('/home')
  }
  else {
    next()
  }
})

export default router
