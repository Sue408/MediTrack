<template>
  <div class="auth-form-container">
    <div class="content">
      <Logo size="120px" color="var(--color-primary)" />
      <h1 class="app-title">MediTrack</h1>
    </div>
    <div class="auth-form">
      <!-- 标题 - 添加key实现切换动画 -->
      <transition name="slide-fade" mode="out-in">
        <div :key="isLogin ? 'login' : 'register'" class="form-header">
          <h2 class="form-title">{{ isLogin ? '登录' : '注册' }}</h2>
          <p class="form-subtitle">{{ isLogin ? '欢迎回来' : '创建新账户' }}</p>
        </div>
      </transition>

      <!-- 表单 -->
      <form @submit.prevent="handleSubmit">
        <!-- 注册时显示用户名 -->
        <transition name="slide-down">
          <div v-if="!isLogin" class="form-group">
            <label for="username">用户名</label>
            <input
              id="username"
              v-model="formData.username"
              type="text"
              placeholder="请输入用户名"
              required
            />
          </div>
        </transition>

        <!-- 邮箱 -->
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="formData.email"
            type="email"
            placeholder="请输入邮箱"
            required
          />
        </div>

        <!-- 密码 -->
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            required
          />
        </div>

        <!-- 注册时显示确认密码 -->
        <transition name="slide-down">
          <div v-if="!isLogin" class="form-group">
            <label for="confirmPassword">确认密码</label>
            <input
              id="confirmPassword"
              v-model="formData.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              required
            />
          </div>
        </transition>

        <!-- 错误提示 -->
        <transition name="fade">
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
        </transition>

        <!-- 提交按钮 -->
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? '处理中...' : (isLogin ? '登录' : '注册') }}
        </button>
      </form>

      <!-- 切换登录/注册 -->
      <div class="form-footer">
        <p>
          {{ isLogin ? '还没有账户？' : '已有账户？' }}
          <a href="#" @click.prevent="toggleMode" class="toggle-link">
            {{ isLogin ? '立即注册' : '立即登录' }}
          </a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { login, register } from '@/api/user'
import Logo from "@/assets/icons/Logo.vue";

const router = useRouter()
const userStore = useUserStore()

const isLogin = ref(true)
const loading = ref(false)
const errorMessage = ref('')

const formData = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// 切换登录/注册模式
const toggleMode = () => {
  isLogin.value = !isLogin.value
  errorMessage.value = ''
  // 清空表单
  formData.username = ''
  formData.email = ''
  formData.password = ''
  formData.confirmPassword = ''
}

// 表单验证
const validateForm = () => {
  if (!isLogin.value) {
    if (!formData.username.trim()) {
      errorMessage.value = '请输入用户名'
      return false
    }
    if (formData.password !== formData.confirmPassword) {
      errorMessage.value = '两次输入的密码不一致'
      return false
    }
  }

  if (!formData.email.trim()) {
    errorMessage.value = '请输入邮箱'
    return false
  }

  if (formData.password.length < 6) {
    errorMessage.value = '密码长度至少为6位'
    return false
  }

  return true
}

// 提交表单
const handleSubmit = async () => {
  errorMessage.value = ''

  if (!validateForm()) {
    return
  }

  loading.value = true

  try {
    if (isLogin.value) {
      // 登录
      const response = await login({
        username: formData.email,
        password: formData.password
      })

      // 保存用户信息和token
      userStore.setUser(response.user)
      userStore.setToken(response.access_token)

      // 跳转到首页
      await router.push('/home')
    } else {
      // 注册
      const response = await register({
        username: formData.username,
        email: formData.email,
        password: formData.password
      })

      // 保存用户信息和token
      userStore.setUser(response.user)
      userStore.setToken(response.access_token)

      // 跳转到首页
      await router.push('/home')
    }
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || error.message || '操作失败，请重试'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-form-container {
  position: fixed;
  left: 0;
  top: 0;
  width: 33.333%;
  height: 100vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  padding: 2rem;
}

.auth-form {
  width: 100%;
  max-width: 400px;
  animation: fadeIn 0.5s ease-out;
}

.content {
  display: none;
  text-align: center;
  color: var(--color-text-light);
  animation: fadeInUp 1s ease-out;
}

.app-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  letter-spacing: 2px;
  color: var(--color-text-primary);
}

.form-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.form-subtitle {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}

.form-header {
  margin-bottom: 0;
}

.form-group {
  margin-bottom: 1.5rem;
}

/* 标题切换动画 */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

/* 表单字段滑入动画 */
.slide-down-enter-active {
  transition: all 0.3s ease-out;
  overflow: hidden;
}

.slide-down-leave-active {
  transition: all 0.2s ease-in;
  overflow: hidden;
}

.slide-down-enter-from {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
  margin-bottom: 0;
}

.slide-down-enter-to {
  max-height: 100px;
  opacity: 1;
  transform: translateY(0);
}

.slide-down-leave-from {
  max-height: 100px;
  opacity: 1;
  transform: translateY(0);
}

.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
  margin-bottom: 0;
}

/* 错误消息淡入淡出 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid var(--color-border-light);
  border-radius: 8px;
  background-color: var(--color-bg-primary);
  color: var(--color-text-primary);
  transition: all var(--transition-base);
}

.form-group input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.05);
}

.form-group input::placeholder {
  color: var(--color-gray-400);
}

.error-message {
  padding: 0.75rem 1rem;
  background-color: #fee;
  border: 1px solid var(--color-error);
  border-radius: 8px;
  color: var(--color-error);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.submit-btn {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-light);
  background-color: var(--color-primary);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all var(--transition-base);
}

.submit-btn:hover:not(:disabled) {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.form-footer p {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.toggle-link {
  color: var(--color-primary);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transition-fast);
}

.toggle-link:hover {
  color: var(--color-gray-700);
  text-decoration: underline;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .auth-form-container {
    width: 100%;
    justify-content: flex-start;
    background-color: rgba(255, 255, 255, 0.95);
  }
}
</style>
