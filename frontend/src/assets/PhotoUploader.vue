<template>
  <div class="photo-uploader">
    <div v-if="photos.length > 0" class="photo-preview-list">
      <div
        v-for="(photo, index) in photos"
        :key="index"
        class="photo-preview-item"
      >
        <img :src="photo" :alt="`照片${index + 1}`" class="preview-image" />
        <button
          type="button"
          @click="handleRemove(index)"
          class="remove-photo-btn"
          title="删除照片"
        >
          ×
        </button>
      </div>
    </div>
    <button
      v-if="photos.length < maxPhotos"
      type="button"
      @click="triggerUpload"
      class="upload-photo-btn"
    >
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21 15 16 10 5 21"></polyline>
      </svg>
      <span>{{ photos.length > 0 ? '继续添加' : uploadText }}</span>
      <span class="upload-hint">(最多{{ maxPhotos }}张)</span>
    </button>
    <input
      ref="fileInput"
      type="file"
      accept="image/*"
      style="display: none"
      @change="handleFileChange"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import toast from '@/utils/toast'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  },
  maxPhotos: {
    type: Number,
    default: 3
  },
  maxSize: {
    type: Number,
    default: 2 * 1024 * 1024 // 2MB
  },
  uploadText: {
    type: String,
    default: '上传照片'
  }
})

const emit = defineEmits(['update:modelValue'])

const fileInput = ref(null)
const photos = ref([...props.modelValue])

// 触发文件选择
const triggerUpload = () => {
  fileInput.value?.click()
}

// 处理文件选择
const handleFileChange = async (event) => {
  const file = event.target.files?.[0]
  if (!file) return

  // 检查文件大小
  if (file.size > props.maxSize) {
    toast.warning(`图片大小不能超过${props.maxSize / (1024 * 1024)}MB`)
    event.target.value = ''
    return
  }

  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    toast.warning('请选择图片文件')
    event.target.value = ''
    return
  }

  try {
    // 转换为Base64
    const reader = new FileReader()
    reader.onload = (e) => {
      const base64 = e.target.result
      photos.value.push(base64)
      emit('update:modelValue', photos.value)
      event.target.value = ''
    }
    reader.readAsDataURL(file)
  } catch (error) {
    console.error('文件读取失败：', error)
    toast.error('文件读取失败，请重试')
    event.target.value = ''
  }
}

// 删除照片
const handleRemove = (index) => {
  photos.value.splice(index, 1)
  emit('update:modelValue', photos.value)
}

// 监听外部变化
const updatePhotos = (newPhotos) => {
  photos.value = [...newPhotos]
}

defineExpose({
  updatePhotos
})
</script>

<style scoped>
.photo-uploader {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.photo-preview-list {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.photo-preview-item {
  position: relative;
  width: 100px;
  height: 100px;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
  border: 2px solid var(--color-border-light);
}

.remove-photo-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--color-error);
  color: white;
  border: none;
  font-size: 1.2rem;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.remove-photo-btn:hover {
  transform: scale(1.1);
  background-color: #dc2626;
}

.upload-photo-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.5rem;
  border: 2px dashed var(--color-border-light);
  border-radius: 8px;
  background-color: var(--color-bg-secondary);
  color: var(--color-text-secondary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.upload-photo-btn:hover {
  border-color: var(--color-primary);
  background-color: var(--color-gray-50);
  color: var(--color-primary);
}

.upload-photo-btn svg {
  width: 32px;
  height: 32px;
}

.upload-hint {
  font-size: 0.75rem;
  color: var(--color-text-secondary);
}
</style>
