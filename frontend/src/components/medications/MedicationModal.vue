<template>
  <transition name="modal">
    <div v-if="visible" class="modal-overlay" @click.self="handleClose">
      <div class="modal-container">
        <!-- 弹窗头部 -->
        <div class="modal-header">
          <div class="header-left">
            <h2 class="modal-title">{{ modalTitle }}</h2>
            <!-- 步骤指示器（仅添加模式显示） -->
            <div v-if="!isEditing" class="step-indicator">
              <span class="step" :class="{ active: currentStep === 1 }">1. 选择药物</span>
              <span class="step-divider">→</span>
              <span class="step" :class="{ active: currentStep === 2 }">2. 确认信息</span>
              <span class="step-divider">→</span>
              <span class="step" :class="{ active: currentStep === 3 }">3. 设置信息</span>
            </div>
          </div>
          <button @click="handleClose" class="close-btn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- 弹窗内容 -->
        <div class="modal-body">
          <!-- 步骤1：搜索药物（仅添加模式） -->
          <div v-if="!isEditing && currentStep === 1" class="step-content">
            <DrugSearch
              ref="drugSearchRef"
              @select="handleDrugSelect"
              @manual-entry="handleManualEntry"
            />
          </div>

          <!-- 步骤2：确认药物信息（仅添加模式） -->
          <div v-if="!isEditing && currentStep === 2" class="step-content">
            <DrugDetail
              :drug="selectedDrug"
              @back="handleBackToSearch"
              @confirm="handleDrugConfirm"
              @view-instruction="handleViewInstruction"
            />
          </div>

          <!-- 步骤3：设置使用信息 / 编辑模式 -->
          <div v-if="isEditing || currentStep === 3" class="step-content">
            <!-- 已选药物信息展示 -->
            <div v-if="selectedDrug && !isEditing" class="selected-drug-info">
              <div class="drug-summary">
                <img v-if="selectedDrug.drug_image_url" :src="selectedDrug.drug_image_url" alt="药品图片" class="drug-thumb" />
                <div class="drug-text">
                  <h4>{{ selectedDrug.name }}</h4>
                  <p>{{ selectedDrug.specification }}</p>
                </div>
                <button type="button" @click="handleChangeDrug" class="change-drug-btn">
                  更换药物
                </button>
              </div>
              <!-- 查看说明书按钮（仅非处方药） -->
              <button
                v-if="selectedDrug.is_prescription === 0"
                type="button"
                @click="handleViewInstruction"
                class="view-instruction-btn"
              >
                查看说明书
              </button>
            </div>

            <!-- 使用信息表单 -->
            <form @submit.prevent="handleSubmit" class="medication-form">
              <!-- 手动录入模式：显示药物名称输入 -->
              <div v-if="isManualMode || isEditing" class="form-section">
                <h3 class="section-title">基本信息</h3>
                <div class="form-group">
                  <label class="form-label required">药物名称</label>
                  <input
                    v-model="formData.name"
                    type="text"
                    class="form-input"
                    :class="{ 'input-disabled': !canEditBasicInfo }"
                    :disabled="!canEditBasicInfo"
                    placeholder="请输入药物名称"
                    required
                  />
                  <p v-if="!canEditBasicInfo" class="field-hint">
                    此药物来自权威数据库，基本信息不可修改
                  </p>
                </div>
              </div>

              <!-- 用药信息 -->
              <div class="form-section">
                <h3 class="section-title">用药信息</h3>
                <div class="form-group">
                  <label class="form-label">剂量</label>
                  <input
                    v-model="formData.dosage"
                    type="text"
                    class="form-input"
                    placeholder="如：500mg"
                  />
                </div>
              </div>

              <!-- 服用频率设置 -->
              <div class="form-section">
                <h3 class="section-title">服用频率</h3>
                <FrequencySettings v-model="frequencyData" />
              </div>

              <!-- 用药时间 -->
              <div class="form-section">
                <h3 class="section-title">用药时间</h3>
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label required">开始日期</label>
                    <input
                      v-model="formData.start_date"
                      type="date"
                      class="form-input"
                      required
                    />
                  </div>
                  <div class="form-group">
                    <label class="form-label required">结束日期</label>
                    <input
                      v-model="formData.end_date"
                      type="date"
                      class="form-input"
                      :min="formData.start_date"
                      required
                    />
                  </div>
                </div>
              </div>

              <!-- 备注 -->
              <div class="form-section">
                <h3 class="section-title">备注信息</h3>
                <div class="form-group">
                  <label class="form-label">备注</label>
                  <textarea
                    v-model="formData.notes"
                    class="form-textarea"
                    placeholder="添加备注信息..."
                    rows="3"
                  ></textarea>
                </div>
              </div>

              <!-- 状态 -->
              <div class="form-section">
                <div class="form-group">
                  <label class="checkbox-label">
                    <input
                      v-model="formData.is_active"
                      type="checkbox"
                      class="form-checkbox"
                      :true-value="1"
                      :false-value="0"
                    />
                    <span>当前使用中</span>
                  </label>
                </div>
              </div>

              <!-- 照片上传 -->
              <div class="form-section">
                <h3 class="section-title">药物照片</h3>
                <div class="photo-upload">
                  <div v-if="formPhotos.length > 0" class="photo-preview">
                    <div v-for="(photo, index) in formPhotos" :key="index" class="photo-item">
                      <img :src="photo" :alt="`照片${index + 1}`" />
                      <button type="button" @click="removePhoto(index)" class="remove-photo-btn">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <label v-if="formPhotos.length < 5" class="upload-btn">
                    <input
                      type="file"
                      accept="image/*"
                      @change="handlePhotoUpload"
                      class="file-input"
                    />
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                      <circle cx="8.5" cy="8.5" r="1.5"></circle>
                      <polyline points="21 15 16 10 5 21"></polyline>
                    </svg>
                    <span>添加照片</span>
                  </label>
                </div>
              </div>
            </form>
          </div>
        </div>

        <!-- 弹窗底部 -->
        <div class="modal-footer">
          <button type="button" @click="handleClose" class="btn btn-secondary">
            取消
          </button>
          <button
            v-if="currentStep === 3 || isEditing"
            type="button"
            @click="handleSubmit"
            class="btn btn-primary"
            :disabled="!isFormValid"
          >
            {{ isEditing ? '保存' : '添加' }}
          </button>
        </div>
      </div>
    </div>
  </transition>

  <!-- 说明书弹窗 -->
  <InstructionModal
    :visible="showInstructionModal"
    :external-drug-id="currentInstructionDrugId"
    @close="showInstructionModal = false"
  />
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import DrugSearch from './DrugSearch.vue'
import DrugDetail from './DrugDetail.vue'
import FrequencySettings from './FrequencySettings.vue'
import InstructionModal from '@/components/medications/InstructionModal.vue'
import { createMedication, updateMedication } from '@/api/medication'
import toast from '@/utils/toast'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  medication: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'success'])

