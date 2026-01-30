<template>
  <teleport to="body">
    <transition name="toast-fade">
      <div v-show="visible" class="toast-container" :class="`toast-${type}`">
        <div class="toast-icon">
          <!-- 成功图标 -->
          <svg v-if="type === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <!-- 错误图标 -->
          <svg v-else-if="type === 'error'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          <!-- 警告图标 -->
          <svg v-else-if="type === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
            <line x1="12" y1="9" x2="12" y2="13"></line>
            <line x1="12" y1="17" x2="12.01" y2="17"></line>
          </svg>
          <!-- 信息图标 -->
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="16" x2="12" y2="12"></line>
            <line x1="12" y1="8" x2="12.01" y2="8"></line>
          </svg>
        </div>
        <div class="toast-content">
          <p class="toast-message">{{ message }}</p>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
// 定义外部插槽
const props = defineProps({
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value) // 类型验证
  },
  duration: {
    type: Number,
    default: 3000
  },
})
// 定义关闭事件
const emit = defineEmits(['close'])
// 控制组件显示
const visible = ref(false)
// 预定义定时器变量
let timer = null

onMounted(() => {
  // 挂载后立即显示 (0.3s加载动画)
  visible.value = true

  // 设置自动关闭定时器
  timer = setTimeout(() => {
    // 首先隐藏内容
    visible.value = false
    // 等待消失动画(0.3s)完成后触发关闭事件 (卸载对象)
    setTimeout(() => {
      emit('close')
    }, 350)
  }, props.duration)
})

onUnmounted(() => {
  // 在卸载后清除定时器对象
  if (timer) {
    clearTimeout(timer)
  }
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 9999;
  min-width: 300px;
  max-width: 500px;
  pointer-events: auto;
}

.toast-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast-icon svg {
  width: 100%;
  height: 100%;
}

.toast-content {
  flex: 1;
}

.toast-message {
  margin: 0;
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--color-text-primary);
  line-height: 1.5;
}

/* 成功样式 */
.toast-success {
  border-left: 4px solid #10b981;
}

.toast-success .toast-icon {
  color: #10b981;
}

/* 错误样式 */
.toast-error {
  border-left: 4px solid #ef4444;
}

.toast-error .toast-icon {
  color: #ef4444;
}

/* 警告样式 */
.toast-warning {
  border-left: 4px solid #f59e0b;
}

.toast-warning .toast-icon {
  color: #f59e0b;
}

/* 信息样式 */
.toast-info {
  border-left: 4px solid #3b82f6;
}

.toast-info .toast-icon {
  color: #3b82f6;
}

/* 动画 */
.toast-fade-enter-active {
  animation: toast-in 0.3s ease-out;
}

.toast-fade-leave-active {
  animation: toast-out 0.3s ease-in;
}

@keyframes toast-in {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

@keyframes toast-out {
  from {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
  to {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .toast-container {
    min-width: auto;
    max-width: calc(100vw - 2rem);
    left: 1rem;
    right: 1rem;
    transform: none;
  }

  @keyframes toast-in {
    from {
      opacity: 0;
      transform: translateY(-20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes toast-out {
    from {
      opacity: 1;
      transform: translateY(0);
    }
    to {
      opacity: 0;
      transform: translateY(-20px);
    }
  }
}
</style>
