import camelcaseKeys from 'camelcase-keys'

import { pinia } from '../pinia'

import iterSocketActions from './useSocketActions'

export const socketOptions = {
  store: pinia,
  format: 'json',
  connectManually: true,
  reconnection: true, // (Boolean) whether to reconnect automatically (false)
  reconnectionAttempts: 15, // (Number) number of reconnection attempts before giving up (Infinity),
  reconnectionDelay: 5000, // (Number) how long to initially wait before attempting a new (1000)
  passToStoreHandler: function (eventName, event) {
    if (!eventName.startsWith('SOCKET_')) {
      return
    }

    let target = eventName
    let msg = event

    if (this.format === 'json' && event.data) {
      msg = JSON.parse(event.data)
      target = 'SOCKET_' + msg.event
    }

    const data = msg.data ? camelcaseKeys(msg.data, { deep: true }) : msg

    for (const actions of iterSocketActions(target)) {
      actions[target](data)
    }
  },
}
