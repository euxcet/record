import Vue from 'vue'
import Router from 'vue-router'
import Login from '@/views/Login.vue'
import Record from '@/views/Record.vue'
import Tape from '@/views/Tape.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/record',
      name: 'Record',
      component: Record
    },
    {
      path: '/tape',
      name: 'Tape',
      component: Tape
    }
  ]
})
