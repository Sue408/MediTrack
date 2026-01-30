<template>
  <div class="search-bar">
    <!-- 搜索框 -->
    <div class="search-input-wrapper">
      <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <input
        :value="searchQuery"
        @input="$emit('update:searchQuery', $event.target.value)"
        type="text"
        class="search-input"
        placeholder="搜索药物名称..."
      />
    </div>

    <!-- 状态筛选 -->
    <div class="filter-group">
      <button
        v-for="option in statusOptions"
        :key="option.value"
        :class="['filter-btn', { active: filterStatus === option.value }]"
        @click="$emit('update:filterStatus', option.value)"
      >
        {{ option.label }}
      </button>
      <!-- 结果统计 -->
      <div class="result-count">
        共 <span class="count-number">{{ resultCount }}</span> 条
      </div>
    </div>

    
  </div>
</template>

<script setup>
defineProps({
  searchQuery: {
    type: String,
    default: ''
  },
  filterStatus: {
    type: String,
    default: 'all'
  },
  resultCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['update:searchQuery', 'update:filterStatus'])

const statusOptions = [
  { value: 'all', label: '全部' },
  { value: 'active', label: '使用中' },
  { value: 'inactive', label: '已停用' }
]
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--color-border-light);
}

/* 搜索框 */
.search-input-wrapper {
  flex: 1;
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 18px;
  height: 18px;
  color: var(--color-text-secondary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.75rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  transition: all var(--transition-base);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.search-input::placeholder {
  color: var(--color-text-secondary);
}

/* 筛选按钮组 */
.filter-group {
  display: flex;
  gap: 0.5rem;
  padding: 0.25rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  overflow: auto;
}

.filter-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  background-color: transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.filter-btn:hover {
  color: var(--color-text-primary);
  background-color: var(--color-gray-100);
}

.filter-btn.active {
  color: var(--color-text-light);
  background-color: var(--color-primary);
}

/* 结果统计 */
.result-count {
  margin-left: 1rem;
  margin-right: 1rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
  display: flex;
  justify-content: center;
  align-items: center;
}

.count-number {
  font-weight: 600;
  color: var(--color-text-primary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-bar {
    flex-wrap: wrap;
  }

  .search-input-wrapper {
    flex: 1 1 100%;
    max-width: 100%;
  }

  .filter-group {
    flex: 1;
  }

  .result-count {
    flex: 0 0 auto;
  }
}
</style>
