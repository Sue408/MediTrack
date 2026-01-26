<template>
  <div class="progress-bar-container">
    <div v-if="showHeader" class="progress-header">
      <span class="progress-label">{{ label }}</span>
      <span class="progress-text">{{ text }}</span>
    </div>
    <div class="progress-bar">
      <div
        class="progress-fill"
        :class="`status-${status}`"
        :style="{ width: percentage + '%' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  percentage: {
    type: Number,
    required: true,
    validator: (value) => value >= 0 && value <= 100
  },
  text: {
    type: String,
    default: ''
  },
  label: {
    type: String,
    default: '进度'
  },
  status: {
    type: String,
    default: 'normal',
    validator: (value) => ['normal', 'warning', 'ending', 'completed'].includes(value)
  },
  showHeader: {
    type: Boolean,
    default: true
  }
})
</script>

<style scoped>
.progress-bar-container {
  width: 100%;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.progress-bar {
  height: 8px;
  background-color: var(--color-gray-200);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
  border-radius: 4px;
}

.progress-fill.status-normal {
  background-color: #3b82f6;
}

.progress-fill.status-warning {
  background-color: #f59e0b;
}

.progress-fill.status-ending {
  background-color: #ef4444;
}

.progress-fill.status-completed {
  background-color: #10b981;
}
</style>
