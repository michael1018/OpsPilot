import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/view/Login.vue'
import Users from '@/view/Users.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/users',
      name: 'users',
      component: Users
    }
  ]
})
