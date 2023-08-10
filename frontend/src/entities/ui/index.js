import { defineStore } from 'pinia'

import { actions } from './actions'
import { socketActions } from './socketActions'

export const useUiStore = defineStore('ui', {
  state: () => ({
    releaseVersion: 'dev',
    dataLoaded: false,
    sidebarOpened: false,
    languages: {
      ru: {
        lang: 'ru',
        name: 'Русский',
      },
      en: {
        lang: 'en',
        name: 'English',
      },
    },
  }),
  actions: {
    ...socketActions,
    ...actions,
  },
  $reset() {
    this.sidebarOpened = false
  },
})
