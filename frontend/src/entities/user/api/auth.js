import transport from '@/shared/api/transport'

class AuthApi {
  appName = 'accounts'

  getCurrentUser = () => {
    return transport.sendGet(`${this.appName}/me/`, {}, false)
  }

  loginUser = (params) => {
    return transport.sendPost(`${this.appName}/login/`, params, false)
  }

  logoutUser = () => {
    return transport.sendPost(`${this.appName}/logout/`)
  }
}

export default new AuthApi()
