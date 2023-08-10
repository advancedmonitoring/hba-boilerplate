<template>
  <v-switch
    inset
    :ripple="false"
    true-icon="mdi-brightness-3"
    false-icon="mdi-white-balance-sunny"
    @click="toggleTheme"
    color="primary"
    density="comfortable"
    :model-value="theme.global.current.value.dark"
    hide-details
  />
</template>

<script setup>
  import { useTheme } from 'vuetify'

  const theme = useTheme()

  const toggleTheme = () => {
    theme.global.name.value = theme.global.current.value.dark ? 'light' : 'dark'
    localStorage.theme = theme.global.name.value
  }
</script>

<style scoped lang="scss">
  :deep(.v-input__control) {
    .v-icon {
      color: white;

      &::before {
        font-size: 18px;
        height: 18px;
      }
    }

    & .v-selection-control__input::before {
      background-color: transparent;
    }

    & .v-selection-control__input > .v-icon {
      opacity: 1;
    }

    & .v-switch__track {
      opacity: 0.8;
    }
  }
</style>
