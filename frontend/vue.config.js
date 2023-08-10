const { defineConfig } = require('@vue/cli-service')
const { VuetifyPlugin } = require('webpack-plugin-vuetify')
const ip = process.env.FRONTEND_SERVER_IP || 'localhost'
const port = process.env.FRONTEND_SERVER_PORT || 8080
const mode = process.env.NODE_ENV
const isProduction = mode === 'production'
const prodStaticUrlPrefix = '/static'
const parseBool = (b) => {
  return !/^(f|false|n|no|0)$/i.test(b) && !!b
}

process.env.VUE_APP_SENTRY_DSN = process.env.SENTRY_DSN_FRONTEND
const encryptionEnabled = parseBool(process.env.VUE_APP_ENABLE_ENCRYPTION)
const decryptionKey = process.env.VUE_APP_DECRYPTION_KEY

class StartError extends Error {
  constructor(message) {
    super(message)
    this.name = 'Start error'
  }
}

if (encryptionEnabled && !decryptionKey) {
  throw new StartError(
    'Encryption enabled, but decryption key not provided! Set VUE_APP_DECRYPTION_KEY environment variable'
  )
}

module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: isProduction ? `${prodStaticUrlPrefix}/` : `http://${ip}:${port}`,
  indexPath: './public/index.html',
  outputDir: './dist/',
  runtimeCompiler: true,
  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config
      .plugin('VuetifyPlugin')
      .use(VuetifyPlugin, [{ styles: { configFile: './src/shared/assets/styles/variables.scss' } }])

    config.resolve.set('symlinks', false)

    config.resolve.alias.set('__STATIC__', 'static')

    config.devServer
      .host('0.0.0.0')
      .port(port)
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['*'] })
  },

  devServer: {
    historyApiFallback: true,
    devMiddleware: {
      publicPath: '/',
    },
    client: {
      overlay: {
        warnings: true,
        errors: true,
      },
    },
    static: {
      publicPath: `http://0.0.0.0:${port}`,
      watch: true,
    },
    hot: 'only',
  },
  pluginOptions: {
    i18n: {
      locale: 'ru',
      fallbackLocale: 'ru',
      localeDir: 'languages',
      enableInSFC: true,
    },
  },
  // generate sourceMap for production build?
  productionSourceMap: isProduction,
})
