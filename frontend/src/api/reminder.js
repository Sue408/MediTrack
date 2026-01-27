import request from '@/utils/request'

/**
 * 生成未来N天的用药记录
 * @param {number} days - 生成天数（1-90）
 * @returns {Promise}
 */
export const generateRecords = (days = 7) => {
  return request({
    url: '/reminder/generate',
    method: 'post',
    data: { days }
  })
}

/**
 * 获取指定日期的用药记录
 * @param {string} date - 日期（YYYY-MM-DD格式），不传则默认今天
 * @returns {Promise}
 */
export const getRecordsByDate = (date) => {
  return request({
    url: '/reminder/records',
    method: 'get',
    params: date ? { target_date: date } : {}
  })
}

/**
 * 获取日期范围内的用药记录
 * @param {string} startDate - 开始日期（YYYY-MM-DD格式）
 * @param {string} endDate - 结束日期（YYYY-MM-DD格式）
 * @returns {Promise}
 */
export const getRecordsByRange = (startDate, endDate) => {
  return request({
    url: '/reminder/records/range',
    method: 'get',
    params: {
      start_date: startDate,
      end_date: endDate
    }
  })
}

/**
 * 标记用药记录为已完成
 * @param {number} recordId - 记录ID
 * @returns {Promise}
 */
export const completeRecord = (recordId) => {
  return request({
    url: `/reminder/records/${recordId}/complete`,
    method: 'put'
  })
}

/**
 * 取消用药记录的完成状态
 * @param {number} recordId - 记录ID
 * @returns {Promise}
 */
export const uncompleteRecord = (recordId) => {
  return request({
    url: `/reminder/records/${recordId}/uncomplete`,
    method: 'put'
  })
}
