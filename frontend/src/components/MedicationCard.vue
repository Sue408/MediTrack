<template>
  <div class="medication-card" :class="{ 'inactive': !medication.is_active }">
    <div class="card-header">
      <h3 class="medication-name">{{ medication.name }}</h3>
      <div class="card-actions">
        <button @click="$emit('edit', medication)" class="icon-btn edit-btn" title="编辑">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button @click="$emit('delete', medication)" class="icon-btn delete-btn" title="删除">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- 药品照片 -->
    <div v-if="photos.length > 0" class="card-photos">
      <img
        v-for="(photo, index) in photos"
        :key="index"
        :src="photo"
        :alt="`药品照片${index + 1}`"
        class="photo-thumbnail"
        @click="$emit('view-photo', photo)"
      />
    </div>

    <div class="card-body">
      <div v-if="medication.dosage" class="info-row">
        <span class="info-label">剂量：</span>
        <span class="info-value">{{ medication.dosage }}</span>
      </div>
      <div v-if="medication.frequency" class="info-row">
        <span class="info-label">频率：</span>
        <span class="info-value">{{ medication.frequency }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">开始日期：</span>
        <span class="info-value">{{ formatDate(medication.start_date) }}</span>
      </div>
      <div v-if="medication.end_date" class="info-row">
        <span class="info-label">结束日期：</span>
        <span class="info-value">{{ formatDate(medication.end_date) }}</span>
      </div>

      <!-- 疗程进度条 -->
      <div v-if="medication.end_date" class="progress-section">
        <ProgressBar
          :percentage="progress.percentage"
          :text="progress.text"
          :status="progress.status"
          label="疗程进度"
        />
      </div>

      <div v-if="medication.notes" class="info-row notes">
        <span class="info-label">备注：</span>
        <span class="info-value">{{ medication.notes }}</span>
      </div>
    </div>

    <div class="card-footer">
      <span class="status-badge" :class="medication.is_active ? 'active' : 'inactive'">
        {{ medication.is_active ? '使用中' : '已停用' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import ProgressBar from '@/assets/ProgressBar.vue'

const props = defineProps({
  medication: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'delete', 'view-photo'])

// 获取药物照片数组
const photos = computed(() => {
  if (!props.medication.photos) return []
  try {
    return JSON.parse(props.medication.photos)
  } catch {
    return []
  }
})

// 计算疗程进度
const progress = computed(() => {
  if (!props.medication.end_date) return { percentage: 0, text: '', status: 'normal' }

  const now = new Date()
  const start = new Date(props.medication.start_date)
  const end = new Date(props.medication.end_date)

  const total = end - start
  const elapsed = now - start
  const percentage = Math.min(Math.max((elapsed / total) * 100, 0), 100)

  const remainingDays = Math.ceil((end - now) / (1000 * 60 * 60 * 24))

  let text = ''
  let status = ''

  if (remainingDays < 0) {
    text = '已完成'
    status = 'completed'
  } else if (remainingDays === 0) {
    text = '今天结束'
    status = 'ending'
  } else if (remainingDays <= 3) {
    text = `剩余 ${remainingDays} 天`
    status = 'ending'
  } else if (remainingDays <= 7) {
    text = `剩余 ${remainingDays} 天`
    status = 'warning'
  } else {
    text = `剩余 ${remainingDays} 天`
    status = 'normal'
  }

  return { percentage: Math.round(percentage), text, status }
})

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}
</script>

<style scoped>
.medication-card {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
}

.medication-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.medication-card.inactive {
  opacity: 0.7;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--color-border-light);
}

.medication-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.icon-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.icon-btn svg {
  width: 18px;
  height: 18px;
}

.edit-btn {
  background-color: var(--color-gray-100);
  color: var(--color-gray-700);
}

.edit-btn:hover {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.delete-btn {
  background-color: var(--color-gray-100);
  color: var(--color-gray-700);
}

.delete-btn:hover {
  background-color: var(--color-error);
  color: var(--color-text-light);
}

/* 药品照片 */
.card-photos {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.photo-thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-base);
  border: 2px solid var(--color-border-light);
}

.photo-thumbnail:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-md);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.info-row {
  display: flex;
  gap: 0.5rem;
}

.info-row.notes {
  flex-direction: column;
}

.info-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  min-width: 80px;
}

.info-value {
  font-size: 0.875rem;
  color: var(--color-text-primary);
}

.progress-section {
  margin: 0.75rem 0;
  padding: 0.75rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
}

.card-footer {
  display: flex;
  justify-content: flex-end;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.active {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--color-success);
}

.status-badge.inactive {
  background-color: rgba(239, 68, 68, 0.1);
  color: var(--color-error);
}
</style>
