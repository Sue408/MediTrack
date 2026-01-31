<template>
  <div class="profile-page">
    <div class="page-header">
      <h1 class="page-title">个人信息</h1>
      <p class="page-subtitle">查看和管理您的个人资料</p>
    </div>

    <div class="profile-content">
      <!-- 头像区域 -->
      <div class="avatar-section">
        <div class="avatar-container">
          <img v-if="user?.avatar_url" :src="user.avatar_url" alt="头像" class="avatar-large" />
          <div v-else class="avatar-placeholder-large">
            {{ user?.username?.charAt(0).toUpperCase() }}
          </div>
        </div>
        <button @click="handleUploadAvatar" class="upload-btn">更换头像</button>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          style="display: none"
          @change="handleFileChange"
        />
      </div>

      <!-- 信息卡片 -->
      <div class="info-section">
        <div class="info-card">
          <h3 class="card-title">基本信息</h3>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">用户名</span>
              <span class="value">{{ user?.username }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱</span>
              <span class="value">{{ user?.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">注册时间</span>
              <span class="value">{{ formatDate(user?.created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="info-card">
          <h3 class="card-title">账户操作</h3>
          <div class="action-buttons">
            <button @click="handleEditProfile" class="action-btn primary">
              编辑资料
            </button>
            <button @click="handleChangePassword" class="action-btn secondary">
              修改密码
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { uploadAvatar } from '@/api/user'
import toast from '@/utils/toast'

const userStore = useUserStore()
const user = computed(() => userStore.user)
const fileInput = ref(null)

// 格式化日期 (2026-1-12 -> 2026年1月12日)
const formatDate = (dateString) => {
  if (!dateString) return '未知'
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// 上传头像方法
const handleUploadAvatar = () => {
  fileInput.value?.click() // 点击按钮即直接触发fileInput的文件上传操作
}

// 修改头像方法 (绑定文件上传input的change事件)
const handleFileChange = async (event) => {
  // 检查文件是否存在
  const file = event.target.files?.[0]
  if (!file) return

  // 检查文件大小（限制5MB）
  if (file.size > 5 * 1024 * 1024) {
    toast.warning('图片大小不能超过5MB')
    return
  }

  // 检查文件类型
  if (!file.type.startsWith('image/')) {
    toast.warning('请选择图片文件')
    return
  }

  try {
    // 转换为Base64并上传
    const reader = new FileReader()
    reader.onload = async (e) => {
      const base64 = e.target.result

      try {
        // 调用API上传（传递对象格式）
        const response = await uploadAvatar({ avatar: base64 })

        // 更新用户信息
        userStore.setUser(response)
        toast.success('头像上传成功', 500)
      } catch (error) {
        console.error('头像上传失败：', error)
        toast.error(error.response?.data?.detail || '头像上传失败，请重试')
      } finally {
        // 最后清空文件选择，允许重复选择同一文件
        event.target.value = ''
      }
    }
    reader.readAsDataURL(file) // 解析成DataURL再调用回调
  } catch (error) {
    console.error('文件读取失败：', error)
    toast.error('文件读取失败，请重试')
  }
}

// 编辑资料
const handleEditProfile = () => {
  toast.info('编辑资料功能开发中...')
}

// 修改密码
const handleChangePassword = () => {
  toast.info('修改密码功能开发中...')
}
</script>

<style scoped>
.profile-page {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
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

.profile-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
}

/* 头像区域 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-md);
  height: fit-content;
}

.avatar-container {
  position: relative;
}

.avatar-large {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid var(--color-border-light);
}

.avatar-placeholder-large {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: var(--color-gray-800);
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 3rem;
  border: 4px solid var(--color-border-light);
}

.upload-btn {
  padding: 0.75rem 2rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.upload-btn:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 信息区域 */
.info-section {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-card {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-md);
}

.card-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-border-light);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item .label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.info-item .value {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.status-active {
  color: var(--color-success);
}

.status-inactive {
  color: var(--color-error);
}

/* 操作按钮 */
.action-buttons {
  display: flex;
  gap: 1rem;
}

.action-btn {
  flex: 1;
  padding: 0.875rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.action-btn.primary {
  background-color: var(--color-primary);
  color: var(--color-text-light);
}

.action-btn.primary:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.action-btn.secondary {
  background-color: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border: 2px solid var(--color-border-light);
}

.action-btn.secondary:hover {
  background-color: var(--color-gray-100);
  border-color: var(--color-gray-400);
  transform: translateY(-2px);
}

/* 响应式设计 */
@media (max-width: 968px) {
  .profile-content {
    grid-template-columns: 1fr;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }
}
</style>
