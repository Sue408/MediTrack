<template>
  <div class="home-page">
    <header class="header">
      <div class="header-content">
        <div class="logo-section">
          <Logo size="40px" />
          <span class="app-name">MediTrack</span>
        </div>
        <div class="user-section">
          <div class="user-info">
            <img v-if="user?.avatar" :src="user.avatar" alt="头像" class="avatar" />
            <div v-else class="avatar-placeholder">{{ user?.username?.charAt(0).toUpperCase() }}</div>
            <span class="username">{{ user?.username }}</span>
          </div>
          <button @click="handleLogout" class="logout-btn">退出登录</button>
        </div>
      </div>
    </header>

    <main class="main-content">
      <div class="welcome-section">
        <h1>欢迎使用 MediTrack</h1>
        <p class="subtitle">您已成功登录系统</p>

        <div class="info-cards">
          <div class="info-card">
            <h3>用户信息</h3>
            <div class="info-item">
              <span class="label">用户名：</span>
              <span class="value">{{ user?.username }}</span>
            </div>
            <div class="info-item">
              <span class="label">邮箱：</span>
              <span class="value">{{ user?.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">账户状态：</span>
              <span class="value status-active">{{ user?.is_active ? '正常' : '未激活' }}</span>
            </div>
          </div>

          <div class="info-card">
            <h3>快速开始</h3>
            <p>这是一个测试页面，用于验证登录功能是否正常工作。</p>
            <p>后续将在此基础上开发完整的药物管理功能。</p>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Logo from '@/assets/Logo.vue'

const router = useRouter()
const userStore = useUserStore()

const user = computed(() => userStore.user)

const handleLogout = () => {
  userStore.logout()
  router.push('/auth')
}
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background-color: var(--color-bg-secondary);
}

.header {
  background-color: var(--color-bg-primary);
  border-bottom: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-sm);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.app-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
}

.user-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--color-border-light);
}

.avatar-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--color-gray-800);
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.2rem;
}

.username {
  font-weight: 500;
  color: var(--color-text-primary);
}

.logout-btn {
  padding: 0.5rem 1.5rem;
  background-color: var(--color-primary);
  color: var(--color-text-light);
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-base);
}

.logout-btn:hover {
  background-color: var(--color-gray-800);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.welcome-section {
  text-align: center;
}

.welcome-section h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: var(--color-text-secondary);
  margin-bottom: 3rem;
}

.info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
  text-align: left;
}

.info-card {
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  padding: 2rem;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-base);
}

.info-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.info-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1.5rem;
  padding-bottom: 0.75rem;
  border-bottom: 2px solid var(--color-border-light);
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--color-border-light);
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  font-weight: 500;
  color: var(--color-text-secondary);
}

.info-item .value {
  font-weight: 600;
  color: var(--color-text-primary);
}

.status-active {
  color: var(--color-success);
}

.info-card p {
  color: var(--color-text-secondary);
  line-height: 1.8;
  margin-bottom: 1rem;
}

.info-card p:last-child {
  margin-bottom: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 1rem;
  }

  .welcome-section h1 {
    font-size: 2rem;
  }

  .info-cards {
    grid-template-columns: 1fr;
  }
}
</style>
