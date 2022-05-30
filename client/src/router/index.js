import Vue from 'vue';
import VueRouter from 'vue-router';
import Activities from '../components/Activities.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'my-activities',
    component: Activities,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
