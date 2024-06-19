import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PredictionBySpacePage from '../views/PredictionBySpacePage.vue'
import PredictionByPricePage from "@/views/PredictionByPricePage.vue";
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/home'
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView
    },
    {
      path: '/predictionBySpace',
      name: 'predictionBySpace',
      component: PredictionBySpacePage
    },
    {
      path: '/predictionByPrice',
      name: 'predictionByPrice',
      component: PredictionByPricePage
    }
  ]
})

export default router