// 步骤控制
const currentStep = ref(1)
const isManualMode = ref(false)
const selectedDrug = ref(null)

// 说明书弹窗
const showInstructionModal = ref(false)
const currentInstructionDrugId = ref('')

// 引用
const drugSearchRef = ref(null)

// 是否为编辑模式
const isEditing = computed(() => !!props.medication)

// 弹窗标题
const modalTitle = computed(() => {
  if (isEditing.value) return '编辑药物'
  if (currentStep.value === 1) return '添加药物 - 选择药物'
  if (currentStep.value === 2) return '添加药物 - 确认信息'
  return '添加药物 - 设置信息'
})

// 表单数据
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
  is_active: 1,
  // 外部药物数据库字段
  drug_code: null,
  manufacturer: null,
  specification: null,
  dosage_form: null,
  is_prescription: null,
  drug_image_url: null,
  instruction_manual: null,
  approval_number: null,
  generic_name: null,
  trade_name: null,
  data_source: 'manual',
  external_drug_id: null
})

const formPhotos = ref([])

// 表单验证
const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' &&
         formData.value.start_date !== '' &&
         formData.value.end_date !== ''
})

// 是否可以编辑基本信息（来自数据库的药物不允许编辑基本信息）
const canEditBasicInfo = computed(() => {
  if (!isEditing.value) return true
  return formData.value.data_source === 'manual'
})

// 频率数据（用于 FrequencySettings 组件的双向绑定）
const frequencyData = computed({
  get: () => ({
    frequency_type: formData.value.frequency_type,
    times_per_day: formData.value.times_per_day,
    daily_times: formData.value.daily_times,
    weekly_days: formData.value.weekly_days
  }),
  set: (value) => {
    formData.value.frequency_type = value.frequency_type
    formData.value.times_per_day = value.times_per_day
    formData.value.daily_times = value.daily_times
    formData.value.weekly_days = value.weekly_days
  }
})

