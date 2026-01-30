<template>
  <div class="date-selector">
    <button @click="$emit('previous')" class="date-nav-btn" aria-label="前一天">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"></polyline>
      </svg>
    </button>

    <div class="date-display">
      <input
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        type="date"
        class="date-input"
        aria-label="选择日期"
      />
      <button @click="$emit('today')" class="today-btn">今天</button>
    </div>

    <button @click="$emit('next')" class="date-nav-btn" aria-label="后一天">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"></polyline>
      </svg>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    required: true
  }
})

defineEmits(['update:modelValue', 'previous', 'next', 'today'])
</script>

<style scoped>
.date-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.date-nav-btn {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-base);
  flex-shrink: 0;
}

.date-nav-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
  transform: scale(1.05);
}

.date-nav-btn:active {
  transform: scale(0.95);
}

.date-nav-btn svg {
  width: 20px;
  height: 20px;
  color: var(--color-text-primary);
}

.date-display {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  max-width: 400px;
}

.date-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  min-width: 0;
}

.date-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

.today-btn {
  padding: 0.75rem 1.25rem;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
  white-space: nowrap;
  flex-shrink: 0;
}

.today-btn:hover {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-light);
}

.today-btn:active {
  transform: scale(0.95);
}

/* 移动端优化 */
@media (max-width: 768px) {
  .date-selector {
    padding: 1rem;
    gap: 0.75rem;
  }

  .date-nav-btn {
    width: 40px;
    height: 40px;
  }

  .date-display {
    gap: 0.5rem;
  }

  .date-input {
    font-size: 0.9375rem;
    padding: 0.625rem 0.75rem;
  }

  .today-btn {
    padding: 0.625rem 1rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .date-selector {
    flex-wrap: wrap;
    justify-content: center;
  }

  .date-display {
    order: -1;
    width: 100%;
    max-width: none;
  }

  .date-nav-btn {
    flex: 1;
    max-width: 120px;
  }
}
</style>
