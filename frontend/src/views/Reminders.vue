<template>
  <div class="reminders-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">用药提醒</h1>
        <p class="page-subtitle">按日期查看和管理用药记录</p>
      </div>
      <button @click="handleGenerateRecords" class="generate-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="23 4 23 10 17 10"></polyline>
          <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
        </svg>
        <span>生成记录</span>
      </button>
    </div>

    <!-- 日期选择器 -->
    <DateSelector
      v-model="selectedDate"
      @previous="previousDay"
      @next="nextDay"
      @today="goToToday"
      @update:modelValue="loadReminders"
    />

    <!-- 统计信息栏 -->
    <StatsBar
      v-if="reminders.length > 0"
      :total="reminders.length"
      :completed="completedCount"
    />

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p class="loading-text">加载中...</p>
    </div>

    <!-- 空状态 -->
    <EmptyState
      v-else-if="reminders.length === 0"
      title="该日期暂无用药记录"
      description="请先在'药物管理'中添加药物，然后点击'生成记录'按钮"
      action-text="前往药物管理"
      @action="goToMedications"
    >
      <template #icon>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <polyline points="12 6 12 12 16 14"></polyline>
        </svg>
      </template>
    </EmptyState>

    <!-- 用药记录列表 -->
    <div v-else class="records-list">
      <ReminderCard
        v-for="reminder in reminders"
        :key="reminder.id"
        :reminder="reminder"
        @toggle="toggleComplete"
      />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { generateReminders, getRemindersByDate, completeReminder, uncompleteReminder } from '@/api/reminder'
import DateSelector from '@/components/reminders/DateSelector.vue'
import StatsBar from '@/components/reminders/StatsBar.vue'
import ReminderCard from '@/components/reminders/ReminderCard.vue'
import EmptyState from '@/assets/EmptyState.vue'
import toast from '@/utils/toast'

const router = useRouter()
const loading = ref(false)
const reminders = ref([])
const selectedDate = ref(getTodayString())

// 获取今天的日期字符串
function getTodayString() {
  const today = new Date()
  return today.toISOString().split('T')[0]
}

// 统计信息
const completedCount = computed(() => {
  return reminders.value.filter(r => r.is_completed).length
})

// 加载提醒
const loadReminders = async () => {
  loading.value = true
  try {
    reminders.value = await getRemindersByDate(selectedDate.value)
  } catch (error) {
    console.error('加载用药记录失败：', error)
    toast.error('加载用药记录失败')
  } finally {
    loading.value = false
  }
}

// 切换完成状态
const toggleComplete = async (reminderId) => {
  const reminder = reminders.value.find(r => r.id === reminderId)
  if (!reminder) return

  try {
    if (reminder.is_completed) {
      await uncompleteReminder(reminder.id)
      reminder.is_completed = false
      reminder.completed_at = null
      toast.success('已取消完成')
    } else {
      const updated = await completeReminder(reminder.id)
      reminder.is_completed = true
      reminder.completed_at = updated.completed_at
      toast.success('已标记为完成')
    }
  } catch (error) {
    console.error('更新失败：', error)
    toast.error('操作失败，请重试')
  }
}

// 生成记录
const handleGenerateRecords = async () => {
  try {
    const result = await generateReminders(30) // 生成未来30天的记录
    toast.success(result.message)
    await loadReminders()
  } catch (error) {
    console.error('生成记录失败：', error)
    toast.error(error.response?.data?.detail || '生成记录失败')
  }
}

// 日期导航
const previousDay = () => {
  const date = new Date(selectedDate.value)
  date.setDate(date.getDate() - 1)
  selectedDate.value = date.toISOString().split('T')[0]
  loadReminders()
}

const nextDay = () => {
  const date = new Date(selectedDate.value)
  date.setDate(date.getDate() + 1)
  selectedDate.value = date.toISOString().split('T')[0]
  loadReminders()
}

const goToToday = () => {
  selectedDate.value = getTodayString()
  loadReminders()
}

// 前往药物管理
const goToMedications = () => {
  router.push('/home/medicines')
}

onMounted(() => {
  loadReminders()
})
</script>

<style scoped>
.reminders-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 页面头部 */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.header-content {
  flex: 1;
  min-width: 0;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

.page-subtitle {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0;
  line-height: 1.5;
}

.generate-btn {
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
  white-space: nowrap;
  flex-shrink: 0;
}

.generate-btn:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.generate-btn:active {
  transform: translateY(0);
}

.generate-btn svg {
  width: 20px;
  height: 20px;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 300px;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--color-gray-200);
  border-top: 4px solid var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 记录列表 */
.records-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 平板端优化 */
@media (max-width: 1024px) {
  .reminders-page {
    padding: 1.5rem;
    gap: 1.25rem;
  }

  .page-title {
    font-size: 1.75rem;
  }
}

/* 移动端优化 */
@media (max-width: 768px) {
  .reminders-page {
    padding: 1rem;
    gap: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: stretch;
  }

  .generate-btn {
    width: 100%;
    justify-content: center;
    padding: 0.75rem 1.25rem;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .page-subtitle {
    font-size: 0.9375rem;
  }

  .loading-state {
    padding: 3rem 1.5rem;
    min-height: 250px;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border-width: 3px;
  }
}

/* 小屏手机优化 */
@media (max-width: 480px) {
  .reminders-page {
    padding: 0.75rem;
  }

  .page-title {
    font-size: 1.375rem;
  }

  .page-subtitle {
    font-size: 0.875rem;
  }

  .generate-btn {
    font-size: 0.9375rem;
    padding: 0.625rem 1rem;
  }

  .generate-btn svg {
    width: 18px;
    height: 18px;
  }
}

/* 触摸设备优化 */
@media (hover: none) and (pointer: coarse) {
  .generate-btn {
    min-height: 44px;
    -webkit-tap-highlight-color: transparent;
  }
}
</style>
