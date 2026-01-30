<template>
  <div class="medication-card" :class="{ inactive: !medication.is_active }">
    <!-- 卡片头部 -->
    <div class="card-header">
      <div class="title-section">
        <h3 class="medication-name">{{ medication.name }}</h3>
        <span v-if="medication.data_source === 'api'" class="verified-badge" title="来自专业药物数据库">
          已验证
        </span>
      </div>
      <div class="action-buttons">
        <button @click="$emit('edit', medication)" class="action-btn" title="编辑">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </button>
        <button @click="$emit('delete', medication)" class="action-btn delete" title="删除">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"></polyline>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- 药物图片 -->
    <div v-if="displayImage" class="card-image">
      <img :src="displayImage" :alt="medication.name" @click="$emit('view-photo', displayImage)" />
    </div>

    <!-- 用户上传的照片 -->
    <div v-else-if="photos.length > 0" class="card-photos">
      <img
        v-for="(photo, index) in photos.slice(0, 3)"
        :key="index"
        :src="photo"
        :alt="`照片${index + 1}`"
        @click="$emit('view-photo', photo)"
      />
      <div v-if="photos.length > 3" class="more-photos">
        +{{ photos.length - 3 }}
      </div>
    </div>

    <!-- 药物信息 -->
    <div class="card-body">
      <!-- 处方药标识 -->
      <div v-if="medication.is_prescription !== null" class="info-badge">
        <span :class="['badge', medication.is_prescription === 1 ? 'prescription' : 'otc']">
          {{ medication.is_prescription === 1 ? '处方药' : '非处方药' }}
        </span>
      </div>

      <!-- 基本信息 -->
      <div class="info-list">
        <div v-if="medication.dosage" class="info-item">
          <span class="label">剂量</span>
          <span class="value">{{ medication.dosage }}</span>
        </div>
        <div v-if="medication.frequency" class="info-item">
          <span class="label">频率</span>
          <span class="value">{{ medication.frequency }}</span>
        </div>
        <div class="info-item">
          <span class="label">开始</span>
          <span class="value">{{ formatDate(medication.start_date) }}</span>
        </div>
        <div v-if="medication.end_date" class="info-item">
          <span class="label">结束</span>
          <span class="value">{{ formatDate(medication.end_date) }}</span>
        </div>
      </div>

      <!-- 疗程进度 -->
      <div v-if="medication.end_date && progress.percentage >= 0" class="progress-section">
        <div class="progress-header">
          <span class="progress-label">疗程进度</span>
          <span class="progress-text" :class="progress.status">{{ progress.text }}</span>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :class="progress.status" :style="{ width: progress.percentage + '%' }"></div>
        </div>
      </div>

      <!-- 备注 -->
      <div v-if="medication.notes" class="notes">
        <span class="label">备注</span>
        <p class="notes-text">{{ medication.notes }}</p>
      </div>
    </div>

    <!-- 卡片底部 -->
    <div class="card-footer">
      <span class="status-badge" :class="medication.is_active ? 'active' : 'inactive'">
        {{ medication.is_active ? '使用中' : '已停用' }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  medication: {
    type: Object,
    required: true
  }
})

defineEmits(['edit', 'delete', 'view-photo'])

// 显示图片（优先官方图片）
const displayImage = computed(() => {
  return props.medication.drug_image_url || null
})

// 用户上传的照片
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
  let status = 'normal'

  if (remainingDays < 0) {
    text = '已完成'
    status = 'completed'
  } else if (remainingDays === 0) {
    text = '今天结束'
    status = 'warning'
  } else if (remainingDays <= 3) {
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
  }).replace(/\//g, '-')
}
</script>

<style scoped>
.medication-card {
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all var(--transition-base);
}

.medication-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--color-gray-300);
}

.medication-card.inactive {
  opacity: 0.6;
}

/* 卡片头部 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border-light);
}

.title-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.medication-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.verified-badge {
  display: inline-block;
  padding: 0.125rem 0.5rem;
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
  border-radius: 4px;
  font-size: 0.6875rem;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  background-color: var(--color-bg-primary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.action-btn:hover {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-light);
}

.action-btn.delete:hover {
  background-color: var(--color-error);
  border-color: var(--color-error);
}

/* 药物图片 */
.card-image {
  margin-bottom: 1rem;
  text-align: center;
  border-radius: 8px;
  overflow: hidden;
  background-color: var(--color-bg-secondary);
}

.card-image img {
  max-width: 100%;
  max-height: 180px;
  cursor: pointer;
  transition: transform var(--transition-base);
}

.card-image img:hover {
  transform: scale(1.05);
}

/* 用户照片 */
.card-photos {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.card-photos img {
  width: 70px;
  height: 70px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--color-border-light);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.card-photos img:hover {
  transform: scale(1.05);
  border-color: var(--color-primary);
}

.more-photos {
  width: 70px;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
}

/* 卡片主体 */
.card-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-badge {
  display: flex;
  gap: 0.5rem;
}

.badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.badge.otc {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.badge.prescription {
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
}

.info-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.75rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item .label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item .value {
  font-size: 0.875rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

/* 进度条 */
.progress-section {
  padding: 0.75rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.progress-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.progress-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.progress-text.normal {
  color: var(--color-text-primary);
}

.progress-text.warning {
  color: var(--color-warning);
}

.progress-text.completed {
  color: var(--color-success);
}

.progress-bar {
  height: 6px;
  background-color: var(--color-gray-200);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  transition: width var(--transition-base);
}

.progress-fill.normal {
  background-color: var(--color-primary);
}

.progress-fill.warning {
  background-color: var(--color-warning);
}

.progress-fill.completed {
  background-color: var(--color-success);
}

/* 备注 */
.notes {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.notes .label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.notes-text {
  font-size: 0.875rem;
  color: var(--color-text-primary);
  line-height: 1.5;
  margin: 0;
}

/* 卡片底部 */
.card-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border-light);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.active {
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
}

.status-badge.inactive {
  background-color: var(--color-gray-200);
  color: var(--color-text-secondary);
}
</style>
