<template>
  <v-layout full-height>
    <v-card class="pa-5 ma-auto" width="400px" elevation="10">
      <v-card-title class="pa-0 pb-5 d-flex flex-row align-center justify-space-between">
        <p class="ma-0">{{ $t('loginPage.title') }}</p>
      </v-card-title>
      <v-card-text class="pa-0">
        <Field name="username" v-slot="{ field, errors }" v-model="username" rules="required">
          <BaseTextField
            v-bind="field"
            class="text-center"
            @keyup.enter="onSubmit"
            :error-messages="errors"
            :label="$t('loginPage.login')"
          />
        </Field>
        <Field name="password" v-slot="{ field, errors }" v-model="password" rules="required|min:5">
          <BaseTextField
            v-bind="field"
            class="text-center"
            @keyup.enter="onSubmit"
            :error-messages="errors"
            :type="isShowPassword ? 'text' : 'password'"
            :append-inner-icon="isShowPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:appendInner="isShowPassword = !isShowPassword"
            :label="$t('loginPage.password')"
          />
        </Field>
      </v-card-text>
      <v-card-actions class="px-0 py-4">
        <LoginButton ref="loginButton" :disabled="!isValid" :username="username" :password="password" />
      </v-card-actions>
    </v-card>
  </v-layout>
</template>

<script setup>
  import { Field, useForm, useIsFormValid } from 'vee-validate'
  import { onMounted, ref } from 'vue'

  import { LoginButton } from '@/features/authenticate'

  import { useUserStore } from '@/entities/user'

  import BaseTextField from '@/shared/ui/BaseTextField'

  useForm()
  const loginButton = ref(null)

  const username = ref('')
  const password = ref('')
  const isShowPassword = ref(false)
  const isValid = useIsFormValid()

  const onSubmit = () => {
    if (isValid.value) {
      loginButton.value.login()
    }
  }

  onMounted(() => {
    useUserStore().$reset()
  })
</script>
