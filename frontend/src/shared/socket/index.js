import { defineStore } from 'pinia'

import { actions } from './socketActions'

export const useSocketStore = defineStore({
  id: 'socket',
  state: () => ({
    isConnected: false,
    reconnectError: false,
    socket: {},
  }),
  actions,
})
