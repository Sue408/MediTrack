import axios from 'axios'
import { getAccessToken, refreshSession } from './supabase'

// 创建axios实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api', // 后端API地址
  timeout: 10000, // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  async (config) => {
    // 从Supabase获取token
    const token = await getAccessToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    // 处理错误响应
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 尝试刷新token
          const { session, error: refreshError } = await refreshSession()
          if (session) {
            // 刷新成功，重试请求
            const token = session.access_token
            error.config.headers.Authorization = `Bearer ${token}`
            return axios.request(error.config)
          } else {
            // 刷新失败，跳转到登录页
            window.location.href = '/auth'
          }
          break
        case 403:
          console.error('没有权限访问')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 500:
          console.error('服务器错误')
          break
      }
    } else if (error.request) {
      console.error('网络错误，请检查网络连接')
    }
    return Promise.reject(error)
  }
)

export default request
