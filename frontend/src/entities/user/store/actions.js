import { dispatch } from '@/shared/utils/dispatch'

import Api from '../api/auth'

export const actions = {
  init() {
    return Api.getCurrentUser().then((response) => {
      if (response.status === 200) {
        this.isLogged = true
      }
    })
  },

  async loginUser(params) {
    return Api.loginUser(params)
      .then((response) => {
        if (response.status === 200) {
          this.isLogged = true
        }
      })
      .catch((error) => {
        const message = error.response.data.detail
        dispatch('alert', 'addAlert', { type: 'error', message })
      })
  },

  async logoutUser() {
    return Api.logoutUser().then(({ status }) => {
      if (status === 200) {
        this.$reset()
      }
    })
  },
}
