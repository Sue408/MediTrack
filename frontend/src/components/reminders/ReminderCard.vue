<template>
  <div class="reminder-card" :class="{ completed: reminder.is_completed }">
    <div class="card-checkbox">
      <input
        :id="`reminder-${reminder.id}`"
        type="checkbox"
        :checked="reminder.is_completed"
        @change="$emit('toggle', reminder.id)"
        class="checkbox-input"
      />
      <label :for="`reminder-${reminder.id}`" class="checkbox-label">
        <span class="checkbox-box">
          <svg v-if="reminder.is_completed" class="check-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </span>
      </label>
    </div>

    <div class="card-content">
      <div class="card-header">
        <h3 class="medication-name">{{ reminder.medication_name }}</h3>
        <span v-if="reminder.is_completed" class="status-badge completed">已完成</span>
        <span v-else class="status-badge pending">待完成</span>
      </div>

      <div class="card-details">
        <div class="detail-item">
          <svg class="detail-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
          </svg>
          <span class="detail-text">剂量：{{ reminder.dosage }}</span>
        </div>

        <div class="detail-item">
          <svg class="detail-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <span class="detail-text">计划时间：{{ reminder.scheduled_time }}</span>
        </div>

        <div v-if="reminder.is_completed && reminder.completed_at" class="detail-item completed-time">
          <svg class="detail-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span class="detail-text success">完成时间：{{ formatCompletedTime(reminder.completed_at) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  reminder: {
    type: Object,
    required: true
  }
})

defineEmits(['toggle'])

const formatCompletedTime = (datetime) => {
  if (!datetime) return ''
  const date = new Date(datetime)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.reminder-card {
  display: flex;
  gap: 1rem;
  padding: 1.25rem;
  background-color: var(--color-bg-primary);
  border: 2px solid var(--color-border-light);
  border-radius: 12px;
  transition: all var(--transition-base);
  cursor: pointer;
}

.reminder-card:hover {
  border-color: var(--color-gray-300);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.reminder-card.completed {
  background-color: var(--color-bg-secondary);
  border-color: rgba(34, 197, 94, 0.2);
}

.reminder-card.completed:hover {
  border-color: rgba(34, 197, 94, 0.4);
}

/* 复选框样式 */
.card-checkbox {
  flex-shrink: 0;
  padding-top: 0.125rem;
}

.checkbox-input {
  display: none;
}

.checkbox-label {
  display: block;
  cursor: pointer;
}

.checkbox-box {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border: 2.5px solid var(--color-border-light);
  border-radius: 8px;
  background-color: var(--color-bg-primary);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

/* 未选中状态悬停效果 */
.checkbox-input:not(:checked) + .checkbox-label:hover .checkbox-box {
  border-color: var(--color-primary);
  transform: scale(1.05);
  box-shadow: 0 0 0 4px rgba(0, 0, 0, 0.05);
}

/* 选中状态 */
.checkbox-input:checked + .checkbox-label .checkbox-box {
  border-color: #22c55e;
  background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.3);
}

.checkbox-input:checked + .checkbox-label:hover .checkbox-box {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.4);
}

/* 勾选图标 */
.check-icon {
  width: 18px;
  height: 18px;
  color: white;
  stroke-width: 3;
  animation: checkmark 0.4s cubic-bezier(0.65, 0, 0.35, 1);
}

@keyframes checkmark {
  0% {
    transform: scale(0) rotate(-45deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotate(0deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

/* 卡片内容 */
.card-content {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
  flex-wrap: wrap;
}

.medication-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.reminder-card.completed .medication-name {
  color: var(--color-text-secondary);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}

.status-badge.completed {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
  border: 1px solid rgba(34, 197, 94, 0.2);
}

.status-badge.pending {
  background-color: rgba(251, 146, 60, 0.1);
  color: #fb923c;
  border: 1px solid rgba(251, 146, 60, 0.2);
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-item.completed-time {
  padding: 0.5rem;
  background-color: rgba(34, 197, 94, 0.05);
  border-radius: 6px;
  border-left: 3px solid #22c55e;
  margin-top: 0.25rem;
}

.detail-icon {
  width: 16px;
  height: 16px;
  color: var(--color-text-secondary);
  flex-shrink: 0;
}

.detail-item.completed-time .detail-icon {
  color: #22c55e;
}

.detail-text {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-text.success {
  color: #16a34a;
  font-weight: 500;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .reminder-card {
    padding: 1rem;
    gap: 0.875rem;
  }

  .checkbox-box {
    width: 26px;
    height: 26px;
    border-width: 2px;
  }

  .check-icon {
    width: 16px;
    height: 16px;
  }

  .medication-name {
    font-size: 1rem;
  }

  .card-details {
    gap: 0.375rem;
  }

  .detail-text {
    font-size: 0.8125rem;
  }

  .detail-item.completed-time {
    padding: 0.375rem 0.5rem;
  }
}

@media (max-width: 480px) {
  .reminder-card {
    padding: 0.875rem;
  }

  .card-header {
    gap: 0.5rem;
  }

  .medication-name {
    font-size: 0.9375rem;
    width: 100%;
  }

  .status-badge {
    font-size: 0.6875rem;
    padding: 0.1875rem 0.625rem;
  }

  .detail-item {
    gap: 0.375rem;
  }

  .detail-icon {
    width: 14px;
    height: 14px;
  }

  .detail-text {
    font-size: 0.75rem;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .reminder-card {
    -webkit-tap-highlight-color: transparent;
  }

  .checkbox-box {
    width: 32px;
    height: 32px;
  }

  .check-icon {
    width: 20px;
    height: 20px;
  }
}
</style>
