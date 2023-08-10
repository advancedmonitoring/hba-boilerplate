import { defineStore } from 'pinia'

import { actions } from './actions'
import { getters } from './getters'
import { socketActions } from './socketActions'

export const useAlertsStore = defineStore('alert', {
  state: () => ({
    alerts: [],
    paused: false,
  }),
  getters: getters,
  actions: {
    ...socketActions,
    ...actions,
  },
  $reset() {
    this.alerts = []
    this.paused = false
  },
})
