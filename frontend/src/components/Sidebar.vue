<template>
  <!-- 遮罩层 (移动端) -->
  <transition name="fade">
    <div v-if="isOpen && isMobile" class="sidebar-overlay" @click="closeSidebar"></div>
  </transition>

  <!-- 侧边栏 -->
  <aside class="sidebar" :class="{ 'sidebar-open': isOpen }">
    <nav class="nav-menu">
      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="nav-item"
        active-class="active"
        @click="handleNavClick"
      >
        <span class="nav-icon">
          <!-- 用户图标 -->
          <svg v-if="item.icon === 'user'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
          <!-- 药丸图标 -->
          <svg v-else-if="item.icon === 'pill'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10.5 20.5 10 21a2 2 0 0 1-2.828 0L4.343 18.172a2 2 0 0 1 0-2.828l.5-.5"></path>
            <path d="m14.5 3.5.5-.5a2 2 0 0 1 2.828 0l2.829 2.828a2 2 0 0 1 0 2.828l-.5.5"></path>
            <path d="M7.778 15.778 18 5.556"></path>
            <path d="m7 13 2-2"></path>
            <path d="m10 16 2-2"></path>
            <path d="m13 19 2-2"></path>
          </svg>
          <!-- 时钟图标 -->
          <svg v-else-if="item.icon === 'clock'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          <!-- 剪贴板图标 -->
          <svg v-else-if="item.icon === 'clipboard'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path>
            <rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect>
          </svg>
          <!-- 图表图标 -->
          <svg v-else-if="item.icon === 'chart'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="20" x2="18" y2="10"></line>
            <line x1="12" y1="20" x2="12" y2="4"></line>
            <line x1="6" y1="20" x2="6" y2="14"></line>
          </svg>
        </span>
        <span class="nav-text">{{ item.name }}</span>
      </router-link>
    </nav>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineExpose } from 'vue'

const menuItems = ref([
  {
    name: '个人信息',
    path: '/home/profile',
    icon: 'user'
  },
  {
    name: '药物管理',
    path: '/home/medicines',
    icon: 'pill'
  },
  {
    name: '用药提醒',
    path: '/home/reminders',
    icon: 'clock'
  },
  {
    name: '用药记录',
    path: '/home/records',
    icon: 'clipboard'
  },
  {
    name: '数据统计',
    path: '/home/statistics',
    icon: 'chart'
  }
])

const isOpen = ref(false)
const isMobile = ref(false)

// 检查是否为移动端
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    isOpen.value = false
  }
}

// 切换侧边栏
const toggleSidebar = () => {
  isOpen.value = !isOpen.value
}

// 关闭侧边栏
const closeSidebar = () => {
  isOpen.value = false
}

// 导航点击处理（移动端自动关闭）
const handleNavClick = () => {
  if (isMobile.value) {
    closeSidebar()
  }
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

// 暴露方法给父组件
defineExpose({
  toggleSidebar
})
</script>

<style scoped>
/* 遮罩层 */
.sidebar-overlay {
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 49;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 侧边栏 */
.sidebar {
  width: 240px;
  background-color: var(--color-bg-primary);
  border-right: 1px solid var(--color-border-light);
  height: calc(100vh - 64px);
  position: fixed;
  top: 64px;
  left: 0;
  overflow-y: auto;
  z-index: 50;
  transition: transform 0.3s ease;
}

.nav-menu {
  padding: 1.5rem 0;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all var(--transition-base);
  border-left: 3px solid transparent;
  user-select: none;
}

.nav-item:hover {
  background-color: var(--color-gray-50);
  color: var(--color-text-primary);
}

.nav-item:hover .nav-icon {
  transform: scale(1.1);
}

.nav-item.active {
  background-color: var(--color-gray-100);
  color: var(--color-primary);
  border-left-color: var(--color-primary);
  font-weight: 600;
}

.nav-icon {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-base);
}

.nav-icon svg {
  width: 100%;
  height: 100%;
}

.nav-text {
  font-size: 1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
    box-shadow: var(--shadow-lg);
  }

  .sidebar.sidebar-open {
    transform: translateX(0);
  }
}
</style>
