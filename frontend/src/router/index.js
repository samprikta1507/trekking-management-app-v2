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
  { path: '/admin', component: AdminView }, 
  { path: '/staff', component: StaffView },
  { path: '/user', component: UserView },
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
