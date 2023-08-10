<template>
  <v-app-bar>
    <template v-slot:prepend v-if="isLogged">
      <v-app-bar-nav-icon @click.stop="toggleSidebar"></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title v-if="isLogged">{{ $t('main.title') }}</v-app-bar-title>

    <v-spacer />

    <div class="d-flex px-4">
      <div class="mr-3">
        <ToggleThemeButton />
      </div>
      <div class="mr-1">
        <ChangeLanguageButton />
      </div>
      <div>
        <LogoutButton />
      </div>
    </div>
  </v-app-bar>
</template>

<script setup>
  import { storeToRefs } from 'pinia'

  import { LogoutButton } from '@/features/authenticate'
  import { ChangeLanguageButton } from '@/features/change-language'
  import { ToggleThemeButton } from '@/features/toggle-theme'

  import { useUiStore } from '@/entities/ui'
  import { useUserStore } from '@/entities/user'

  const uiStore = useUiStore()

  const { isLogged } = storeToRefs(useUserStore())

  const { toggleSidebar } = uiStore
</script>
