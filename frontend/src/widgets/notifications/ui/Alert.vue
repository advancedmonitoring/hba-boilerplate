<template>
  <v-alert closable width="440" :title="alert.title" :text="alert.message" :type="alert.type" @click:close="onClose">
    <v-progress-linear
      height="6"
      :model-value="alert.progress"
      :buffer-value="alert.buffer"
      class="alert-progress"
      color="white"
    />
  </v-alert>
</template>

<script setup>
  import { useAlertsStore, Alert } from '@/entities/alerts'

  const props = defineProps({
    alert: {
      type: Alert,
      required: true,
    },
  })

  const onClose = () => {
    useAlertsStore().deleteAlert(props.alert.id)
  }
</script>

<style lang="scss" scoped>
  @import '@/shared/assets/styles/mixins.scss';

  @include fade-animation(1.5s);

  .v-alert {
    margin-bottom: 12px;
  }

  .alert-progress {
    height: 6px;
    opacity: 0.5;
    position: absolute;
    bottom: 0;
    left: 0;
  }
</style>
