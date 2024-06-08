import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import inject from '@rollup/plugin-inject'

import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    inject({
      $: 'jquery',
      jQuery: 'jquery',
      'window.jQuery': 'jquery',
    }),
    AutoImport({ // JS按需引入
      imports: [
        'vue',
        'vue-router',
        'pinia',
        {from: 'echarts', imports: [['*','echarts'],]},
      ],
      resolvers: [ElementPlusResolver()],
      dirs: [
        './src/api/**',
        './src/json/**',
      ],
      dts: 'src/auto-imports.d.ts',
      vueTemplate: true,
      injectAtEnd: true,
      eslintrc: {
        enabled: true,
      }
    }),
    Components({ // 组件自动引入
      dirs: ['src/components'],
      extensions: ['vue'],
      deep: true,
      resolvers: [ElementPlusResolver()],
      dts: 'src/components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  // 配置服务器映射
  server: {
    host: '0.0.0.0',
    port: 14514,
    open: true,
  },
})
