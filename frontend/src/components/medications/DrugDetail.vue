<template>
  <div class="drug-detail">
    <!-- 药物图片 -->
    <div v-if="drug.drug_image_url" class="drug-image-section">
      <img :src="drug.drug_image_url" alt="药品图片" class="drug-image" />
    </div>

    <!-- 基本信息 -->
    <div class="info-section">
      <h3 class="section-title">基本信息</h3>
      <div class="info-grid">
        <div class="info-item">
          <label>药品名称</label>
          <span>{{ drug.name }}</span>
        </div>
        <div v-if="drug.generic_name" class="info-item">
          <label>通用名</label>
          <span>{{ drug.generic_name }}</span>
        </div>
        <div v-if="drug.trade_name" class="info-item">
          <label>商品名</label>
          <span>{{ drug.trade_name }}</span>
        </div>
        <div v-if="drug.manufacturer" class="info-item">
          <label>生产厂家</label>
          <span>{{ drug.manufacturer }}</span>
        </div>
        <div v-if="drug.specification" class="info-item">
          <label>包装规格</label>
          <span>{{ drug.specification }}</span>
        </div>
        <div v-if="drug.dosage_form" class="info-item">
          <label>产品剂型</label>
          <span>{{ drug.dosage_form }}</span>
        </div>
        <div class="info-item">
          <label>处方类型</label>
          <span class="prescription-badge" :class="{ prescription: drug.is_prescription === 1 }">
            {{ drug.is_prescription === 1 ? '处方药' : '非处方药' }}
          </span>
        </div>
        <div v-if="drug.approval_number" class="info-item">
          <label>批准文号</label>
          <span>{{ drug.approval_number }}</span>
        </div>
      </div>
    </div>

    <!-- 说明书按钮 -->
    <div class="instruction-section">
      <button
        v-if="drug.is_prescription === 0"
        type="button"
        @click="handleViewInstruction"
        class="view-instruction-btn"
      >
        查看说明书
      </button>
      <p v-else class="prescription-notice">
        处方药不提供说明书信息，请遵医嘱使用
      </p>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <button type="button" @click="$emit('back')" class="btn btn-secondary">
        返回搜索
      </button>
      <button type="button" @click="handleConfirm" class="btn btn-primary">
        确认选择
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  drug: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['back', 'confirm', 'view-instruction'])

const handleConfirm = () => {
  emit('confirm', props.drug)
}

const handleViewInstruction = () => {
  emit('view-instruction', props.drug.external_drug_id)
}
</script>

<style scoped>
.drug-detail {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 药物图片 */
.drug-image-section {
  text-align: center;
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
}

.drug-image {
  max-width: 200px;
  max-height: 200px;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

/* 信息区块 */
.info-section {
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
}

.section-title {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--color-text-primary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--color-primary);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.info-item label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-item span {
  font-size: 0.875rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

.prescription-badge {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

.prescription-badge.prescription {
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
}

/* 说明书区域 */
.instruction-section {
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
}

.view-instruction-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.view-instruction-btn:hover {
  background-color: var(--color-gray-800);
}

.prescription-notice {
  padding: 0.75rem;
  background-color: var(--color-gray-100);
  color: var(--color-text-secondary);
  border-radius: 6px;
  font-size: 0.8125rem;
  text-align: center;
  margin: 0;
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn {
    width: 100%;
  }
}
</style>
