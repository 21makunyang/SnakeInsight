<template>
  <div class="about">
    <guan-zhou-map />
  </div>
</template>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>

<script lang="ts" setup>
import GuanZhouMap from '@/components/charts/GuangZhouMap.vue'

</script>