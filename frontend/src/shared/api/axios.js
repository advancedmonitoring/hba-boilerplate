import axios from 'axios'
import camelcaseKeys from 'camelcase-keys'
import snakecaseKeys from 'snakecase-keys'

import i18n from '@/shared/translation'

let hostUrl = window.location.origin
const isProduction = process.env.NODE_ENV === 'production'
if (process.env.VUE_APP_SERVER_URL && !isProduction) {
  hostUrl = '//' + process.env.VUE_APP_SERVER_URL
}

axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN'
axios.defaults.withCredentials = true

const API_URL = '/api/v1'

const axiosClient = axios.create({
  baseURL: hostUrl + API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

const formDataAxiosClient = axios.create({
  baseURL: hostUrl + API_URL,
  headers: {
    'Content-Type': 'multipart/form-data',
  },
})

axiosClient.defaults.transformResponse = [
  (data, headers) => {
    if (data && headers['content-type'].includes('application/json')) {
      try {
        return camelcaseKeys(JSON.parse(data), { deep: true })
      } catch {
        return data
      }
    }
    return data
  },
]

axiosClient.defaults.transformRequest = [
  (data, headers) => {
    if (data && headers['Content-Type'].includes('application/json')) {
      return JSON.stringify(snakecaseKeys(data, { deep: true }))
    }
    return data
  },
]

const setLanguage = (config) => {
  config.headers = {
    ...config.headers,
    'Accept-Language': i18n.global.locale,
  }
}

axiosClient.interceptors.request.use((config) => {
  setLanguage(config)
  return config
})

formDataAxiosClient.interceptors.request.use((config) => {
  setLanguage(config)
  return config
})

export { axiosClient, formDataAxiosClient }
