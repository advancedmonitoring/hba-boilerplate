import camelcaseKeys from 'camelcase-keys'
import { isArray, isUndefined } from 'lodash'

import { ALERT_VIEW_TYPE, ALERT_TYPES } from '@/shared/const/enums'

import { useAlertsStore } from '../store'

const TYPES = {
  1: ALERT_TYPES.INFO,
  2: ALERT_TYPES.SUCCESS,
  3: ALERT_TYPES.WARNING,
  4: ALERT_TYPES.ERROR,
}

class Alert {
  constructor(obj) {
    this.id = obj.id || new Date().getTime()
    this.message = obj.message
    this.title = obj.title || null
    this.extra = obj.extra || {}
    this.hidden = obj.hidden || false
    this.timer = 0
    this.interval = null
    this.paused = true
    this.timeout = 5
    this.buffer = 100
    this.read = obj.read || false
    this.store = obj.store || false
    this.viewType = obj.viewType || ALERT_VIEW_TYPE.SHORT
    this.type = obj.type || (obj.level ? TYPES[obj.level] : ALERT_TYPES.INFO)
    this.extraData = camelcaseKeys(obj.extra, { deep: true }) || {}
    this.expiring = isUndefined(this.extraData.expiring) ? true : Boolean(this.extraData.expiring)
  }

  start() {
    if (!this.paused) return

    if (this.expiring) {
      this.paused = false
      this.interval = setInterval(() => {
        this.timer += 100 / 1000
        if (this.timer > this.timeout) {
          useAlertsStore().deleteAlert(this.id)
          clearInterval(this.interval)
        }
      }, 100)
    }
  }

  pause() {
    this.paused = true
    clearInterval(this.interval)
  }

  get progress() {
    return this.timer * (this.buffer / this.timeout)
  }
}

export default Alert
