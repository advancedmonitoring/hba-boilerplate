import { createApp } from 'vue'

import { useUserStore } from '@/entities/user'

import router from '@/shared/router'
import { getQueryNextPath } from '@/shared/utils/helpers'

import App from './app/App'
import { registerPlugins } from './app/plugins'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')

useUserStore()
  .init()
  .catch(() => {
    router.push({ name: 'auth', query: getQueryNextPath(router.currentRoute.value) }).catch()
  })
