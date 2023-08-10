import { withVuetifyTheme, DEFAULT_THEME } from './withVeutifyTheme.decorator'
import { setup } from '@storybook/vue3'
import vuetify from '../src/app/plugins/vuetify'

setup((app) => {
  app.use(vuetify)
})

export const globalTypes = {
  theme: {
    name: 'Theme',
    description: 'Global theme for components',
    defaultValue: DEFAULT_THEME,
    toolbar: {
      icon: 'paintbrush',
      // Array of plain string values or MenuItem shape (see below)
      items: [
        { value: 'light', title: 'Light', left: '🌞' },
        { value: 'dark', title: 'Dark', left: '🌛' },
      ],
      // Change title based on selected value
      dynamicTitle: true,
    },
  },
}

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  layout: 'fullscreen',
}

export const decorators = [withVuetifyTheme]
