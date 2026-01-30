<template>
  <div class="custom-select" ref="selectRef" :class="{ open: isOpen }">
    <!-- 选择器触发按钮 -->
    <div class="select-trigger" @click="toggleDropdown">
      <span class="selected-text">{{ selectedLabel }}</span>
      <svg
        class="arrow-icon"
        :class="{ rotate: isOpen }"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <polyline points="6 9 12 15 18 9"></polyline>
      </svg>
    </div>

    <!-- 下拉选项列表 -->
    <transition name="dropdown">
      <div v-if="isOpen" class="select-dropdown">
        <div class="dropdown-content">
          <div
            v-for="option in options"
            :key="option.value"
            class="select-option"
            :class="{
              selected: modelValue === option.value,
              active: activeIndex === options.indexOf(option)
            }"
            @click="selectOption(option)"
            @mouseenter="activeIndex = options.indexOf(option)"
          >
            <span class="option-label">{{ option.label }}</span>
            <svg
              v-if="modelValue === option.value"
              class="check-icon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    required: true
  },
  options: {
    type: Array,
    required: true,
    // 格式: [{ label: '显示文本', value: '值' }]
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOpen = ref(false)
const selectRef = ref(null)
const activeIndex = ref(-1)

// 获取当前选中项的标签
const selectedLabel = computed(() => {
  const selected = props.options.find(opt => opt.value === props.modelValue)
  return selected ? selected.label : ''
})

// 切换下拉框显示状态
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    // 打开时，设置当前选中项为活动项
    activeIndex.value = props.options.findIndex(opt => opt.value === props.modelValue)
  }
}

// 选择选项
const selectOption = (option) => {
  emit('update:modelValue', option.value)
  emit('change', option.value)
  isOpen.value = false
}

// 点击外部关闭下拉框
const handleClickOutside = (event) => {
  if (selectRef.value && !selectRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

// 键盘导航
const handleKeydown = (event) => {
  if (!isOpen.value) {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      toggleDropdown()
    }
    return
  }

  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      activeIndex.value = Math.min(activeIndex.value + 1, props.options.length - 1)
      break
    case 'ArrowUp':
      event.preventDefault()
      activeIndex.value = Math.max(activeIndex.value - 1, 0)
      break
    case 'Enter':
      event.preventDefault()
      if (activeIndex.value >= 0) {
        selectOption(props.options[activeIndex.value])
      }
      break
    case 'Escape':
      event.preventDefault()
      isOpen.value = false
      break
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.custom-select {
  position: relative;
  width: 100%;
  min-width: 140px;
}

/* 触发按钮 */
.select-trigger {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  user-select: none;
}

.select-trigger:hover {
  border-color: var(--color-gray-400);
  background-color: var(--color-bg-primary);
}

.custom-select.open .select-trigger {
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.selected-text {
  flex: 1;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.arrow-icon {
  width: 20px;
  height: 20px;
  color: var(--color-text-secondary);
  transition: transform 0.2s ease;
  flex-shrink: 0;
}

.arrow-icon.rotate {
  transform: rotate(180deg);
}

/* 下拉列表 */
.select-dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  left: 0;
  right: 0;
  z-index: 1000;
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1), 0 2px 4px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.dropdown-content {
  max-height: 240px;
  overflow-y: auto;
  padding: 0.25rem;
}

/* 自定义滚动条 */
.dropdown-content::-webkit-scrollbar {
  width: 6px;
}

.dropdown-content::-webkit-scrollbar-track {
  background: transparent;
}

.dropdown-content::-webkit-scrollbar-thumb {
  background-color: var(--color-gray-300);
  border-radius: 3px;
}

.dropdown-content::-webkit-scrollbar-thumb:hover {
  background-color: var(--color-gray-400);
}

/* 选项 */
.select-option {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.625rem 0.875rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.select-option:hover,
.select-option.active {
  background-color: var(--color-gray-100);
}

.select-option.selected {
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
}

.select-option.selected:hover {
  background-color: var(--color-gray-800);
}

.option-label {
  flex: 1;
  font-size: 0.9375rem;
  font-weight: 500;
}

.check-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
  color: var(--color-text-light);
}

/* 下拉动画 */
.dropdown-enter-active {
  animation: dropdown-in 0.2s ease-out;
}

.dropdown-leave-active {
  animation: dropdown-out 0.15s ease-in;
}

@keyframes dropdown-in {
  from {
    opacity: 0;
    transform: translateY(-8px) scale(0.96);
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
    transform: translateY(-8px) scale(0.96);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .select-trigger {
    padding: 0.625rem 0.875rem;
  }

  .selected-text,
  .option-label {
    font-size: 0.875rem;
  }
}
</style>
