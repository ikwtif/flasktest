import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '../components/Home.vue';
import Ping from '../components/Ping.vue';
import Metselwerk from '../components/berekeningen/Metselwerk.vue';
import Betonkolom from '../components/berekeningen/Betonkolom.vue';
Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/ping',
    name: 'Ping',
    component: Ping,
  },
  {
    path: '/berekeningen/metselwerk',
    name: 'Metselwerk',
    component: Metselwerk,
  },
  {
    path: '/berekeningen/betonkolom',
    name: 'Betonkolom',
    component: Betonkolom,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
