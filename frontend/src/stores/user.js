import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 从localStorage恢复用户信息
  const savedUser = localStorage.getItem('user')
  const savedToken = localStorage.getItem('token')

  console.log('UserStore初始化 - savedUser:', savedUser ? 'exists' : 'null')
  console.log('UserStore初始化 - savedToken:', savedToken ? `${savedToken.substring(0, 20)}...` : 'null')

  // 状态
  const user = ref(savedUser ? JSON.parse(savedUser) : null)
  const token = ref(savedToken || null)

  // 设置用户信息
  const setUser = (userData) => {
    console.log('setUser调用 - userData:', userData)
    user.value = userData
    if (userData) {
      localStorage.setItem('user', JSON.stringify(userData))
      console.log('setUser - 已保存到localStorage')
    } else {
      localStorage.removeItem('user')
      console.log('setUser - 已从localStorage移除')
    }
  }

  // 设置token
  const setToken = (newToken) => {
    console.log('setToken调用 - newToken:', newToken ? `${newToken.substring(0, 20)}...` : 'null')
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
      console.log('setToken - 已保存到localStorage')
      console.log('setToken - 验证localStorage:', localStorage.getItem('token') ? 'success' : 'failed')
    } else {
      localStorage.removeItem('token')
      console.log('setToken - 已从localStorage移除')
    }
  }

  // 登出
  const logout = () => {
    console.log('logout调用')
    user.value = null
    token.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  // 检查是否已登录
  const isAuthenticated = () => {
    const result = !!token.value
    console.log('isAuthenticated调用 - result:', result, 'token.value:', token.value ? 'exists' : 'null')
    return result
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
