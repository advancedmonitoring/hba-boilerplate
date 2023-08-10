<template>
  <v-menu offset="8">
    <template #activator="{ props }">
      <v-btn v-bind="props" icon>
        <v-icon>mdi-web</v-icon>
      </v-btn>
    </template>

    <v-list class="pa-0">
      <v-list-item v-for="language in languages" :key="language.lang" @click="changeLocale(language.lang)">
        <v-list-item-title class="pointer">
          <p class="ma-0 text-body">{{ language.name }}</p>
        </v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { useI18n } from 'vue-i18n'
  import { useLocale } from 'vuetify'

  import { useUiStore } from '@/entities/ui'

  const uiStore = useUiStore()
  const { current } = useLocale()
  const { locale } = useI18n({ useScope: 'global' })
  const { languages } = storeToRefs(uiStore)

  const changeLocale = (lang) => {
    locale.value = lang
    current.value = lang
    localStorage.lang = lang
  }
</script>