// 监听弹窗显示状态
watch(() => props.visible, (newVal) => {
  if (newVal) {
    if (props.medication) {
      loadMedicationData()
    } else {
      resetForm()
      currentStep.value = 1
      isManualMode.value = false
      selectedDrug.value = null
    }
  }
})

// 重置表单
const resetForm = () => {
  formData.value = {
    name: '',
    dosage: '',
    frequency_type: 'daily',
    times_per_day: 1,
    daily_times: ['08:00'],
    weekly_days: [],
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    notes: '',
    is_active: 1,
    drug_code: null,
    manufacturer: null,
    specification: null,
    dosage_form: null,
    is_prescription: null,
    drug_image_url: null,
    instruction_manual: null,
    approval_number: null,
    generic_name: null,
    trade_name: null,
    data_source: 'manual',
    external_drug_id: null
  }
  formPhotos.value = []
}

// 加载药物数据（编辑模式）
const loadMedicationData = () => {
  if (props.medication) {
    formData.value = {
      name: props.medication.name || '',
      dosage: props.medication.dosage || '',
      frequency_type: props.medication.frequency_type || 'daily',
      times_per_day: props.medication.times_per_day || 1,
      daily_times: props.medication.daily_times || ['08:00'],
      weekly_days: props.medication.weekly_days || [],
      start_date: props.medication.start_date || '',
      end_date: props.medication.end_date || '',
      notes: props.medication.notes || '',
      is_active: props.medication.is_active ?? 1,
      drug_code: props.medication.drug_code || null,
      manufacturer: props.medication.manufacturer || null,
      specification: props.medication.specification || null,
      dosage_form: props.medication.dosage_form || null,
      is_prescription: props.medication.is_prescription ?? null,
      drug_image_url: props.medication.drug_image_url || null,
      instruction_manual: props.medication.instruction_manual || null,
      approval_number: props.medication.approval_number || null,
      generic_name: props.medication.generic_name || null,
      trade_name: props.medication.trade_name || null,
      data_source: props.medication.data_source || 'manual',
      external_drug_id: props.medication.external_drug_id || null
    }

    // 加载照片
    if (props.medication.photos) {
      try {
        formPhotos.value = JSON.parse(props.medication.photos)
      } catch (e) {
        formPhotos.value = []
      }
    }
  }
}

// 选择药物（从搜索结果）
const handleDrugSelect = (drug) => {
  selectedDrug.value = drug
  isManualMode.value = false
  // 进入步骤2（确认信息）
  currentStep.value = 2
}

// 确认药物选择
const handleDrugConfirm = (drug) => {
  // 填充药物信息到表单
  formData.value.name = drug.name
  // 剂量需要用户手动输入，不使用规格信息
  formData.value.dosage = ''
  formData.value.drug_code = drug.drug_code
  formData.value.manufacturer = drug.manufacturer
  formData.value.specification = drug.specification
  formData.value.dosage_form = drug.dosage_form
  formData.value.is_prescription = drug.is_prescription
  formData.value.drug_image_url = drug.drug_image_url
  formData.value.approval_number = drug.approval_number
  formData.value.generic_name = drug.generic_name
  formData.value.trade_name = drug.trade_name
  formData.value.data_source = 'api'
  formData.value.external_drug_id = drug.external_drug_id

  // 如果有说明书，保存为JSON字符串
  if (drug.instruction_manual) {
    formData.value.instruction_manual = JSON.stringify(drug.instruction_manual)
  }

  // 进入步骤3（设置使用信息）
  currentStep.value = 3
}

// 从确认页面返回搜索
const handleBackToSearch = () => {
  currentStep.value = 1
}

// 手动录入
const handleManualEntry = () => {
  isManualMode.value = true
  selectedDrug.value = null
  formData.value.data_source = 'manual'
  currentStep.value = 3
}

// 更换药物
const handleChangeDrug = () => {
  currentStep.value = 1
  selectedDrug.value = null
  // 清空搜索
  if (drugSearchRef.value) {
    drugSearchRef.value.clearSearch()
  }
}

// 查看说明书
const handleViewInstruction = () => {
  if (selectedDrug.value?.external_drug_id) {
    currentInstructionDrugId.value = selectedDrug.value.external_drug_id
    showInstructionModal.value = true
  }
}

