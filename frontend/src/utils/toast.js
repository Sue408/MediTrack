import { createApp } from 'vue'
import Toast from '@/assets/Toast.vue'

let toastInstance = null
let toastApp = null

/**
 * 显示Toast提示
 * @param {Object} options - 配置选项
 * @param {string} options.message - 提示消息
 * @param {string} options.type - 类型：success, error, warning, info
 * @param {number} options.duration - 显示时长（毫秒）
 */
export function showToast({ message, type = 'info', duration = 3000 }) {
  // 如果已有实例，先销毁
  if (toastInstance) {
    hideToast()
  }

  // 创建容器 (用于挂载Vue应用)
  const container = document.createElement('div')
  document.body.appendChild(container)

  // 创建Vue应用实例 (组件、属性对象)
  toastApp = createApp(Toast, {
    message,
    type,
    duration,
    onClose: () => {
      hideToast()
    }
  })

  // 挂载
  toastInstance = toastApp.mount(container)

  return toastInstance
}

/**
 * 隐藏Toast
 */
export function hideToast() {
  if (toastApp && toastInstance) {
    setTimeout(() => {
      toastApp?.unmount()
      const container = document.querySelector('body > div:last-child')
      if (container) {
        document.body.removeChild(container)
      }
      toastApp = null
      toastInstance = null
    }, 300) // 等待动画完成
  }
}

/**
 * 快捷方法
 */
export const toast = {
  success: (message, duration) => showToast({ message, type: 'success', duration }),
  error: (message, duration) => showToast({ message, type: 'error', duration }),
  warning: (message, duration) => showToast({ message, type: 'warning', duration }),
  info: (message, duration) => showToast({ message, type: 'info', duration })
}

export default toast
