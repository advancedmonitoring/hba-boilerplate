import { axiosClient, formDataAxiosClient } from '@/shared/api/axios'
import to from '@/shared/api/to'

class Transport {
  async sendGet(url, config, handleStatus = true) {
    return to(axiosClient.get(url, config), handleStatus)
  }

  async sendPost(url, params = {}, handleStatus = true) {
    return to(axiosClient.post(url, params), handleStatus)
  }

  async sendPostFormData(url, params = {}, config = {}, handleStatus = true) {
    return to(formDataAxiosClient.post(url, params, config), handleStatus)
  }

  async sendPut(url, params = {}) {
    return to(axiosClient.put(url, params))
  }

  async sendPatch(url, params = {}) {
    return to(axiosClient.patch(url, params))
  }

  async sendDelete(url, params = {}) {
    return to(axiosClient.delete(url, { params }))
  }
}

const transport = new Transport()
export default transport
