<template>
  <v-navigation-drawer v-model="sidebarOpened" temporary>
    <v-list variant="flat" density="compact" nav class="py-2">
      <v-list-item class="text-left" prepend-icon="mdi-home" :title="$t('menu.about')" to="/" value="home" />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup>
  import { storeToRefs } from 'pinia'

  import { useUiStore } from '@/entities/ui'

  const { sidebarOpened } = storeToRefs(useUiStore())
</script>
