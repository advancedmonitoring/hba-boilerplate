import BaseButton from './BaseButton.vue'

export default {
  title: 'BaseButton',
  component: BaseButton,
}

export const Primary = {
  render: (args) => ({
    components: { BaseButton },
    setup() {
      return { args }
    },
    template: '<BaseButton v-bind="args" />',
  }),
  args: {
    primary: true,
    label: 'BaseButton',
  },
}
