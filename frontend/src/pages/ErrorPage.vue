<template>
  <div class="ma-auto text-center not-found">
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
  defineProps({
    title: String,
    message: String,
  })
</script>

<style lang="scss" scoped>
  .not-found {
    color: #888;

    h1 {
      font-size: 10rem;
    }

    p {
      font-size: 50px;
      padding-right: 10px;
      animation: type 0.5s alternate infinite;
    }

    @keyframes type {
      from {
        box-shadow: inset -3px 0px 0px #888;
      }
      to {
        box-shadow: inset -3px 0px 0px transparent;
      }
    }
  }
</style>
