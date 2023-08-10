<template>
  <v-checkbox density="compact" :model-value="value" color="primary" :error-messages="errors" />
</template>

<script>
  import { useField } from 'vee-validate'
  export default {
    props: {
      // The group's value
      modelValue: {
        type: null,
      },
      // Field's own value
      value: {
        type: null,
      },
      name: {
        type: String,
      },
      rules: {
        type: String,
        default: undefined,
      },
    },
    setup(props) {
      // We pass a function to make sure the name stays reactive
      const { checked, handleChange, errors } = useField(() => props.name, props.rules, {
        // 👇 These are important
        //type: 'checkbox',
        checkedValue: props.value,
      })
      // select/unselect the input
      handleChange(props.value)
      return {
        checked, // readonly
        handleChange,
        errors,
      }
    },
  }
</script>
