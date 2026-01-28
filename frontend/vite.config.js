import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  // 加载环境变量
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [
      vue(),
      vueDevTools(),
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      host: env.VITE_HOST || '0.0.0.0',
      port: parseInt(env.VITE_PORT) || 5173,
      strictPort: false,

      // 允许所有主机访问（支持 cpolar 等内网穿透工具）
      // 使用数组形式以兼容更多场景
      allowedHosts: [
        '.cpolar.cn',      // cpolar 域名通配符
        '.cpolar.top',     // cpolar 备用域名
        'localhost',       // 本地访问
        '.local',          // 局域网 .local 域名
      ],

      // 禁用 host 检查（开发环境）
      hmr: {
        clientPort: parseInt(env.VITE_PORT) || 5173,
      },

      // API 代理配置
      // 将 /api/* 请求代理到后端服务器
      proxy: {
        '/api': {
          target: env.VITE_PROXY_TARGET || 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          // 添加调试信息
          configure: (proxy, options) => {
            proxy.on('error', (err, req, res) => {
              console.log('代理错误:', err)
            })
            proxy.on('proxyReq', (proxyReq, req, res) => {
              console.log('代理请求:', req.method, req.url, '→', options.target + req.url.replace(/^\/api/, ''))
            })
          }
        }
      }
    }
  }
})
