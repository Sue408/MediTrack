<template>
  <transition name="modal">
    <div v-if="visible" class="modal-overlay" @click.self="handleClose">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="modal-title">{{ isEditing ? '编辑药物' : '添加药物' }}</h2>
          <button @click="handleClose" class="close-btn">×</button>
        </div>

        <form @submit.prevent="handleSubmit" class="modal-body">
          <div class="form-group">
            <label class="form-label">药物名称 <span class="required">*</span></label>
            <input
              v-model="formData.name"
              type="text"
              class="form-input"
              placeholder="请输入药物名称"
              required
            />
          </div>

          <div class="form-group">
            <label class="form-label">剂量</label>
            <input
              v-model="formData.dosage"
              type="text"
              class="form-input"
              placeholder="如：500mg"
            />
          </div>

          <!-- 频率类型选择 -->
          <div class="form-group">
            <label class="form-label">服用频率类型 <span class="required">*</span></label>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  v-model="formData.frequency_type"
                  type="radio"
                  value="daily"
                  class="radio-input"
                  required
                />
                <span>每天</span>
              </label>
              <label class="radio-label">
                <input
                  v-model="formData.frequency_type"
                  type="radio"
                  value="weekly"
                  class="radio-input"
                  required
                />
                <span>每周</span>
              </label>
            </div>
          </div>

          <!-- 每日频率设置 -->
          <div v-if="formData.frequency_type === 'daily'" class="frequency-section">
            <div class="form-group">
              <label class="form-label">每日服用次数 <span class="required">*</span></label>
              <input
                v-model.number="formData.times_per_day"
                type="number"
                min="1"
                max="10"
                class="form-input"
                placeholder="如：3"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">具体服用时间 <span class="required">*</span></label>
              <div class="time-inputs">
                <div
                  v-for="(time, index) in formData.daily_times"
                  :key="index"
                  class="time-input-row"
                >
                  <input
                    v-model="formData.daily_times[index]"
                    type="time"
                    class="form-input time-input"
                    required
                  />
                  <button
                    v-if="formData.daily_times.length > 1"
                    type="button"
                    @click="removeTime(index)"
                    class="remove-time-btn"
                    title="删除此时间"
                  >
                    ×
                  </button>
                </div>
              </div>
              <button
                v-if="formData.daily_times.length < 10"
                type="button"
                @click="addTime"
                class="add-time-btn"
              >
                + 添加时间
              </button>
            </div>
          </div>

          <!-- 每周频率设置 -->
          <div v-if="formData.frequency_type === 'weekly'" class="frequency-section">
            <div class="form-group">
              <label class="form-label">服用日期 <span class="required">*</span></label>
              <div class="weekday-selector">
                <label
                  v-for="day in weekdays"
                  :key="day.value"
                  class="weekday-label"
                  :class="{ active: formData.weekly_days.includes(day.value) }"
                >
                  <input
                    v-model="formData.weekly_days"
                    type="checkbox"
                    :value="day.value"
                    class="weekday-checkbox"
                  />
                  <span class="weekday-text">{{ day.label }}</span>
                </label>
              </div>
              <p v-if="formData.weekly_days.length === 0" class="field-hint error">
                请至少选择一天
              </p>
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">开始日期 <span class="required">*</span></label>
              <input
                v-model="formData.start_date"
                type="date"
                class="form-input"
                required
              />
            </div>

            <div class="form-group">
              <label class="form-label">结束日期 <span class="required">*</span></label>
              <input
                v-model="formData.end_date"
                type="date"
                class="form-input"
              />
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">备注</label>
            <textarea
              v-model="formData.notes"
              class="form-textarea"
              placeholder="请输入备注信息"
              rows="3"
            ></textarea>
          </div>

          <div v-if="isEditing" class="form-group">
            <label class="form-label">状态</label>
            <div class="radio-group">
              <label class="radio-label">
                <input
                  v-model="formData.is_active"
                  type="radio"
                  :value="1"
                  class="radio-input"
                />
                <span>使用中</span>
              </label>
              <label class="radio-label">
                <input
                  v-model="formData.is_active"
                  type="radio"
                  :value="0"
                  class="radio-input"
                />
                <span>已停用</span>
              </label>
            </div>
          </div>

          <!-- 药品照片上传 -->
          <div class="form-group">
            <label class="form-label">药品照片</label>
            <PhotoUploader v-model="formPhotos" :max-photos="3" />
          </div>

          <div class="modal-footer">
            <button type="button" @click="handleClose" class="btn btn-secondary">
              取消
            </button>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? '提交中...' : '确定' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import PhotoUploader from '@/assets/PhotoUploader.vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  medication: {
    type: Object,
    default: null
  },
  isSubmitting: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'submit', 'close'])

// 星期选项
const weekdays = [
  { label: '周一', value: 1 },
  { label: '周二', value: 2 },
  { label: '周三', value: 3 },
  { label: '周四', value: 4 },
  { label: '周五', value: 5 },
  { label: '周六', value: 6 },
  { label: '周日', value: 7 }
]

const isEditing = ref(false)
const formData = ref({
  name: '',
  dosage: '',
  frequency_type: 'daily',
  times_per_day: 1,
  daily_times: ['08:00'],
  weekly_days: [],
  start_date: '',
  end_date: '',
  notes: '',
  is_active: 1
})
const formPhotos = ref([])

// 重置表单
const resetForm = () => {
  formData.value = {
    name: '',
    dosage: '',
    frequency_type: 'daily',
    times_per_day: 1,
    daily_times: ['08:00'],
    weekly_days: [],
    start_date: '',
    end_date: '',
    notes: '',
    is_active: 1
  }
  formPhotos.value = []
}

