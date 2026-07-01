import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import AdminView from '../views/AdminView.vue' 
import StaffView from '../views/StaffView.vue'
import UserView from '../views/UserView.vue'

const routes = [
  { path: '/', component: LandingView },
  { path: '/register', component: RegisterView },
  { path: '/login', component: LoginView },

  { path: '/admin', component: AdminView, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/staff', component: StaffView, meta: { requiresAuth: true, role: 'staff' } },
  { path: '/user', component: UserView, meta: { requiresAuth: true, role: 'user' } },

  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {

  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  if (to.meta.role && to.meta.role !== role) {
    next('/login')
    return
  }

  next()
})

export default router
