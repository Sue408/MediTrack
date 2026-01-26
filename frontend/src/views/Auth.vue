<template>
  <div class="auth-page">
    <AuthBack />
    <AuthForm />
  </div>
</template>

<script setup>
import AuthBack from '@/components/AuthBack.vue'
import AuthForm from '@/components/AuthForm.vue'
</script>

<style scoped>
.auth-page {
  position: relative;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  user-select: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

/* 允许表单输入框可以选择和复制 */
.auth-page :deep(input),
.auth-page :deep(textarea) {
  user-select: text;
  -webkit-user-select: text;
  -moz-user-select: text;
  -ms-user-select: text;
}
</style>
