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
        replace
      >
        <span class="nav-icon">
          <img :src="`/icons/${item.icon}.svg`" :alt="item.name" />
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

// 导航点击处理（移动端会触发自动关闭）
const handleNavClick = () => {
  if (isMobile.value) {
    closeSidebar()
  }
}

onMounted(() => {
  checkMobile() // 挂载时自动检查是否为移动端
  window.addEventListener('resize', checkMobile) // 监听窗口尺寸变化实时检查是否为移动端S
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile) // 卸载时移除监听事件
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

.nav-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
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
