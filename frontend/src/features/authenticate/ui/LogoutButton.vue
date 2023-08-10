<template>
  <v-btn v-if="isLogged" icon @click="logout">
    <v-icon>mdi-logout</v-icon>
  </v-btn>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { useRouter } from 'vue-router'

  import { useUserStore } from '@/entities/user'

  const userStore = useUserStore()
  const { isLogged } = storeToRefs(userStore)
  const router = useRouter()

  const logout = async () => {
    await userStore.logoutUser()
    router.push({ name: 'auth' })
  }
</script>
