import { camelCase, isEmpty } from 'lodash'
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

export const notifyError = (error, defaultMessage, type = 'error') => {
  const data = getErrorResponseData(error)

  if (data?.errorType && data.errorType !== VALIDATION_ERROR) {
    const messages = data?.errors || []
    if (!isEmpty(messages)) {
      const message = messages[0].message
      notify(message || defaultMessage, type)
    }
  }
}

export const notify = (message, type = 'error') => {
  dispatch('alert', 'addAlert', { type, message })
}

const VALIDATION_ERROR = 'ValidationError'

export const makeErrors = (error) => {
  const data = getErrorResponseData(error)
  if (data?.errorType === VALIDATION_ERROR) {
    return getErrors(data.errors)
  }

  return null
}

const getErrorResponseData = (error) => {
  const responseData = error?.response?.data
  let data

  if (isBlob(responseData)) {
    responseData.text().then((text) => {
      data = JSON.parse(text)
    })
  } else {
    data = responseData
  }

  return data
}

export function getErrors(errors) {
  const errorMessages = {}
  for (const error of errors) {
    const field = camelCase(error.field)
    if (!(field in errorMessages)) {
      errorMessages[field] = []
    }
    if (!isEmpty(error.errors)) {
      if (Array.isArray(error.errors[0])) {
        errorMessages[field] = error.errors
      } else {
        errorMessages[field].push(getErrors(error.errors))
      }
    } else {
      errorMessages[field].push(error.message || error)
    }
  }

  return errorMessages
}
