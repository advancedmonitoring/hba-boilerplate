import snakecaseKeys from 'snakecase-keys'

import { dispatch } from './dispatch'

export const getSubscriptionUrl = () => {
  let hostUrl = window.location.host
  const isProduction = process.env.NODE_ENV === 'production'

  if (process.env.VUE_APP_SERVER_URL && !isProduction) {
    hostUrl = process.env.VUE_APP_SERVER_URL
  }

  return '//' + hostUrl + '/ws/v1/'
}

export const getSocketNames = (store) => {
  return Object.getOwnPropertyNames(store).filter((item) => item.startsWith('SOCKET'))
}

export const getSendFunction = (socket, isConnected) => {
  return function sendObj(obj) {
    obj = snakecaseKeys(obj)
    if (isConnected) {
      return socket.send(JSON.stringify(obj))
    }

    const sendInterval = setInterval(() => {
      if (isConnected) {
        socket.send(JSON.stringify(obj))
        clearInterval(sendInterval)
      }
    }, 200)
  }
}

export const getQueryNextPath = (currentRoute) => {
  return currentRoute.path !== '/auth' ? { next: currentRoute.path } : currentRoute.query || {}
}

export const isBlob = (data) => {
  return toString.call(data) === '[object Blob]'
}

export const notify = (error, defaultMessage, type = 'error') => {
  const responseData = error?.response?.data
  if (isBlob(responseData)) {
    responseData.text().then((text) => {
      const data = JSON.parse(text)
      dispatch('alert', 'addAlert', { detail: { type, message: data?.detail || defaultMessage } })
    })
  } else {
    dispatch('alert', 'addAlert', { detail: { type, message: responseData?.detail || defaultMessage } })
  }
}
