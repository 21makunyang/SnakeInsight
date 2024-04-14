import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ECharts from 'vue-echarts'
import 'echarts'
import $ from 'jquery'
import ElementPlus from 'element-plus'

const app = createApp(App)
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.use(ElementPlus)
app.component('ECharts', ECharts)
app.config.globalProperties.$ = $

app.mount('#app')
