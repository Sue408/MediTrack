<template>
  <div class="medicines-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div>
        <h1 class="page-title">药物管理</h1>
        <p class="page-subtitle">管理您的药物信息</p>
      </div>
      <button @click="handleAddMedication" class="add-btn">
        <span class="btn-icon">+</span>
        添加药物
      </button>
    </div>

    <!-- 搜索和筛选栏 -->
    <MedicationFilter
      v-model:search-query="searchQuery"
      v-model:filter-status="filterStatus"
      :result-count="filteredMedications.length"
      class="filter-section"
    />

    <!-- 药物列表 -->
    <div v-if="filteredMedications.length > 0" class="medications-grid">
      <MedicationCard
        v-for="medication in filteredMedications"
        :key="medication.id"
        :medication="medication"
        @edit="handleEditMedication"
        @delete="handleDeleteMedication"
        @view-photo="handleViewPhoto"
      />
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg t="1769580221309" class="icon"
         viewBox="0 0 1024 1024" version="1.1"
          xmlns="http://www.w3.org/2000/svg"
           p-id="4912" xmlns:xlink="http://www.w3.org/1999/xlink"
            width="200"
             height="200">
            <path d="M304.128 371.712q-14.336 0-21.504-5.12t-10.24-12.288q-4.096-8.192-4.096-18.432l0-67.584q0-19.456 7.68-29.184t16.896-14.848q11.264-5.12 24.576-5.12l396.288 0q13.312 0 24.576 5.12 9.216 5.12 16.896 14.848t7.68 29.184l0 67.584q0 10.24-4.096 18.432-3.072 7.168-9.728 12.288t-20.992 5.12l-423.936 0zM837.632 943.104q0 22.528-8.192 40.96-7.168 15.36-22.016 27.648t-42.496 12.288l-497.664 0q-28.672 0-43.008-12.288t-21.504-27.648q-8.192-18.432-9.216-40.96l0-382.976q0-33.792 12.288-48.128t22.528-24.576l72.704-67.584 443.392 0 58.368 67.584q10.24 10.24 22.528 24.576t12.288 48.128l0 382.976zM677.888 678.912l-107.52 0 0-108.544-109.568 0 0 108.544-107.52 0 0 109.568 107.52 0 0 107.52 109.568 0 0-107.52 107.52 0 0-109.568z" p-id="4913"></path></svg>
      </div>
      <p class="empty-text">
        {{ searchQuery || filterStatus !== 'all' ? '未找到匹配的药物' : '暂无药物记录' }}
      </p>
      <p class="empty-hint">
        {{ searchQuery || filterStatus !== 'all' ? '尝试调整搜索条件' : '点击右上角"添加药物"按钮开始添加' }}
      </p>
    </div>

    <!-- 添加/编辑药物表单 -->
    <MedicationForm
      v-model:visible="showModal"
      :medication="currentMedication"
      :is-submitting="isSubmitting"
      @submit="handleSubmit"
      @close="handleCloseModal"
    />

    <!-- 照片查看器 -->
    <PhotoViewer
      v-model:visible="showPhotoViewer"
      :photo-url="viewingPhoto"
      @close="handleClosePhotoViewer"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getMedications, createMedication, updateMedication, deleteMedication } from '@/api/medication'
import MedicationFilter from '@/components/MedicationFilter.vue'
import MedicationCard from '@/components/MedicationCard.vue'
import MedicationForm from '@/components/MedicationForm.vue'
import PhotoViewer from '@/assets/PhotoViewer.vue'
import toast from '@/utils/toast'
import confirm from '@/utils/confirm'
const route = useRoute()

// 状态管理
const medications = ref([])
const searchQuery = ref('')
const filterStatus = ref('all')
const showModal = ref(false)
const showPhotoViewer = ref(false)
const viewingPhoto = ref(null)
const currentMedication = ref(null)
const isSubmitting = ref(false)

// 筛选后的药物列表
const filteredMedications = computed(() => {
  let result = medications.value

  // 按搜索关键词筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(med =>
      med.name.toLowerCase().includes(query)
    )
  }

  // 按状态筛选
  if (filterStatus.value !== 'all') {
    const isActive = filterStatus.value === 'active' ? 1 : 0
    result = result.filter(med => med.is_active === isActive)
  }

  return result
})

// 加载药物列表
const loadMedications = async () => {
  try {
    const data = await getMedications()
    medications.value = data
  } catch (error) {
    console.error('加载药物列表失败：', error)
    toast.error('加载药物列表失败')
  }
}

// 打开添加药物弹窗
const handleAddMedication = () => {
  currentMedication.value = null
  showModal.value = true
}

// 打开编辑药物弹窗
const handleEditMedication = (medication) => {
  currentMedication.value = medication
  showModal.value = true
}

// 关闭表单弹窗
const handleCloseModal = () => {
  showModal.value = false
  currentMedication.value = null
}

// 提交表单
const handleSubmit = async (submitData, isEditing) => {
  if (isSubmitting.value) return

  isSubmitting.value = true

  try {
    if (isEditing) {
      await updateMedication(currentMedication.value.id, submitData)
      toast.success('药物更新成功')
    } else {
      await createMedication(submitData)
      toast.success('药物添加成功')
    }

    handleCloseModal()
    await loadMedications()
  } catch (error) {
    console.error('提交失败：', error)
    toast.error(error.response?.data?.detail || '操作失败，请重试')
  } finally {
    isSubmitting.value = false
  }
}

// 删除药物
const handleDeleteMedication = async (medication) => {
  try {
    await confirm.danger(
      `确定要删除药物"${medication.name}"吗？此操作无法撤销。`,
      '删除药物'
    )

    await deleteMedication(medication.id)
    toast.success('药物删除成功')
    await loadMedications()
  } catch (error) {
    if (error.message === '用户取消') return
    console.error('删除失败：', error)
    toast.error(error.response?.data?.detail || '删除失败，请重试')
  }
}

// 查看照片
const handleViewPhoto = (photo) => {
  viewingPhoto.value = photo
  showPhotoViewer.value = true
}

// 关闭照片查看器
const handleClosePhotoViewer = () => {
  showPhotoViewer.value = false
  viewingPhoto.value = null
}

// 页面加载时获取数据
onMounted(async () => {
  await loadMedications()

  // 检查是否有编辑参数
  const editId = route.query?.edit
  if (editId) {
    const medication = medications.value.find(m => m.id === parseInt(editId))
    if (medication) {
      handleEditMedication(medication)
    }
  }
})
</script>

<style scoped>
.medicines-page {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.page-subtitle {
  font-size: 1rem;
  color: var(--color-text-secondary);
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.875rem 1.5rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.add-btn:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.btn-icon {
  font-size: 1.5rem;
  line-height: 1;
}

.filter-section {
  margin-bottom: 2rem;
}

.medications-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

/* 空状态 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
}

.empty-icon {
  transform: scale(0.5);
  color: var(--color-gray-800);
  margin-bottom: 1.5rem;
  opacity: 0.6;
  transition: all var(--transition-base);
}

.empty-state:hover .empty-icon {
  opacity: 0.8;
  transform: scale(0.55);
}

.empty-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.empty-hint {
  font-size: 1rem;
  color: var(--color-text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .medicines-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .add-btn {
    width: 100%;
    justify-content: center;
  }

  .medications-grid {
    grid-template-columns: 1fr;
  }
}
</style>
