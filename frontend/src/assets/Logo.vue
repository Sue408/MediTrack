<template>
  <div class="logo" :style="{ width: size, height: size }">
    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <!-- 医疗十字标志 -->
      <g class="logo-cross">
        <rect x="42" y="25" width="16" height="50" :fill="color" rx="2"/>
        <rect x="25" y="42" width="50" height="16" :fill="color" rx="2"/>
      </g>
      <!-- 外圈 -->
      <circle cx="50" cy="50" r="42" :stroke="color" stroke-width="2.5" fill="none" class="logo-circle"/>
      <!-- 内圈装饰 -->
      <circle cx="50" cy="50" r="35" :stroke="color" stroke-width="1" fill="none" opacity="0.3" class="logo-inner-circle"/>
    </svg>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: '60px'
  },
  color: {
    type: String,
    default: 'var(--color-primary)'
  }
})
</script>

<style scoped>
.logo {
  display: inline-block;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

.logo svg {
  width: 100%;
  height: 100%;
  display: block;
}

.logo-cross,
.logo-circle,
.logo-inner-circle {
  pointer-events: none;
}
</style>
