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

  async sendPut(url, params = {}, handleStatus = true) {
    return to(axiosClient.put(url, params), handleStatus)
  }

  async sendPatch(url, params = {}, handleStatus = true) {
    return to(axiosClient.patch(url, params), handleStatus)
  }

  async sendDelete(url, params = {}, handleStatus = true) {
    return to(axiosClient.delete(url, { params }), handleStatus)
  }
}

const transport = new Transport()
export default transport
