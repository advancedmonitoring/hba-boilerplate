import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socketActions } from './socketActions'

export const useUserStore = defineStore('user', {
  state: () => ({
    userData: {},
    isLogged: false,
  }),
  getters: getters,
  actions: {
    ...socketActions,
    ...actions,
  },
  $reset() {
    this.isLogged = false
    this.userData = {}
  },
})
