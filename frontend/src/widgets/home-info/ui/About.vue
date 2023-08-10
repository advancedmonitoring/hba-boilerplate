<template>
  <div class="ma-auto text-center">
    <img alt="Vue logo" src="@/shared/assets/logo.png" />
    <h1>{{ $t('main.welcome') }}</h1>
    <div class="hello w-50 ma-auto">
      <div class="d-flex py-4 justify-center align-center">
        <a
          class="px-2"
          href=""
          target="_blank"
          rel="noopener"
          >{{ $t('main.appArchitecture') }}</a
        >
        <a
          class="px-2"
          href=""
          target="_blank"
          rel="noopener"
          >GitLab</a
        >
      </div>
      <div class="pt-4">
        <h3 class="pb-3">{{ $t('main.dependencies') }}</h3>
        <div class="d-flex flex-wrap justify-center">
          <div class="pa-2" v-for="item in dependencies" :key="item.href">
            <a :href="item.href" target="_blank" rel="noopener">{{ item.name }}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { dependencies } from '@/widgets/home-info'
</script>
