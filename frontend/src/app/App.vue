<template>
  <v-layout class="app-container overflow-y-hidden">
    <NavBar />
    <SideBar />

    <v-main class="d-flex flex-column" v-if="showMainContainer">
      <router-view class="pa-6 scroll_style" />
    </v-main>
    <NotificationWrapper />
  </v-layout>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { computed, getCurrentInstance, watch } from 'vue'
  import { useRouter } from 'vue-router'

  import { NavBar } from '@/widgets/navbar'
  import { NotificationWrapper } from '@/widgets/notifications'
  import { SideBar } from '@/widgets/sidebar'

  import { useUiStore } from '@/entities/ui'
  import { useUserStore } from '@/entities/user'

  const { proxy } = getCurrentInstance()
  const router = useRouter()
  const { isLogged } = storeToRefs(useUserStore())
  const { dataLoaded } = storeToRefs(useUiStore())
  const showMainContainer = computed(() => dataLoaded.value || router.currentRoute.value.name === 'auth')

  watch(isLogged, (val) => (val ? proxy.$connect() : proxy.$disconnect()))
</script>

<style lang="scss" src="@/shared/assets/styles/main.scss"></style>
