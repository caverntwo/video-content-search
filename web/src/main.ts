import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import HomeView from './views/HomeView.vue'
import VideoView from './views/VideoView.vue'
import { createPinia } from 'pinia'

const app = createApp(App);

const pinia = createPinia()


const routes = [
  { path: '/', name:'Home', component: HomeView },
  { path: '/player', name:'Player', component: VideoView },
]

const router = createRouter({
	history: createWebHistory(),
	routes})

app.use(pinia)
app.use(router)
app.mount('#app')
