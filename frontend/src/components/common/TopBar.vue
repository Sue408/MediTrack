<template>
  <header class="top-bar">
    <div class="left-section">
      <!-- 移动端菜单按钮 -->
      <button class="menu-btn" @click="toggleSidebar">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      <Logo size="40px" />
      <span class="app-name">MediTrack</span>
    </div>
    <div class="right-section">
      <div class="user-info">
        <img v-if="user?.avatar_url" :src="user.avatar_url" alt="头像" class="avatar" />
        <div v-else class="avatar-placeholder">{{ user?.username?.charAt(0).toUpperCase() }}</div>
        <span class="username">{{ user?.username }}</span>
      </div>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </div>
  </header>
</template>

<script setup>
import { computed, inject } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { signOut } from '@/utils/supabase'
import Logo from '@/assets/Logo.vue'
import confirm from '@/utils/confirm'
// 获取路由管理和全局用户状态
const router = useRouter()
const userStore = useUserStore()
// 构造计算类型的响应变量
const user = computed(() => userStore.user)

// 从父组件注入的侧边栏切换方法，用于显示侧边栏
const toggleSidebar = inject('toggleSidebar', () => {})

// 登出方法
const handleLogout = async () => {
  try {
    await confirm.warning(
      '确定要退出登录吗？',
      '退出登录'
    )

    // 清除 Supabase session
    await signOut()

    // 清除本地状态
    userStore.logout()

    // 跳转到登录页
    router.push('/auth')
  } catch (error) {
    // 用户取消操作
    if (error.message === '用户取消') {
      return
    }
    console.error('登出失败:', error)
  }
}
</script>

<style scoped>
.top-bar {
  height: 64px;
  background-color: var(--color-bg-primary);
  border-bottom: 1px solid var(--color-border-light);
  box-shadow: var(--shadow-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 2rem;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* 菜单按钮 */
.menu-btn {
  display: none;
  width: 40px;
  height: 40px;
  padding: 0;
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: var(--color-text-primary);
  transition: all var(--transition-base);
  border-radius: 6px;
}

.menu-btn:hover {
  background-color: var(--color-gray-100);
}

.menu-btn:active {
  transform: scale(0.95);
}

.menu-btn svg {
  width: 24px;
  height: 24px;
}

.app-name {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  user-select: none;
}

.right-section {
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

/* 响应式设计 */
@media (max-width: 768px) {
  .top-bar {
    padding: 0 1rem;
  }

  .menu-btn {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .app-name {
    display: none;
  }

  .username {
    display: none;
  }

  .logout-btn {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
  }
}
</style>
