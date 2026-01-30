<template>
  <div class="stats-bar">
    <div class="stat-item">
      <div class="stat-icon total">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="9" x2="15" y2="9"></line>
          <line x1="9" y1="15" x2="15" y2="15"></line>
        </svg>
      </div>
      <div class="stat-content">
        <span class="stat-label">总计</span>
        <span class="stat-value">{{ total }}</span>
      </div>
    </div>

    <div class="stat-item">
      <div class="stat-icon completed">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
      </div>
      <div class="stat-content">
        <span class="stat-label">已完成</span>
        <span class="stat-value completed">{{ completed }}</span>
      </div>
    </div>

    <div class="stat-item">
      <div class="stat-icon pending">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </div>
      <div class="stat-content">
        <span class="stat-label">待完成</span>
        <span class="stat-value pending">{{ pending }}</span>
      </div>
    </div>

    <div class="stat-item">
      <div class="stat-icon rate">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <path d="M12 6v6l4 2"></path>
        </svg>
      </div>
      <div class="stat-content">
        <span class="stat-label">完成率</span>
        <span class="stat-value rate">{{ completionRate }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  total: {
    type: Number,
    default: 0
  },
  completed: {
    type: Number,
    default: 0
  }
})

const pending = computed(() => props.total - props.completed)

const completionRate = computed(() => {
  if (props.total === 0) return 0
  return Math.round((props.completed / props.total) * 100)
})
</script>

<style scoped>
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 10px;
  transition: all var(--transition-base);
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 24px;
  height: 24px;
}

.stat-icon.total {
  background-color: rgba(100, 116, 139, 0.1);
  color: var(--color-gray-700);
}

.stat-icon.completed {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.stat-icon.pending {
  background-color: rgba(251, 146, 60, 0.1);
  color: #fb923c;
}

.stat-icon.rate {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 0;
}

.stat-label {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  white-space: nowrap;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  line-height: 1;
}

.stat-value.completed {
  color: #22c55e;
}

.stat-value.pending {
  color: #fb923c;
}

.stat-value.rate {
  color: #3b82f6;
}

/* 平板端优化 */
@media (max-width: 1024px) {
  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    padding: 1rem;
  }

  .stat-item {
    padding: 0.875rem;
  }

  .stat-icon {
    width: 44px;
    height: 44px;
  }

  .stat-icon svg {
    width: 22px;
    height: 22px;
  }

  .stat-value {
    font-size: 1.375rem;
  }
}

/* 移动端优化 */
@media (max-width: 768px) {
  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
    padding: 1rem;
  }

  .stat-item {
    padding: 0.75rem;
    gap: 0.75rem;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
  }

  .stat-icon svg {
    width: 20px;
    height: 20px;
  }

  .stat-label {
    font-size: 0.75rem;
  }

  .stat-value {
    font-size: 1.25rem;
  }
}

/* 小屏手机优化 */
@media (max-width: 480px) {
  .stats-bar {
    grid-template-columns: 1fr;
    gap: 0.5rem;
    padding: 0.75rem;
  }

  .stat-item {
    padding: 0.75rem 1rem;
  }
}
</style>
