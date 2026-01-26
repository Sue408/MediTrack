<template>
  <div class="auth-back">
    <!-- 左侧纯色区域 -->
    <div class="left-section"></div>

    <!-- 右侧展示区域 -->
    <div class="right-section">
      <div class="content">
        <Logo size="120px" color="var(--color-primary)" />
        <h1 class="app-title">MediTrack</h1>
        <p class="app-description">
          智能药物管理平台
        </p>
        <p class="app-subtitle">
          让健康管理更简单、更高效
        </p>
      </div>
    </div>

    <!-- SVG曲线分隔 -->
    <svg class="divider" viewBox="0 0 100 100" preserveAspectRatio="none">
      <!-- 主多边形 - 白色区域延伸 -->
      <path
        class="main-curve"
        d="M 0,0
           L 0,100
           C 25,90 35,75 45,60
           C 55,45 65,30 75,20
           C 85,10 92,5 100,0
           L 0,0
           Z"
        fill="var(--color-bg-primary)"
      />
      <!-- 半透明渐变遮罩层 -->
      <defs>
        <linearGradient id="curveGradient" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" style="stop-color:var(--color-bg-primary);stop-opacity:1" />
          <stop offset="70%" style="stop-color:var(--color-bg-primary);stop-opacity:0.3" />
          <stop offset="100%" style="stop-color:var(--color-bg-primary);stop-opacity:0" />
        </linearGradient>
      </defs>
      <path
        class="gradient-overlay"
        d="M 0,0
           L 0,100
           C 25,90 35,75 45,60
           C 55,45 65,30 75,20
           C 85,10 92,5 100,0
           L 0,0
           Z"
        fill="url(#curveGradient)"
      />
      <!-- 边缘高光线 -->
      <path
        class="edge-highlight"
        d="M 0,100
           C 25,90 35,75 45,60
           C 55,45 65,30 75,20
           C 85,10 92,5 100,0"
        stroke="var(--color-gray-200)"
        stroke-width="0.5"
        fill="none"
        opacity="0.6"
      />
    </svg>
  </div>
</template>

<script setup>
import Logo from '@/assets/Logo.vue'
</script>

<style scoped>
.auth-back {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  overflow: hidden;
}

/* 左侧区域 - 占1/3 */
.left-section {
  flex: 1;
  background-color: var(--color-bg-primary);
  position: relative;
  z-index: 1;
}

/* 右侧区域 - 占2/3 */
.right-section {
  flex: 2;
  background: linear-gradient(135deg, var(--color-gray-900) 0%, var(--color-gray-800) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  z-index: 1;
}

.right-section .content {
  text-align: center;
  color: var(--color-text-light);
  animation: fadeInUp 1s ease-out;
}

.app-title {
  font-size: 3rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  letter-spacing: 2px;
  color: var(--color-secondary);
}

.app-description {
  font-size: 1.5rem;
  font-weight: 300;
  margin-bottom: 1rem;
  color: var(--color-gray-300);
}

.app-subtitle {
  font-size: 1rem;
  color: var(--color-gray-400);
  font-weight: 300;
}

/* SVG曲线分隔 */
.divider {
  position: absolute;
  left: 33.333%;
  top: 0;
  width: 120px;
  height: 100%;
  z-index: 2;
  pointer-events: none;
}

/* 主曲线 */
.main-curve {
  transition: transform var(--transition-slow);
}

/* 渐变遮罩层动画 */
.gradient-overlay {
  animation: gradientFlow 8s ease-in-out infinite;
}

/* 边缘高光线动画 */
.edge-highlight {
  animation: edgeGlow 4s ease-in-out infinite;
}

@keyframes gradientFlow {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes edgeGlow {
  0%, 100% {
    opacity: 0.6;
    stroke-width: 0.5;
  }
  50% {
    opacity: 0.3;
    stroke-width: 0.8;
  }
}

/* 动画 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .auth-back {
    display: none;
  }
}
</style>
