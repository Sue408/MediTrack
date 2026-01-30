/**
 * Supabase客户端初始化和认证工具
 */
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('缺少Supabase配置，请检查.env文件')
}

// 创建Supabase客户端
export const supabase = createClient(supabaseUrl, supabaseAnonKey)

/**
 * 用户注册
 * @param {string} email - 邮箱
 * @param {string} password - 密码
 * @param {string} username - 用户名
 * @param {string} fullName - 真实姓名
 * @returns {Promise<{user, session, error}>}
 */
export async function signUp(email, password, username, fullName = '') {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: {
        username,
        full_name: fullName
      }
    }
  })

  return { user: data.user, session: data.session, error }
}

/**
 * 用户登录
 * @param {string} email - 邮箱
 * @param {string} password - 密码
 * @returns {Promise<{user, session, error}>}
 */
export async function signIn(email, password) {
  const { data, error } = await supabase.auth.signInWithPassword({
    email,
    password
  })

  return { user: data.user, session: data.session, error }
}

/**
 * 用户登出
 * @returns {Promise<{error}>}
 */
export async function signOut() {
  const { error } = await supabase.auth.signOut()
  return { error }
}

/**
 * 获取当前会话
 * @returns {Promise<{session, error}>}
 */
export async function getSession() {
  const { data, error } = await supabase.auth.getSession()
  return { session: data.session, error }
}

/**
 * 获取当前用户
 * @returns {Promise<{user, error}>}
 */
export async function getCurrentUser() {
  const { data, error } = await supabase.auth.getUser()
  return { user: data.user, error }
}

/**
 * 刷新会话
 * @returns {Promise<{session, error}>}
 */
export async function refreshSession() {
  const { data, error } = await supabase.auth.refreshSession()
  return { session: data.session, error }
}

/**
 * 监听认证状态变化
 * @param {Function} callback - 回调函数
 * @returns {Object} 订阅对象
 */
export function onAuthStateChange(callback) {
  return supabase.auth.onAuthStateChange(callback)
}

/**
 * 获取访问令牌
 * @returns {Promise<string|null>}
 */
export async function getAccessToken() {
  const { session } = await getSession()
  return session?.access_token || null
}
