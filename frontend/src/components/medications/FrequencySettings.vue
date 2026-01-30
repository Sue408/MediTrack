<template>
  <div class="frequency-settings">
    <!-- 频率类型选择 -->
    <div class="form-group">
      <label class="form-label">服用频率类型 <span class="required">*</span></label>
      <div class="radio-group">
        <label class="radio-label" :class="{ active: modelValue.frequency_type === 'daily' }">
          <input
            :checked="modelValue.frequency_type === 'daily'"
            @change="updateField('frequency_type', 'daily')"
            type="radio"
            name="frequency_type"
            value="daily"
            class="radio-input"
            required
          />
          <span>每天</span>
        </label>
        <label class="radio-label" :class="{ active: modelValue.frequency_type === 'weekly' }">
          <input
            :checked="modelValue.frequency_type === 'weekly'"
            @change="updateField('frequency_type', 'weekly')"
            type="radio"
            name="frequency_type"
            value="weekly"
            class="radio-input"
            required
          />
          <span>每周</span>
        </label>
      </div>
    </div>

    <!-- 每日频率设置 -->
    <div v-if="modelValue.frequency_type === 'daily'" class="frequency-section">
      <div class="form-group">
        <label class="form-label">每日服用次数 <span class="required">*</span></label>
        <input
          :value="modelValue.times_per_day"
          @input="updateField('times_per_day', parseInt($event.target.value) || 1)"
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
            v-for="(time, index) in modelValue.daily_times"
            :key="index"
            class="time-input-row"
          >
            <input
              :value="time"
              @input="updateTime(index, $event.target.value)"
              type="time"
              class="form-input time-input"
              required
            />
            <button
              v-if="modelValue.daily_times.length > 1"
              type="button"
              @click="removeTime(index)"
              class="remove-time-btn"
              title="删除此时间"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
        </div>
        <button
          v-if="modelValue.daily_times.length < 10"
          type="button"
          @click="addTime"
          class="add-time-btn"
        >
          + 添加时间
        </button>
      </div>
    </div>

    <!-- 每周频率设置 -->
    <div v-if="modelValue.frequency_type === 'weekly'" class="frequency-section">
      <div class="form-group">
        <label class="form-label">服用日期 <span class="required">*</span></label>
        <div class="weekday-selector">
          <label
            v-for="day in weekdays"
            :key="day.value"
            class="weekday-label"
            :class="{ active: modelValue.weekly_days.includes(day.value) }"
          >
            <input
              :checked="modelValue.weekly_days.includes(day.value)"
              @change="toggleWeekday(day.value)"
              type="checkbox"
              :value="day.value"
              class="weekday-checkbox"
            />
            <span class="weekday-text">{{ day.label }}</span>
          </label>
        </div>
        <p v-if="modelValue.weekly_days.length === 0" class="field-hint error">
          请至少选择一天
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

const weekdays = [
  { label: '周一', value: 1 },
  { label: '周二', value: 2 },
  { label: '周三', value: 3 },
  { label: '周四', value: 4 },
  { label: '周五', value: 5 },
  { label: '周六', value: 6 },
  { label: '周日', value: 7 }
]

const updateField = (field, value) => {
  // 当修改每日次数时，自动调整时间数组长度
  if (field === 'times_per_day') {
    const currentTimes = [...props.modelValue.daily_times]
    const newCount = value

    if (newCount > currentTimes.length) {
      // 增加时间点
      while (currentTimes.length < newCount) {
        currentTimes.push('08:00')
      }
    } else if (newCount < currentTimes.length) {
      // 减少时间点
      currentTimes.splice(newCount)
    }

    emit('update:modelValue', {
      ...props.modelValue,
      times_per_day: value,
      daily_times: currentTimes
    })
  } else {
    emit('update:modelValue', {
      ...props.modelValue,
      [field]: value
    })
  }
}

// 监听频率类型变化，重置相关字段
watch(() => props.modelValue.frequency_type, (newType) => {
  if (newType === 'daily') {
    // 切换到每日模式，确保有默认时间
    if (!props.modelValue.daily_times || props.modelValue.daily_times.length === 0) {
      emit('update:modelValue', {
        ...props.modelValue,
        times_per_day: 1,
        daily_times: ['08:00']
      })
    }
  }
})

const updateTime = (index, value) => {
  const newTimes = [...props.modelValue.daily_times]
  newTimes[index] = value
  updateField('daily_times', newTimes)
}

const addTime = () => {
  if (props.modelValue.daily_times.length < 10) {
    const newTimes = [...props.modelValue.daily_times, '08:00']
    updateField('daily_times', newTimes)
    updateField('times_per_day', newTimes.length)
  }
}

const removeTime = (index) => {
  if (props.modelValue.daily_times.length > 1) {
    const newTimes = props.modelValue.daily_times.filter((_, i) => i !== index)
    emit('update:modelValue', {
      ...props.modelValue,
      times_per_day: newTimes.length,
      daily_times: newTimes
    })
  }
}

const toggleWeekday = (value) => {
  const currentDays = [...props.modelValue.weekly_days]
  const index = currentDays.indexOf(value)

  if (index > -1) {
    currentDays.splice(index, 1)
  } else {
    currentDays.push(value)
  }

  updateField('weekly_days', currentDays)
}
</script>

<style scoped>
.frequency-settings {
  display: flex;
  flex-direction: column;
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

.required {
  color: var(--color-error);
}

/* 单选按钮组 */
.radio-group {
  display: flex;
  gap: 0.75rem;
}

.radio-label {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  background-color: var(--color-bg-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.radio-label:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.radio-label.active {
  border-color: var(--color-primary);
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.radio-input {
  display: none;
}

/* 输入框 */
.form-input {
  padding: 0.75rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  font-size: 0.9375rem;
  color: var(--color-text-primary);
  background-color: var(--color-bg-secondary);
  transition: all var(--transition-fast);
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

/* 频率设置区域 */
.frequency-section {
  padding: 1rem;
  background-color: var(--color-bg-secondary);
  border-radius: 8px;
  border: 1px solid var(--color-border-light);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

/* 时间输入 */
.time-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
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
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border-light);
  border-radius: 6px;
  background-color: var(--color-bg-primary);
  color: var(--color-error);
  cursor: pointer;
  transition: all var(--transition-fast);
  flex-shrink: 0;
}

.remove-time-btn svg {
  width: 16px;
  height: 16px;
}

.remove-time-btn:hover {
  background-color: var(--color-error);
  border-color: var(--color-error);
  color: var(--color-text-light);
}

.add-time-btn {
  padding: 0.625rem 1rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.add-time-btn:hover {
  background-color: var(--color-gray-800);
}

/* 星期选择器 */
.weekday-selector {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.5rem;
}

.weekday-label {
  padding: 0.75rem 0.5rem;
  border: 1px solid var(--color-border-light);
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  background-color: var(--color-bg-secondary);
}

.weekday-label:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg-primary);
}

.weekday-label.active {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-text-light);
}

.weekday-checkbox {
  display: none;
}

.weekday-text {
  font-size: 0.875rem;
  font-weight: 500;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  margin: 0.25rem 0 0 0;
}

.field-hint.error {
  color: var(--color-error);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .weekday-selector {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
