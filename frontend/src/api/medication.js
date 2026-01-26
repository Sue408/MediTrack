import request from '@/utils/request'

/**
 * 创建药物记录
 * @param {Object} data - 药物数据
 * @param {string} data.name - 药物名称
 * @param {string} data.dosage - 剂量
 * @param {string} data.frequency - 服用频率
 * @param {string} data.start_date - 开始日期
 * @param {string} data.end_date - 结束日期
 * @param {string} data.notes - 备注
 * @returns {Promise}
 */
export const createMedication = (data) => {
  return request({
    url: '/medication',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户的所有药物记录
 * @returns {Promise}
 */
export const getMedications = () => {
  return request({
    url: '/medication',
    method: 'get'
  })
}

/**
 * 获取指定药物记录
 * @param {number} id - 药物ID
 * @returns {Promise}
 */
export const getMedicationById = (id) => {
  return request({
    url: `/medication/${id}`,
    method: 'get'
  })
}

/**
 * 更新药物记录
 * @param {number} id - 药物ID
 * @param {Object} data - 更新数据
 * @returns {Promise}
 */
export const updateMedication = (id, data) => {
  return request({
    url: `/medication/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除药物记录
 * @param {number} id - 药物ID
 * @returns {Promise}
 */
export const deleteMedication = (id) => {
  return request({
    url: `/medication/${id}`,
    method: 'delete'
  })
}
