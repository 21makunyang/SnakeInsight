import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
import ECharts from 'vue-echarts'
import 'echarts'
import locale from 'element-plus/es/locale/lang/zh-cn'
import $ from 'jquery'

const app = createApp(App)
const pinia = createPinia();
pinia.use(piniaPluginPersistedstate)

app.use(pinia)
app.use(router)
app.component('ECharts', ECharts)
app.config.globalProperties.$ = $

app.mount('#app')
