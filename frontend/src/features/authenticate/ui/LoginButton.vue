<template>
  <BaseButton :label="$t('loginPage.signIn')" class="w-100" primary @click="login" />
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { watch } from 'vue'
  import { useRouter } from 'vue-router'

  import { useAlertsStore } from '@/entities/alerts'
  import { useUserStore } from '@/entities/user'

  import { ALERT_TYPES } from '@/shared/const/enums'
  import BaseButton from '@/shared/ui/BaseButton'

  const router = useRouter()
  const currentRoute = router.currentRoute.value
  const userStore = useUserStore()
  const { addAlert } = useAlertsStore()
  const { isLogged } = storeToRefs(userStore)

  const props = defineProps({
    username: String,
    password: String,
  })

  const login = () =>
    userStore.loginUser(props).catch((e) => {
      addAlert({ message: e.error.response.data.errors?.[0]?.message, type: ALERT_TYPES.ERROR })
    })

  watch(isLogged, (val) => {
    if (val) {
      if (currentRoute.query.hasOwnProperty('next')) {
        router.push({ path: currentRoute.query.next }).catch()
        return
      }

      router.push({ name: 'home' }).catch()
    }
  })
  defineExpose({
    login,
  })
</script>

