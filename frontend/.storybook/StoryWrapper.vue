<template>
  <v-app :theme="themeName">
    <v-main>
      <div class="pa-5">
        <slot name="story"></slot>
      </div>
    </v-main>
  </v-app>
</template>

<script>
  export default {
    props: {
      themeName: String,
    },
  }
</script>