// 处理照片上传
const handlePhotoUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return

  // 检查文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    toast.error('照片大小不能超过5MB')
    return
  }

  // 读取文件并转换为Base64
  const reader = new FileReader()
  reader.onload = (e) => {
    formPhotos.value.push(e.target.result)
  }
  reader.readAsDataURL(file)

  // 重置input
  event.target.value = ''
}

// 删除照片
const removePhoto = (index) => {
  formPhotos.value.splice(index, 1)
}

// 提交表单
const handleSubmit = async () => {
  if (!isFormValid.value) {
    toast.error('请填写必填项')
    return
  }

  try {
    const submitData = {
      ...formData.value,
      photos: formPhotos.value.length > 0 ? JSON.stringify(formPhotos.value) : null
    }

    if (isEditing.value) {
      await updateMedication(props.medication.id, submitData)
      emit('success', true) // 传递 true 表示是编辑操作
    } else {
      await createMedication(submitData)
      emit('success', false) // 传递 false 表示是添加操作
    }

    handleClose()
  } catch (error) {
    console.error('保存药物失败:', error)
    toast.error(error.response?.data?.detail || '保存失败，请稍后重试')
  }
}

// 关闭弹窗
const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
/* 弹窗遮罩 */
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

.modal-container {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  width: 100%;
  max-width: 700px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
}

/* 弹窗头部 */
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border-light);
}

.header-left {
  flex: 1;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
}

.step-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.step {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  transition: all var(--transition-fast);
}

.step.active {
  color: var(--color-primary);
  font-weight: 600;
}

.step-divider {
  color: var(--color-text-secondary);
  font-size: 0.75rem;
}

.close-btn {
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
  flex-shrink: 0;
}

.close-btn svg {
  width: 18px;
  height: 18px;
}

.close-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

/* 弹窗内容 */
.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.step-content {
  min-height: 300px;
}

/* 已选药物信息 */
.selected-drug-info {
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
}

.drug-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.drug-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  border: 1px solid var(--color-border-light);
}

.drug-text {
  flex: 1;
  min-width: 0;
}

.drug-text h4 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.25rem 0;
}

.drug-text p {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

.change-drug-btn {
  padding: 0.5rem 1rem;
  background-color: var(--color-bg-primary);
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.change-drug-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

.view-instruction-btn {
  width: 100%;
  padding: 0.625rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-instruction-btn:hover {
  background-color: var(--color-gray-800);
}

/* 表单 */
.medication-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-primary);
}

.form-label.required::after {
  content: ' *';
  color: var(--color-error);
}

.form-input,
.form-textarea {
  padding: 0.75rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  transition: all var(--transition-fast);
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.form-input.input-disabled {
  background-color: var(--color-gray-100);
  color: var(--color-text-secondary);
  cursor: not-allowed;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  margin: 0;
  font-style: italic;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
}

.form-checkbox {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

/* 照片上传 */
.photo-upload {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.photo-preview {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.photo-item {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border-light);
}

.photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.remove-photo-btn {
  position: absolute;
  top: 0.25rem;
  right: 0.25rem;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.remove-photo-btn svg {
  width: 14px;
  height: 14px;
}

.remove-photo-btn:hover {
  background-color: var(--color-error);
}

.upload-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100px;
  height: 100px;
  border: 2px dashed var(--color-border-medium);
  border-radius: 8px;
  background-color: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.upload-btn:hover {
  border-color: var(--color-primary);
  background-color: var(--color-gray-100);
  color: var(--color-primary);
}

.upload-btn svg {
  width: 24px;
  height: 24px;
}

.upload-btn span {
  font-size: 0.75rem;
  font-weight: 500;
}

.file-input {
  display: none;
}

/* 弹窗底部 */
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding: 1.5rem;
  border-top: 1px solid var(--color-border-light);
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
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

.btn-primary:hover {
  background-color: var(--color-gray-800);
}

.btn-primary:disabled {
  background-color: var(--color-gray-300);
  color: var(--color-gray-500);
  cursor: not-allowed;
}

/* 动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--transition-base);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform var(--transition-base);
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.95);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .step {
    font-size: 0.72rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .drug-summary {
    flex-wrap: wrap;
  }

  .change-drug-btn {
    width: 100%;
  }
}
</style>
