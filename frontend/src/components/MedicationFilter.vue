<template>
  <div class="medication-filter">
    <div class="search-box">
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

    <!-- 自定义下拉框 -->
    <div class="custom-select" ref="selectRef">
      <div class="select-trigger" @click="toggleDropdown">
        <span class="select-value">{{ selectedLabel }}</span>
        <svg
          class="select-arrow"
          :class="{ 'rotate': isOpen }"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </div>

      <transition name="dropdown">
        <div v-if="isOpen" class="select-dropdown">
          <div
            v-for="option in options"
            :key="option.value"
            class="select-option"
            :class="{ 'selected': option.value === filterStatus }"
            @click="selectOption(option.value)"
          >
            <span>{{ option.label }}</span>
            <svg
              v-if="option.value === filterStatus"
              class="check-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
        </div>
      </transition>
    </div>

    <div class="result-count">
      共 {{ resultCount }} 条记录
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
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

const emit = defineEmits(['update:searchQuery', 'update:filterStatus'])

const isOpen = ref(false)
const selectRef = ref(null)

const options = [
  { value: 'all', label: '全部状态' },
  { value: 'active', label: '使用中' },
  { value: 'inactive', label: '已停用' }
]

// 当前选中的标签
const selectedLabel = computed(() => {
  const option = options.find(opt => opt.value === props.filterStatus)
  return option ? option.label : '全部状态'
})

// 切换下拉框
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

// 选择选项
const selectOption = (value) => {
  emit('update:filterStatus', value)
  isOpen.value = false
}

// 点击外部关闭下拉框
const handleClickOutside = (event) => {
  if (selectRef.value && !selectRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.medication-filter {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.search-box {
  flex: 1;
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: var(--color-text-secondary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
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
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

/* 自定义下拉框 */
.custom-select {
  position: relative;
  min-width: 140px;
}

.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
  user-select: none;
}

.select-trigger:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.select-value {
  flex: 1;
}

.select-arrow {
  width: 16px;
  height: 16px;
  color: var(--color-text-secondary);
  transition: transform 0.3s ease;
}

.select-arrow.rotate {
  transform: rotate(180deg);
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  z-index: 100;
}

.select-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.select-option:hover {
  background-color: var(--color-gray-50);
}

.select-option.selected {
  background-color: var(--color-gray-100);
  color: var(--color-primary);
  font-weight: 500;
}

.check-icon {
  width: 16px;
  height: 16px;
  color: var(--color-primary);
}

/* 下拉动画 */
.dropdown-enter-active {
  animation: dropdown-in 0.3s ease-out;
}

.dropdown-leave-active {
  animation: dropdown-out 0.2s ease-in;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes dropdown-out {
  from {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
  to {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
}

.result-count {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .medication-filter {
    flex-direction: column;
    align-items: stretch;
  }

  .search-box {
    max-width: 100%;
  }

  .custom-select {
    min-width: auto;
  }
}
</style>
