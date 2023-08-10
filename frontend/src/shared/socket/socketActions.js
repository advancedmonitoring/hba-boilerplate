import { getSendFunction } from '@/shared/utils/helpers'

export const actions = {
  SOCKET_onopen(event) {
    this.isConnected = true
    const _socket = event.currentTarget
    _socket.sendObj = getSendFunction(_socket, this.isConnected)
    this.socket = _socket
  },

  SOCKET_onclose() {
    this.isConnected = false
  },

  SOCKET_onerror(event) {
    console.error(event)
  },

  SOCKET_RECONNECT(count) {
    console.info('SOCKET_RECONNECT...', count)
  },

  SOCKET_RECONNECT_ERROR() {
    this.reconnectError = true
  },

  sendData(data) {
    this.socket.sendObj(data)
  },
}
