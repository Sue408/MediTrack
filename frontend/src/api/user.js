import request from '@/utils/request'

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @param {string} data.username - 用户名
 * @param {string} data.email - 邮箱
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const register = (data) => {
  return request({
    url: '/user/register',
    method: 'post',
    data
  })
}

/**
 * 用户登录
 * @param {Object} data - 登录数据
 * @param {string} data.username - 用户名或邮箱
 * @param {string} data.password - 密码
 * @returns {Promise}
 */
export const login = (data) => {
  return request({
    url: '/user/login',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export const getCurrentUser = () => {
  return request({
    url: '/user/me',
    method: 'get'
  })
}

/**
 * 更新当前用户信息
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export const updateCurrentUser = (data) => {
  return request({
    url: '/user/me',
    method: 'put',
    data
  })
}

/**
 * 上传用户头像
 * @param {Object} data - 头像数据
 * @param {string} data.avatar - Base64编码的头像
 * @returns {Promise}
 */
export const uploadAvatar = (data) => {
  return request({
    url: '/user/avatar',
    method: 'post',
    data
  })
}
