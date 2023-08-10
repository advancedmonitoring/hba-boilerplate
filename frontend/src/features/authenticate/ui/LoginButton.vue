<template>
  <BaseButton :label="$t('loginPage.signIn')" class="w-100" primary @click="login" />
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { watch } from 'vue'
  import { useRouter } from 'vue-router'

  import { useUserStore } from '@/entities/user'

  import BaseButton from '@/shared/ui/BaseButton'

  const router = useRouter()
  const currentRoute = router.currentRoute.value
  const userStore = useUserStore()
  const { isLogged } = storeToRefs(userStore)

  const props = defineProps({
    username: String,
    password: String,
  })

  const login = () => userStore.loginUser(props)

  watch(isLogged, (val) => {
    if (val) {
      if (currentRoute.query.hasOwnProperty('next')) {
        router.push({ path: currentRoute.query.next }).catch()
        return
      }

      router.push({ name: 'home' }).catch()
    }
  })
</script>
