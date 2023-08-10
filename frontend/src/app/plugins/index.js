import VueNativeSocket from 'vue-native-websocket-vue3'

import router from '@/shared/router'
import i18n from '@/shared/translation'
import { getSubscriptionUrl } from '@/shared/utils/helpers'

import { pinia } from './pinia'
import { socketOptions } from './socket/socket.config'
import vuetify from './vuetify'

import './vee-validate'

export function registerPlugins(app) {
  app.use(i18n).use(vuetify).use(pinia).use(router).use(VueNativeSocket, getSubscriptionUrl(), socketOptions)
}
