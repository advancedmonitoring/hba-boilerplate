import router from '@/shared/router'
import i18n from '@/shared/translation'
import { getQueryNextPath, makeErrors, notifyError } from '@/shared/utils/helpers'

export default function to(promise, handleStatus = true) {
  return promise
    .then((data) => {
      return data
    })
    .catch((error) => {
      if (handleStatus) {
        switch (error.response.status) {
          case 400:
          case 500:
            notifyError(error, i18n.global.t('main.requestError'))
            break
          case 403:
            notifyError(error, i18n.global.t('main.permissionsDenied'))
            break
          case 401:
            router.push({ name: 'auth', query: getQueryNextPath(router.currentRoute.value) }).then()
            break
        }
      }
      const validationErrors = makeErrors(error)
      return Promise.reject({ error, validationErrors })
    })
}
