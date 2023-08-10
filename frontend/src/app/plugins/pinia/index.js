import { createPinia } from 'pinia'
import { markRaw } from 'vue'

import router from '@/shared/router'
import { dispatchPlugin } from '@/shared/utils/dispatch'
import { wsRelatedPlugin } from '@/shared/utils/wsRelated'

const pinia = createPinia()

pinia.use(({ store }) => {
  store.router = markRaw(router)
})

pinia.use(wsRelatedPlugin).use(dispatchPlugin)

export { pinia }
