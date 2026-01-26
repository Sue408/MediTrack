import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 从localStorage恢复用户信息
  const savedUser = localStorage.getItem('user')

  // 状态
  const user = ref(savedUser ? JSON.parse(savedUser) : null)
  const token = ref(localStorage.getItem('token') || null)

  // 设置用户信息
  const setUser = (userData) => {
    user.value = userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
    } else {
      localStorage.removeItem('user')
    }
  }

  // 设置token
  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  // 登出
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 检查是否已登录
  const isAuthenticated = () => {
    return !!token.value
  }

  return {
    user,
    token,
    setUser,
    setToken,
    logout,
    isAuthenticated
  }
})
