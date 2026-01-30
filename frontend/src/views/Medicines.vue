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
    <SearchBar
      v-model:search-query="searchQuery"
      v-model:filter-status="filterStatus"
      :result-count="filteredMedications.length"
      class="filter-section"
    />

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">加载中...</p>
    </div>

    <!-- 药物列表 -->
    <div v-else-if="filteredMedications.length > 0" class="medications-grid">
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
        <svg class="icon"
         viewBox="0 0 1024 1024"
          xmlns="http://www.w3.org/2000/svg"
            width="200"
             height="200">
            <path d="M304.128 371.712q-14.336 0-21.504-5.12t-10.24-12.288q-4.096-8.192-4.096-18.432l0-67.584q0-19.456 7.68-29.184t16.896-14.848q11.264-5.12 24.576-5.12l396.288 0q13.312 0 24.576 5.12 9.216 5.12 16.896 14.848t7.68 29.184l0 67.584q0 10.24-4.096 18.432-3.072 7.168-9.728 12.288t-20.992 5.12l-423.936 0zM837.632 943.104q0 22.528-8.192 40.96-7.168 15.36-22.016 27.648t-42.496 12.288l-497.664 0q-28.672 0-43.008-12.288t-21.504-27.648q-8.192-18.432-9.216-40.96l0-382.976q0-33.792 12.288-48.128t22.528-24.576l72.704-67.584 443.392 0 58.368 67.584q10.24 10.24 22.528 24.576t12.288 48.128l0 382.976zM677.888 678.912l-107.52 0 0-108.544-109.568 0 0 108.544-107.52 0 0 109.568 107.52 0 0 107.52 109.568 0 0-107.52 107.52 0 0-109.568z"></path></svg>
      </div>
      <p class="empty-text">
        {{ searchQuery || filterStatus !== 'all' ? '未找到匹配的药物' : '暂无药物记录' }}
      </p>
      <p class="empty-hint">
        {{ searchQuery || filterStatus !== 'all' ? '尝试调整搜索条件' : '点击右上角"添加药物"按钮开始添加' }}
      </p>
    </div>

    <!-- 添加/编辑药物弹窗 -->
    <MedicationModal
      :visible="showModal"
      :medication="currentMedication"
      @close="handleCloseModal"
      @success="handleFormSuccess"
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
import { getMedications, deleteMedication } from '@/api/medication'
import SearchBar from '@/components/medications/SearchBar.vue'
import MedicationCard from '@/components/medications/MedicationCard.vue'
import MedicationModal from '@/components/medications/MedicationModal.vue'
import PhotoViewer from '@/assets/PhotoViewer.vue'
import toast from '@/utils/toast'
import confirm from '@/utils/confirm'
const route = useRoute()

// 状态管理
const medications = ref([])
const searchQuery = ref('')
const filterStatus = ref('all')
const showModal = ref(false) // 管理添加/编辑页面的显示
const showPhotoViewer = ref(false) // 管理照片查看器显示
const viewingPhoto = ref(null) // 管理照片查看器的数据
const currentMedication = ref(null) // 管理编辑页面内容数据
const loading = ref(false) // 加载状态

// 筛选后的药物列表 (基于原始药物列表与筛选条件计算) (直接用于组件显示)
const filteredMedications = computed(() => {
  let result = medications.value

  // 按搜索关键词筛选 (无关键词则直接跳过)
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(med =>
      med.name.toLowerCase().includes(query)
    )
  }

  // 按状态筛选
  if (filterStatus.value !== 'all') {
    const isActive = filterStatus.value === 'active' ? 1 : 0 // active -> 1
    result = result.filter(med => med.is_active === isActive)
  }

  return result
})

// 加载所有药物列表
const loadMedications = async () => {
  loading.value = true
  try {
    medications.value = await getMedications()
  } catch (error) {
    console.error('加载药物列表失败：', error)
    toast.error('加载药物列表失败')
  } finally {
    loading.value = false
  }
}

// 打开添加药物弹窗
const handleAddMedication = () => {
  currentMedication.value = null  // 重置当前编辑的药物
  showModal.value = true
}

// 打开编辑药物弹窗
const handleEditMedication = (medication) => {
  currentMedication.value = medication // 将当前编辑药物设置为选择的药物信息
  showModal.value = true
}

// 关闭表单弹窗
const handleCloseModal = () => {
  showModal.value = false
  currentMedication.value = null // 重置当前编辑药物
}

// 表单提交成功
const handleFormSuccess = async (isEditing) => {
  await loadMedications() // 表单提交后重新加载药物列表
  toast.success(isEditing ? '药物更新成功' : '药物添加成功') // 根据参数生成提示
}

// 删除药物方法
const handleDeleteMedication = async (medication) => {
  try {
    // 触发选项弹窗
    await confirm.danger(
      `确定要删除药物"${medication.name}"吗？此操作无法撤销。`,
      '删除药物'
    )
    // 发送删除药物请求
    await deleteMedication(medication.id)
    // 提示请求成功
    toast.success('药物删除成功')
    // 重新加载药物列表
    await loadMedications()
  } catch (error) {
    if (error.message === '用户取消') return
    console.error('删除失败：', error)
    toast.error(error.response?.data?.detail || '删除失败，请重试')
  }
}

// 查看照片 (绑定每药物卡片的照片子元素点击事件，触发查看器)
const handleViewPhoto = (photo) => {
  viewingPhoto.value = photo // 将当前查看的图像数据设为事件传递的图像数据
  showPhotoViewer.value = true
}

// 关闭照片查看器
const handleClosePhotoViewer = () => {
  showPhotoViewer.value = false // 重置当前查看的图像数据
  viewingPhoto.value = null
}

// 页面挂载时加载药物列表
onMounted(async () => {
  await loadMedications()

  // 检查是否有编辑参数 (\home\medicines?{编辑参数}) (可以直接进行精确跳转直接显示对应的编辑页面)
  const editId = route.query?.edit
  if (editId) {
    const medication = medications.value.find(m => m.id === parseInt(editId)) // 查询对应id的药物数据
    if (medication) {
      handleEditMedication(medication) // 如果数据存在则直接触发对应方法打开对应药物编辑界面
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

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  gap: 1rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-gray-200);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0;
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
