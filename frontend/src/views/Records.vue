<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">用药记录</h1>
      <p class="page-subtitle">查看您的用药历史记录</p>
    </div>
    <div class="placeholder-content">
      <div class="placeholder-icon">📋</div>
      <p class="placeholder-text">用药记录功能开发中...</p>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.page-container {
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

.placeholder-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  background-color: var(--color-bg-primary);
  border-radius: 12px;
  box-shadow: var(--shadow-md);
}

.placeholder-icon {
  font-size: 5rem;
  margin-bottom: 1rem;
}

.placeholder-text {
  font-size: 1.2rem;
  color: var(--color-text-secondary);
}
</style>
