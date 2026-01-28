<template>
  <div class="reminders-page">
    <div class="page-header">
      <div>
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
    <div class="date-selector">
      <button @click="previousDay" class="date-nav-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6"></polyline>
        </svg>
      </button>

      <div class="date-display">
        <input
          v-model="selectedDate"
          type="date"
          class="date-input"
          @change="loadReminders"
        />
        <button @click="goToToday" class="today-btn">今天</button>
      </div>

      <button @click="nextDay" class="date-nav-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>

    <!-- 统计信息 -->
    <div v-if="reminders.length > 0" class="stats-bar">
      <div class="stat-item">
        <span class="stat-label">总计</span>
        <span class="stat-value">{{ reminders.length }}</span>
      </div>
      <div class="stat-item completed">
        <span class="stat-label">已完成</span>
        <span class="stat-value">{{ completedCount }}</span>
      </div>
      <div class="stat-item pending">
        <span class="stat-label">待完成</span>
        <span class="stat-value">{{ pendingCount }}</span>
      </div>
      <div class="stat-item progress">
        <span class="stat-label">完成率</span>
        <span class="stat-value">{{ completionRate }}%</span>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 空状态 -->
    <div v-else-if="reminders.length === 0" class="empty-state">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
      <p>该日期暂无用药记录</p>
      <p class="empty-hint">请先在"药物管理"中添加药物，然后点击"生成记录"按钮</p>
      <button @click="goToMedications" class="empty-add-btn">前往药物管理</button>
    </div>

    <!-- 用药记录列表 -->
    <div v-else class="records-list">
      <div
        v-for="reminder in reminders"
        :key="reminder.id"
        class="record-item"
        :class="{ completed: reminder.is_completed }"
      >
        <div class="record-checkbox">
          <input
            type="checkbox"
            :checked="reminder.is_completed"
            @change="toggleComplete(reminder)"
            class="checkbox-input"
          />
          <span class="checkbox-custom"></span>
        </div>

        <div class="record-content">
          <div class="record-header">
            <h3 class="medication-name">{{ reminder.medication_name }}</h3>
            <span v-if="reminder.dosage" class="dosage-badge">{{ reminder.dosage }}</span>
          </div>

          <div class="record-info">
            <div v-if="reminder.scheduled_time" class="time-info">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <polyline points="12 6 12 12 16 14"></polyline>
              </svg>
              <span>{{ reminder.scheduled_time }}</span>
            </div>
            <div v-else class="time-info">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                <line x1="16" y1="2" x2="16" y2="6"></line>
                <line x1="8" y1="2" x2="8" y2="6"></line>
                <line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <span>每周服用</span>
            </div>

            <div v-if="reminder.is_completed && reminder.completed_at" class="completed-info">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>{{ formatCompletedTime(reminder.completed_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {generateReminders, getRemindersByDate, completeReminder, uncompleteReminder} from '@/api/reminder'
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

const pendingCount = computed(() => {
  return reminders.value.filter(r => !r.is_completed).length
})

const completionRate = computed(() => {
  if (reminders.value.length === 0) return 0
  return Math.round((completedCount.value / reminders.value.length) * 100)
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
const toggleComplete = async (record) => {
  try {
    if (record.is_completed) {
      await uncompleteReminder(record.id)
      record.is_completed = false
      record.completed_at = null
      toast.success('已取消完成')
    } else {
      const updated = await completeReminder(record.id)
      record.is_completed = true
      record.completed_at = updated.completed_at
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

// 格式化完成时间
const formatCompletedTime = (datetime) => {
  const date = new Date(datetime)
  return `完成于 ${date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })}`
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

.generate-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.generate-btn:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.generate-btn svg {
  width: 20px;
  height: 20px;
}

/* 日期选择器 */
.date-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
}

.date-nav-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.date-nav-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

.date-nav-btn svg {
  width: 20px;
  height: 20px;
  color: var(--color-text-primary);
}

.date-display {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.date-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 1rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.date-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1);
}

.today-btn {
  padding: 0.75rem 1.5rem;
  background-color: var(--color-bg-secondary);
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.today-btn:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-300);
}

/* 统计信息 */
.stats-bar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-item {
  padding: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 0.875rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
}

.stat-value {
  display: block;
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
}

.stat-item.completed .stat-value {
  color: #10b981;
}

.stat-item.pending .stat-value {
  color: #f59e0b;
}

.stat-item.progress .stat-value {
  color: var(--color-primary);
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--color-text-secondary);
  font-size: 1.1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-state svg {
  width: 80px;
  height: 80px;
  color: var(--color-gray-800);
  margin-bottom: 1rem;
}

.empty-state p {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.5rem;
}

.empty-hint {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.empty-add-btn {
  padding: 0.75rem 2rem;
  background-color: var(--color-primary);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--transition-base);
}

.empty-add-btn:hover {
  background-color: var(--color-gray-800);
}

/* 记录列表 */
.records-list {
  display: grid;
  gap: 1rem;
}

.record-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-sm);
  border: 2px solid var(--color-border-light);
  transition: all var(--transition-base);
}

.record-item:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.record-item.completed {
  border-color: #10b981;
  background-color: #f0fdf4;
}

.record-checkbox {
  position: relative;
  flex-shrink: 0;
}

.checkbox-input {
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.checkbox-custom {
  display: block;
  width: 28px;
  height: 28px;
  border: 2px solid var(--color-border-light);
  border-radius: 6px;
  background-color: white;
  cursor: pointer;
  transition: all var(--transition-base);
}

.checkbox-input:checked + .checkbox-custom {
  background-color: #10b981;
  border-color: #10b981;
}

.checkbox-input:checked + .checkbox-custom::after {
  content: '';
  position: absolute;
  left: 9px;
  top: 5px;
  width: 6px;
  height: 12px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.record-content {
  flex: 1;
}

.record-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}

.medication-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.record-item.completed .medication-name {
  text-decoration: line-through;
  color: var(--color-text-secondary);
}

.dosage-badge {
  padding: 0.25rem 0.75rem;
  background-color: var(--color-gray-100);
  color: var(--color-text-secondary);
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.record-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.time-info,
.completed-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-secondary);
  font-size: 0.875rem;
}

.time-info svg,
.completed-info svg {
  width: 16px;
  height: 16px;
}

.completed-info {
  color: #10b981;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .reminders-page {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .generate-btn {
    width: 100%;
    justify-content: center;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .stats-bar {
    grid-template-columns: repeat(2, 1fr);
  }

  .date-selector {
    flex-direction: column;
    gap: 1rem;
  }

  .date-display {
    width: 100%;
    flex-direction: column;
  }

  .date-input,
  .today-btn {
    width: 100%;
  }

  .record-item {
    padding: 1rem;
  }

  .record-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
