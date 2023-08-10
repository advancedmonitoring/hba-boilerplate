<template>
  <div class="alerts overflow-hidden" :class="{ empty: !alerts.length }">
    <TransitionGroup
      name="alert-transition"
      tag="div"
      @mouseover="alertsStore.setAlertsPaused(true)"
      @mouseout="alertsStore.setAlertsPaused(false)"
    >
      <Alert v-for="alert of alerts" :key="alert.id" progress :alert="alert" />
    </TransitionGroup>
  </div>
</template>

<script setup>
  import { storeToRefs } from 'pinia'
  import { watch } from 'vue'

  import { useAlertsStore } from '@/entities/alerts'

  import Alert from './Alert'

  const alertsStore = useAlertsStore()
  const { visibleAlerts: alerts, paused } = storeToRefs(alertsStore)

  watch(alerts, (val) => {
    if (val.length && !paused.value) val[0].start()
  })
</script>

<style lang="scss" scoped>
  @import '@/shared/assets/styles/variables.scss';
  @import '@/shared/assets/styles/mixins.scss';

  @include fade-animation(0.3s);

  .alerts {
    position: absolute;
    top: #{$nav-bar-height};
    z-index: 100000000;
    right: 0;
    max-height: calc(100vh - #{$nav-bar-height});
    padding: 12px 16px;
    transition: all 0.3s ease;
  }

  .alerts.empty {
    top: calc(#{$nav-bar-height} + 12px);
    padding: 0;
  }

  .alert-transition-leave-from,
  .alert-transition-enter-to {
    opacity: 1;
  }
  .alert-transition-move,
  .alert-transition-enter-active,
  .alert-transition-leave-active {
    transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
  }

  .alert-transition-enter-from,
  .alert-transition-leave-to {
    opacity: 0;
    transform: translateX(500px);
  }
</style>
