const { defineConfig } = require('@vue/cli-service');
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/users': {
        target: 'http://backend:8000', // Сервис Backend в Docker Compose
        changeOrigin: true,
      },
      '/posts': {
        target: 'http://backend:8000', // Сервис Backend в Docker Compose
        changeOrigin: true,
      },
    },
  },
});