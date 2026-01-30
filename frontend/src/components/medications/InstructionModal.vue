<template>
  <div class="instruction-modal" v-if="visible" @click.self="handleClose">
    <div class="modal-content">
      <div class="modal-header">
        <h3>药品说明书</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </div>

      <div class="modal-body">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>正在加载说明书...</p>
        </div>

        <!-- 说明书内容 -->
        <div v-else-if="instruction" class="instruction-content">
          <div v-for="(value, key) in instruction" :key="key" class="instruction-section">
            <h4 class="section-title">{{ key }}</h4>
            <p class="section-content">{{ value }}</p>
          </div>
        </div>

        <!-- 错误提示 -->
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
        </div>
      </div>

      <div class="modal-footer">
        <button class="close-footer-btn" @click="handleClose">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { getInstructionManual } from '@/api/thirdParty'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  externalDrugId: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['close'])

const loading = ref(false)
const instruction = ref(null)
const error = ref('')

// 监听 visible 变化，加载说明书
watch(() => props.visible, (newVal) => {
  if (newVal && props.externalDrugId) {
    loadInstruction()
  } else {
    // 关闭时清空数据
    instruction.value = null
    error.value = ''
  }
})

// 加载说明书
const loadInstruction = async () => {
  loading.value = true
  error.value = ''
  instruction.value = null

  try {
    const response = await getInstructionManual(props.externalDrugId)
    instruction.value = response.data?.instruction_manual || response.instruction_manual
  } catch (err) {
    console.error('加载说明书失败:', err)
    error.value = err.response?.data?.detail || '加载说明书失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

const handleClose = () => {
  emit('close')
}
</script>

<style scoped>
.instruction-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 700px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  width: 32px;
  height: 32px;
  border: none;
  background: #f5f5f5;
  border-radius: 50%;
  font-size: 24px;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  background: #e0e0e0;
  color: #333;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.loading-state {
  text-align: center;
  padding: 40px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 16px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4CAF50;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.instruction-content {
  line-height: 1.6;
}

.instruction-section {
  margin-bottom: 24px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #4CAF50;
}

.section-content {
  font-size: 14px;
  color: #555;
  margin: 0;
  white-space: pre-wrap;
}

.error-state {
  text-align: center;
  padding: 40px 20px;
  color: #f44336;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  text-align: right;
}

.close-footer-btn {
  padding: 10px 24px;
  background: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.close-footer-btn:hover {
  background: #e0e0e0;
}
</style>
