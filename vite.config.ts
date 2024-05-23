import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    // 预处理器配置项
    preprocessorOptions: {
      less: {
        math: "always",
      },
    },
  },
  optimizeDeps: {
    exclude: [
      // 在这里添加你想要排除的文件或文件夹的路径
      './sourceData/bpv-fetal-infer/output_result/output_result_02',
    ],
  },
})
