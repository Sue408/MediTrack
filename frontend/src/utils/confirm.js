import { createApp } from 'vue'
import Confirm from '@/assets/Confirm.vue'

let confirmInstance = null
let confirmApp = null
let confirmContainer = null
let isClosing = false

/**
 * 显示确认弹窗
 * @param {Object} options - 配置选项
 * @param {string} options.title - 标题
 * @param {string} options.message - 消息内容
 * @param {string} options.type - 类型：warning, danger, info
 * @param {string} options.confirmText - 确认按钮文本
 * @param {string} options.cancelText - 取消按钮文本
 * @returns {Promise} - 返回Promise，确认时resolve，取消时reject
 */
export function showConfirm({
  title = '确认操作',
  message,
  type = 'warning',
  confirmText = '确定',
  cancelText = '取消'
}) {
  return new Promise((resolve, reject) => {
    // 如果已有实例，先销毁
    if (confirmInstance && !isClosing) {
      hideConfirm()
    }

    // 创建容器
    confirmContainer = document.createElement('div')
    document.body.appendChild(confirmContainer)

    // 创建Vue应用实例
    confirmApp = createApp(Confirm, {
      title,
      message,
      type,
      confirmText,
      cancelText,
      onConfirm: () => {
        resolve()
        hideConfirm()
      },
      onCancel: () => {
        reject(new Error('用户取消'))
        hideConfirm()
      },
      onClose: () => {
        reject(new Error('用户取消'))
        hideConfirm()
      }
    })

    // 挂载并设置正在加载为false
    confirmInstance = confirmApp.mount(confirmContainer)
    isClosing = false
  })
}

/**
 * 隐藏确认弹窗
 */
export function hideConfirm() {
  // 防止重复调用
  if (isClosing || !confirmApp || !confirmInstance) {
    return
  }

  isClosing = true
  try {
      if (confirmApp) {
        confirmApp.unmount()
      }
      if (confirmContainer && confirmContainer.parentNode) {
        document.body.removeChild(confirmContainer)
      }
    } catch (error) {
      console.error('关闭确认弹窗时出错：', error)
    } finally {
      confirmApp = null
      confirmInstance = null
      confirmContainer = null
      isClosing = false
    }
  }

/**
 * 快捷方法
 */
export const confirm = {
  // 警告确认
  warning: (message, title = '警告') =>
    showConfirm({ message, title, type: 'warning' }),

  // 危险确认（删除等操作）
  danger: (message, title = '危险操作') =>
    showConfirm({ message, title, type: 'danger', confirmText: '确认删除' }),

  // 信息确认
  info: (message, title = '提示') =>
    showConfirm({ message, title, type: 'info' }),

  // 自定义确认
  custom: (options) => showConfirm(options)
}

export default confirm
