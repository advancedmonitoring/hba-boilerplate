import Alert from '../model/alert'

export const actions = {
  addAlert(alertData) {
    const alert = new Alert(alertData)
    this.alerts.unshift(alert)
  },

  deleteAlert(alertId) {
    const index = this.alerts.findIndex((item) => alertId === item.id)
    if (index >= 0) {
      this.alerts.splice(index, 1)
    }
  },

  setAlertsPaused(pause) {
    const visibleAlerts = this.alerts.filter((item) => !item.hidden)
    visibleAlerts.forEach((item) => item[pause ? 'pause' : 'start']())
    this.paused = pause
  },
}
