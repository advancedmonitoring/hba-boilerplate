import { createVuetify } from 'vuetify'
import 'vuetify/styles'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import * as labsComponents from 'vuetify/labs/components'
import { ru, en } from 'vuetify/locale'
import '@mdi/font/css/materialdesignicons.css' // Ensure you are using css-loader

const theme = localStorage.theme || 'light'
const locale = localStorage.lang || 'ru'

export default createVuetify({
  components: {
    ...components,
    ...labsComponents,
  },
  directives,
  display: {
    mobileBreakpoint: 'sm',
    thresholds: {
      xs: 0,
      sm: 340,
      md: 540,
      lg: 800,
      xl: 1280,
    },
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    options: {
      customProperties: true,
    },
    defaultTheme: theme,
  },
  locale: {
    locale: locale,
    messages: { ru, en },
  },
})
