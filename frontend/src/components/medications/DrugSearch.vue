<template>
  <div class="drug-search">
    <!-- 搜索输入区 -->
    <div class="search-section">
      <div class="search-input-group">
        <input
          v-model="searchQuery"
          type="text"
          class="search-input"
          :placeholder="searchPlaceholder"
          @input="handleSearchInput"
          @keyup.enter="handleSearch"
        />
        <div class="search-type-select">
          <CustomSelect
          v-model="searchType"
          :options="searchTypeOptions"
          @change="handleSearchTypeChange"
          />
        </div>  
        <button class="search-btn" @click="handleSearch" :disabled="!searchQuery.trim()">
          搜索
        </button>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">正在搜索药物信息...</p>
    </div>

    <!-- 搜索结果列表 -->
    <div v-else-if="searchResults.length > 0" class="search-results">
      <div class="results-header">
        <span class="results-count">找到 <strong>{{ searchResults.length }}</strong> 个结果</span>
        <button class="clear-btn" @click="clearSearch">清除</button>
      </div>
      <div class="results-list">
        <div
          v-for="drug in searchResults"
          :key="drug.external_drug_id"
          class="drug-item"
          :class="{ selected: selectedDrug?.external_drug_id === drug.external_drug_id }"
          @click="selectDrug(drug)"
        >
          <!-- 药物图片 -->
          <div class="drug-image">
            <img v-if="drug.drug_image_url" :src="drug.drug_image_url" alt="药品图片" />
            <div v-else class="no-image">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                <circle cx="8.5" cy="8.5" r="1.5"></circle>
                <polyline points="21 15 16 10 5 21"></polyline>
              </svg>
            </div>
          </div>

          <!-- 药物信息 -->
          <div class="drug-info">
            <h4 class="drug-name">{{ drug.name }}</h4>
            <p v-if="drug.generic_name" class="drug-generic-name">
              通用名：{{ drug.generic_name }}
            </p>
            <p class="drug-spec">{{ drug.specification }}</p>
            <p class="drug-manufacturer">{{ drug.manufacturer }}</p>
          </div>

          <!-- 标识 -->
          <div class="drug-badges">
            <span v-if="drug.is_prescription === 1" class="badge prescription">处方药</span>
            <span v-else class="badge otc">非处方药</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 无结果提示 -->
    <div v-else-if="searched && searchResults.length === 0" class="no-results">
      <svg class="empty-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"></circle>
        <path d="m21 21-4.35-4.35"></path>
      </svg>
      <p class="empty-text">未找到匹配的药物</p>
      <button class="manual-entry-btn" @click="handleManualEntry">
        手动录入
      </button>
    </div>

    <!-- 初始提示 -->
    <div v-else class="initial-hint">
      <svg class="hint-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M12 16v-4"></path>
        <path d="M12 8h.01"></path>
      </svg>
      <p class="hint-text">请输入药物名称、条形码或生产厂家进行搜索</p>
      <p class="hint-subtext">或者</p>
      <button class="manual-entry-btn secondary" @click="handleManualEntry">
        直接手动录入
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { searchDrugs } from '@/api/thirdParty'
import CustomSelect from '@/assets/CustomSelect.vue'
import toast from '@/utils/toast'

const emit = defineEmits(['select', 'manual-entry'])

// 搜索相关状态
const searchQuery = ref('')
const searchType = ref('name')
const searchResults = ref([])
const selectedDrug = ref(null)
const loading = ref(false)
const searched = ref(false)

// 搜索类型选项
const searchTypeOptions = [
  { label: '药物名称', value: 'name' },
  { label: '条形码', value: 'barcode' },
  { label: '生产厂家', value: 'manufacturer' }
]

// 防抖定时器
let debounceTimer = null

// 搜索占位符
const searchPlaceholder = computed(() => {
  const placeholders = {
    name: '输入药物名称，如：阿莫西林',
    barcode: '输入或扫描条形码',
    manufacturer: '输入生产厂家名称'
  }
  return placeholders[searchType.value]
})