// 添加时间
const addTime = () => {
  if (formData.value.daily_times.length < 10) {
    formData.value.daily_times.push('08:00')
  }
}

// 删除时间
const removeTime = (index) => {
  if (formData.value.daily_times.length > 1) {
    formData.value.daily_times.splice(index, 1)
  }
}

// 监听 times_per_day 变化，自动调整 daily_times 数组长度
watch(() => formData.value.times_per_day, (newVal) => {
  if (formData.value.frequency_type === 'daily' && newVal) {
    const currentLength = formData.value.daily_times.length
    if (newVal > currentLength) {
      // 增加时间项
      for (let i = currentLength; i < newVal; i++) {
        formData.value.daily_times.push('08:00')
      }
    } else if (newVal < currentLength) {
      // 减少时间项
      formData.value.daily_times = formData.value.daily_times.slice(0, newVal)
    }
  }
})

// 监听 visible 和 medication 变化，初始化表单
watch([() => props.visible, () => props.medication], ([newVisible, newMedication]) => {
  if (newVisible) {
    if (newMedication) {
      isEditing.value = true
      formData.value = {
        name: newMedication.name || '',
        dosage: newMedication.dosage || '',
        frequency_type: newMedication.frequency_type || 'daily',
        times_per_day: newMedication.times_per_day || 1,
        daily_times: newMedication.daily_times || ['08:00'],
        weekly_days: newMedication.weekly_days || [],
        start_date: newMedication.start_date || '',
        end_date: newMedication.end_date || '',
        notes: newMedication.notes || '',
        is_active: newMedication.is_active ?? 1
      }
      // 解析照片
      if (newMedication.photos) {
        try {
          formPhotos.value = JSON.parse(newMedication.photos)
        } catch {
          formPhotos.value = []
        }
      } else {
        formPhotos.value = []
      }
    } else {
      isEditing.value = false
      resetForm()
    }
  }
})

// 关闭弹窗
const handleClose = () => {
  emit('update:visible', false)
  emit('close')
}

// 提交表单
const handleSubmit = () => {
  // 验证每周类型至少选择一天
  if (formData.value.frequency_type === 'weekly' && formData.value.weekly_days.length === 0) {
    return
  }

  const submitData = {
    name: formData.value.name,
    frequency_type: formData.value.frequency_type,
    start_date: formData.value.start_date
  }

  if (formData.value.dosage) submitData.dosage = formData.value.dosage
  if (formData.value.end_date) submitData.end_date = formData.value.end_date
  if (formData.value.notes) submitData.notes = formData.value.notes
  if (isEditing.value) submitData.is_active = formData.value.is_active

  // 根据频率类型添加相应字段
  if (formData.value.frequency_type === 'daily') {
    submitData.times_per_day = formData.value.times_per_day
    submitData.daily_times = formData.value.daily_times
  } else if (formData.value.frequency_type === 'weekly') {
    submitData.weekly_days = formData.value.weekly_days
  }

  // 添加照片数据
  if (isEditing.value) {
    submitData.photos = formPhotos.value.length > 0 ? JSON.stringify(formPhotos.value) : null
  } else {
    if (formPhotos.value.length > 0) {
      submitData.photos = JSON.stringify(formPhotos.value)
    }
  }

  emit('submit', submitData, isEditing.value)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  width: 100%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
}

/* 自定义滚动条样式 - Webkit浏览器 (Chrome, Safari, Edge) */
.modal-content::-webkit-scrollbar {
  width: 8px;
}

.modal-content::-webkit-scrollbar-track {
  background: transparent;
  border-radius: 4px;
}

.modal-content::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.modal-content::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.3);
}

/* 自定义滚动条样式 - Firefox */
.modal-content {
  scrollbar-width: thin;
  scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border-light);
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.close-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  font-size: 2rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  border-radius: 6px;
  transition: all var(--transition-base);
}

.close-btn:hover {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-label {
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.required {
  color: var(--color-error);
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  transition: all var(--transition-base);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.radio-group {
  display: flex;
  gap: 1.5rem;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  color: var(--color-text-primary);
}

.radio-input {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.btn-secondary {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
}

.btn-secondary:hover {
  background-color: var(--color-gray-100);
}

.btn-primary {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.btn-primary:hover:not(:disabled) {
  background-color: var(--color-gray-800);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 弹窗动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9);
}

/* 频率设置区域 */
.frequency-section {
  background-color: var(--color-gray-50);
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.time-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.time-input-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.time-input {
  flex: 1;
}

.remove-time-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-error);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all var(--transition-base);
  flex-shrink: 0;
}

.remove-time-btn:hover {
  background-color: #c53030;
}

.add-time-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--color-bg-primary);
  border: 1px dashed var(--color-border-light);
  border-radius: 6px;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all var(--transition-base);
}

.add-time-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background-color: var(--color-gray-50);
}

/* 星期选择器 */
.weekday-selector {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.weekday-label {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem 0.5rem;
  background-color: var(--color-bg-primary);
  border: 2px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-base);
  user-select: none;
}

.weekday-label:hover {
  border-color: var(--color-gray-400);
  background-color: var(--color-gray-50);
}

.weekday-label.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: white;
}

.weekday-checkbox {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.weekday-text {
  font-size: 0.875rem;
  font-weight: 600;
}

.field-hint {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.field-hint.error {
  color: var(--color-error);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-height: 95vh;
  }

  .weekday-selector {
    grid-template-columns: repeat(4, 1fr);
  }

  .weekday-text {
    font-size: 0.75rem;
  }
}
</style>
