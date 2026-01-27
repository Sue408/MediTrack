import request from '@/utils/request'

/**
 * 创建药物记录
 * @param {Object} data - 药物数据
 * @param {string} data.name - 药物名称
 * @param {string} data.dosage - 剂量
 * @param {string} data.frequency_type - 频率类型：daily-每日，weekly-每周
 * @param {number} data.times_per_day - 每日服用次数（仅daily类型）
 * @param {Array<string>} data.daily_times - 每日具体服用时间（HH:MM格式，仅daily类型）
 * @param {Array<number>} data.weekly_days - 每周服用的星期几（1-7，仅weekly类型）
 * @param {string} data.start_date - 开始日期
 * @param {string} data.end_date - 结束日期
 * @param {string} data.notes - 备注
 * @param {string} data.photos - 药品照片JSON数组
 * @param {string} data.barcode - 药品条形码
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