// 处理搜索输入（防抖）
const handleSearchInput = () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  // 如果输入为空，清除结果
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    searched.value = false
    return
  }

  // 300ms 防抖
  debounceTimer = setTimeout(() => {
    handleSearch()
  }, 300)
}

// 执行搜索
const handleSearch = async () => {
  const query = searchQuery.value.trim()
  if (!query) return

  loading.value = true
  searched.value = false

  try {
    const response = await searchDrugs(query, searchType.value, 10)
    searchResults.value = response.data || response
    searched.value = true
  } catch (error) {
    console.error('搜索药物失败:', error)
    toast.error('搜索失败，请稍后重试')
    searchResults.value = []
    searched.value = true
  } finally {
    loading.value = false
  }
}

// 搜索类型改变
const handleSearchTypeChange = () => {
  if (searchQuery.value.trim()) {
    handleSearch()
  }
}

// 选择药物
const selectDrug = (drug) => {
  selectedDrug.value = drug
  emit('select', drug)
}

// 清除搜索
const clearSearch = () => {
  searchQuery.value = ''
  searchResults.value = []
  selectedDrug.value = null
  searched.value = false
}

// 手动录入
const handleManualEntry = () => {
  emit('manual-entry')
}

// 暴露方法供父组件调用
defineExpose({
  clearSearch
})
</script>

<style scoped>
.drug-search {
  width: 100%;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 1.5rem;
}

.search-input-group {
  display: flex;
  gap: 0.75rem;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  transition: all var(--transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.search-type-select {
  width: 20%;
  margin-right: 10px;
}

.search-btn {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
  white-space: nowrap;
}

.search-btn:hover:not(:disabled) {
  background-color: var(--color-gray-800);
}

.search-btn:disabled {
  background-color: var(--color-gray-300);
  color: var(--color-gray-500);
  cursor: not-allowed;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 3rem 1.5rem;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid var(--color-gray-200);
  border-top: 3px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 搜索结果 */
.search-results {
  margin-top: 1rem;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--color-border-light);
}

.results-count {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.results-count strong {
  color: var(--color-text-primary);
  font-weight: 600;
}

.clear-btn {
  padding: 0.375rem 0.75rem;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.clear-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

.results-list {
  max-height: 400px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* 药物项 */
.drug-item {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.drug-item:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg-secondary);
}

.drug-item.selected {
  border-color: var(--color-primary);
  background-color: var(--color-gray-100);
  box-shadow: 0 0 0 1px var(--color-primary);
}

.drug-image {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 6px;
  overflow: hidden;
  background-color: var(--color-bg-secondary);
}

.drug-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
}

.no-image svg {
  width: 32px;
  height: 32px;
}

.drug-info {
  flex: 1;
  min-width: 0;
}

.drug-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.25rem 0;
}

.drug-generic-name {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  margin: 0 0 0.25rem 0;
}

.drug-spec,
.drug-manufacturer {
  font-size: 0.8125rem;
  color: var(--color-text-secondary);
  margin: 0.125rem 0;
}

.drug-badges {
  display: flex;
  align-items: flex-start;
}

.badge {
  padding: 0.25rem 0.625rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  white-space: nowrap;
}

.badge.prescription {
  background-color: var(--color-gray-900);
  color: var(--color-text-light);
}

.badge.otc {
  background-color: var(--color-gray-100);
  color: var(--color-text-primary);
}

/* 空状态 */
.no-results,
.initial-hint {
  text-align: center;
  padding: 3rem 1.5rem;
}

.empty-icon,
.hint-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 1rem;
  color: var(--color-text-secondary);
}

.empty-text,
.hint-text {
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
}

.hint-subtext {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin: 1rem 0 0.75rem 0;
}

.manual-entry-btn {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 0.9375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.manual-entry-btn:hover {
  background-color: var(--color-gray-800);
}

.manual-entry-btn.secondary {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 1px solid var(--color-border-light);
}

.manual-entry-btn.secondary:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .search-input-group {
    flex-direction: column;
  }

  .drug-item {
    flex-direction: column;
  }

  .drug-image {
    width: 100%;
    height: 150px;
  }
}
</style>
