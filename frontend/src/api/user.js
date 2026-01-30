import request from '@/utils/request'

/**
 * 获取当前用户信息
 * @returns {Promise}
 */
export const getUserInfo = () => {
  return request({
    url: '/users/me',
    method: 'get'
  })
}

/**
 * 更新当前用户信息
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export const updateUserInfo = (data) => {
  return request({
    url: '/users/me',
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
    url: '/users/avatar',
    method: 'post',
    data
  })
}
