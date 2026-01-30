import request from '@/utils/request'

/**
 * 搜索外部药物数据库
 * @param {string} query - 搜索关键词
 * @param {string} searchType - 搜索类型：name-名称, barcode-条码, manufacturer-厂家
 * @param {number} limit - 返回结果数量限制
 * @returns {Promise}
 */
export const searchDrugs = (query, searchType = 'name', limit = 10) => {
  return request({
    url: '/third-party',
    method: 'get',
    params: {
      query,
      search_type: searchType,
      limit
    }
  })
}

/**
 * 获取外部数据库中的药物详细信息
 * @param {string} externalDrugId - 外部数据库药物ID
 * @returns {Promise}
 */
export const getDrugDetail = (externalDrugId) => {
  return request({
    url: `third-party/drug-detail/${externalDrugId}`,
    method: 'get'
  })
}

/**
 * 获取药物说明书
 * @param {string} externalDrugId - 外部数据库药物ID
 * @returns {Promise}
 */
export const getInstructionManual = (externalDrugId) => {
  return request({
    url: `third-party/instruction/${externalDrugId}`,
    method: 'get'
  })
}
