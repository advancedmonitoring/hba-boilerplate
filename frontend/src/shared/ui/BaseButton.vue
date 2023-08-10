<template>
  <v-btn type="button" color="primary" @click="onClick" :variant="variant" :size="size">{{ label }}</v-btn>
</template>

<script>
  import { reactive, computed } from 'vue'
  export default {
    name: 'BaseButton',
    props: {
      label: {
        type: String,
        required: true,
      },
      primary: {
        type: Boolean,
        default: false,
      },
      size: {
        type: String,
        validator: (value) => {
          return ['small', 'large'].indexOf(value) !== -1
        },
      },
      backgroundColor: {
        type: String,
      },
    },
    emits: ['click'],
    setup(props, { emit }) {
      props = reactive(props)
      return {
        onClick() {
          emit('click')
        },
        variant: computed(() => (props.primary ? 'flat' : 'tonal')),
      }
    },
  }
</script>
