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

          <div class="form-row">
            <div class="form-group">
              <label class="form-label">剂量</label>
              <input
                v-model="formData.dosage"
                type="text"
                class="form-input"
                placeholder="如：500mg"
              />
            </div>

            <div class="form-group">
              <label class="form-label">服用频率</label>
              <input
                v-model="formData.frequency"
                type="text"
                class="form-input"
                placeholder="如：每日3次"
              />
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
              <label class="form-label">结束日期</label>
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

const isEditing = ref(false)
const formData = ref({
  name: '',
  dosage: '',
  frequency: '',
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
    frequency: '',
    start_date: '',
    end_date: '',
    notes: '',
    is_active: 1
  }
  formPhotos.value = []
}

// 监听 visible 和 medication 变化，初始化表单
watch([() => props.visible, () => props.medication], ([newVisible, newMedication]) => {
  if (newVisible) {
    if (newMedication) {
      isEditing.value = true
      formData.value = {
        name: newMedication.name || '',
        dosage: newMedication.dosage || '',
        frequency: newMedication.frequency || '',
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
  const submitData = {
    name: formData.value.name,
    start_date: formData.value.start_date
  }

  if (formData.value.dosage) submitData.dosage = formData.value.dosage
  if (formData.value.frequency) submitData.frequency = formData.value.frequency
  if (formData.value.end_date) submitData.end_date = formData.value.end_date
  if (formData.value.notes) submitData.notes = formData.value.notes
  if (isEditing.value) submitData.is_active = formData.value.is_active

  // 添加照片数据（编辑模式下即使为空也要发送，以支持删除操作）
  if (isEditing.value) {
    // 编辑模式：始终发送 photos 字段，即使为空
    submitData.photos = formPhotos.value.length > 0 ? JSON.stringify(formPhotos.value) : null
  } else {
    // 新增模式：只在有照片时发送
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

/* 响应式设计 */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-height: 95vh;
  }
}
</style>
