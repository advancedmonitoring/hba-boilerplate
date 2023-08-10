<template>
  <v-text-field
    v-model="value"
    color="primary"
    variant="underlined"
    @blur="handleBlur"
    :label="label"
    :error-messages="errors"
    :type="type"
  />
</template>

<script setup>
  import { useField } from 'vee-validate'
  import { toRef } from 'vue'

  const props = defineProps({
    name: {
      type: String,
      requird: true,
    },
    type: {
      type: String,
      requird: true,
    },
    label: {
      type: String,
      required: true,
    },
  })

  const { value, handleBlur, errors } = useField(toRef(props, 'name'), undefined)
</script>
