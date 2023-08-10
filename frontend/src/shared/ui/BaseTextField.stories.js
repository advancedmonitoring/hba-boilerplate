import BaseTextField from './BaseTextField.vue'

export default {
  title: 'BaseTextField',
  component: BaseTextField,
}

export const Default = {
  render: (args) => ({
    components: { BaseTextField },
    setup() {
      return { args }
    },
    template: '<BaseTextField v-bind="args" />',
  }),
  args: {
    label: 'BaseTextField',
  },
}
