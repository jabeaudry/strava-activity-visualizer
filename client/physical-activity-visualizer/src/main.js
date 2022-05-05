import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueRouter from 'vue-router'

Vue.config.productionTip = false
Vue.prototype.$http = axios;
Vue.use(VueRouter);



createApp(App).mount('#app')
