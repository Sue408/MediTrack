<template>
  <teleport to="body">
    <transition name="confirm-fade">
      <div v-if="visible" class="confirm-overlay" @click.self="handleCancel">
        <div class="confirm-dialog">
          <!-- 图标 -->
          <div class="confirm-icon" :class="`icon-${type}`">
            <!-- 警告图标 -->
            <svg v-if="type === 'warning'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <!-- 危险图标 -->
            <svg v-else-if="type === 'danger'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <!-- 信息图标 -->
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
          </div>

          <!-- 标题 -->
          <h3 class="confirm-title">{{ title }}</h3>

          <!-- 消息 -->
          <p class="confirm-message">{{ message }}</p>

          <!-- 按钮组 -->
          <div class="confirm-actions">
            <button
              @click="handleCancel"
              class="confirm-btn btn-cancel"
              :disabled="loading"
            >
              {{ cancelText }}
            </button>
            <button
              @click="handleConfirm"
              class="confirm-btn btn-confirm"
              :class="`btn-${type}`"
              :disabled="loading"
            >
              {{ loading ? '处理中...' : confirmText }}
            </button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const props = defineProps({
  title: {
    type: String,
    default: '确认操作'
  },
  message: {
    type: String,
    required: true
  },
  type: {
    type: String,
    default: 'warning',
    validator: (value) => ['warning', 'danger', 'info'].includes(value)
  },
  confirmText: {
    type: String,
    default: '确定'
  },
  cancelText: {
    type: String,
    default: '取消'
  }
})

const emit = defineEmits(['confirm', 'cancel', 'close'])

const visible = ref(false)
const loading = ref(false)

onMounted(() => {
  visible.value = true
})

// 确认方法
const handleConfirm = () => {
  loading.value = true
  emit('confirm')
}

// 取消方法
const handleCancel = () => {
  // 如果已经正在加载则拒绝取消操作
  if (loading.value) return
  // 触发取消动画并设置定时器在动画完成后发生取消、关闭事件
  visible.value = false
  setTimeout(() => {
    emit('cancel')
    emit('close')
  }, 300)
}

// 暴露方法供外部调用 （直接关闭方法）
const close = () => {
  visible.value = false
  setTimeout(() => {
    emit('close')
  }, 300)
}

defineExpose({
  close
})
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
  padding: 1rem;
}

.confirm-dialog {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* 图标样式 */
.confirm-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.confirm-icon svg {
  width: 36px;
  height: 36px;
}

.icon-warning {
  background-color: rgba(245, 158, 11, 0.1);
  color: #f59e0b;
}

.icon-danger {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.icon-info {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

/* 标题 */
.confirm-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 1rem 0;
}

/* 消息 */
.confirm-message {
  font-size: 1rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

/* 按钮组 */
.confirm-actions {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.confirm-btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.confirm-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
}

.btn-cancel:hover:not(:disabled) {
  background-color: var(--color-gray-100);
}

.btn-confirm {
  color: var(--color-text-light);
}

.btn-confirm.btn-warning {
  background-color: #f59e0b;
}

.btn-confirm.btn-warning:hover:not(:disabled) {
  background-color: #d97706;
}

.btn-confirm.btn-danger {
  background-color: #ef4444;
}

.btn-confirm.btn-danger:hover:not(:disabled) {
  background-color: #dc2626;
}

.btn-confirm.btn-info {
  background-color: #3b82f6;
}

.btn-confirm.btn-info:hover:not(:disabled) {
  background-color: #2563eb;
}

/* 动画 */
.confirm-fade-enter-active {
  animation: confirm-overlay-in 0.3s ease-out;
}

.confirm-fade-leave-active {
  animation: confirm-overlay-out 0.3s ease-in;
}

.confirm-fade-enter-active .confirm-dialog {
  animation: confirm-dialog-in 0.3s ease-out;
}

.confirm-fade-leave-active .confirm-dialog {
  animation: confirm-dialog-out 0.3s ease-in;
}

@keyframes confirm-overlay-in {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes confirm-overlay-out {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
  }
}

@keyframes confirm-dialog-in {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

@keyframes confirm-dialog-out {
  from {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
  to {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .confirm-dialog {
    max-width: calc(100vw - 2rem);
    padding: 1.5rem;
  }

  .confirm-title {
    font-size: 1.25rem;
  }

  .confirm-message {
    font-size: 0.9375rem;
  }

  .confirm-actions {
    flex-direction: column-reverse;
  }

  .confirm-btn {
    width: 100%;
  }
}
</style>
