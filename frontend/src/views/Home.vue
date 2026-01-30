<template>
  <div class="home-layout">
    <!-- 顶部栏 -->
    <TopBar />

    <!-- 左侧导航栏 -->
    <Sidebar ref="sidebarRef" />

    <!-- 主内容区 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, provide } from 'vue'
import TopBar from '@/components/common/TopBar.vue'
import Sidebar from '@/components/common/Sidebar.vue'

const sidebarRef = ref(null)

// 提供侧边栏切换方法给子组件 (toggleSidebar-用于显示、隐藏侧边栏)
const toggleSidebar = () => {
  sidebarRef.value?.toggleSidebar()
}

provide('toggleSidebar', toggleSidebar)
</script>

<style scoped>
.home-layout {
  min-height: 100vh;
  overflow: hidden;
  background-color: var(--color-bg-secondary);
}

.main-content {
  margin-left: 240px;
  margin-top: 64px;
  min-height: calc(100vh - 64px);
  background-color: var(--color-bg-secondary);
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .home-layout {
    overflow-y: auto;
  }

  .main-content {
    margin-left: 0;
  }
}
</style>
