export const getters = {
  visibleAlerts: (state) => {
    return state.alerts.filter((item) => !item.hidden).slice(0, 6)
  },
}
