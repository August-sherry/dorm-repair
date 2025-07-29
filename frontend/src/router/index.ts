// src/router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import { useWorkerStore } from '@/stores/worker'
import AdminLayout from '@/views/AdminLayout.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // 主页
    { path: '/', redirect: '/select-role' },
    { path: '/select-role', component: () => import('@/views/SelectRole.vue') },
    { path: '/new', name: 'new-order', component: () => import('@/views/NewOrder.vue') },

    // 维修工登录
    { path: '/login/worker', name: 'WorkerLogin', component: () => import('@/views/Login.vue') },

    // 管理员登录
    { path: '/admin/login', component: () => import('@/views/AdminLogin.vue') },

    // 添加维修工
    {
      path: '/admin/add-worker',
      component: () => import('@/views/AddWorker.vue'),
      meta: { requiresAdmin: true }
    },

    // 左侧导航后台
    {
      path: '/admin',
      component: AdminLayout,
      meta: { requiresWorker: true },
      children: [
        { path: 'worker', name: 'Worker',   component: () => import('@/views/Worker.vue') },
        { path: 'kpi',    name: 'KPI',      component: () => import('@/views/KPI.vue') },
        { path: 'list',   name: 'OrderList',component: () => import('@/views/OrderList.vue') }
      ]
    },

    // 评价页
    { path: '/rate/:id', name: 'Rate', component: () => import('@/views/Rate.vue') },

    // 旧路由统一重定向到左侧导航
    { path: '/worker', redirect: '/admin/worker' },
    { path: '/kpi',    redirect: '/admin/kpi' },
    { path: '/list',   redirect: '/admin/list' }
  ]
})

/* 守卫：先判断管理员，再判断维修工 */
router.beforeEach((to, from, next) => {
  const workerStore = useWorkerStore()

  /* 管理员专用页面 */
  if (to.meta.requiresAdmin && !sessionStorage.getItem('admin')) {
    next('/admin/login')

  /* 维修工/左侧导航页面 */
  } else if (to.matched.some(r => r.meta.requiresWorker) && !workerStore.id) {
    next('/login/worker')

  } else {
    next()
  }
})

export default router
