
const BundleTracker = require('webpack-bundle-tracker');
const path = require('path');

module.exports = {
  // publicPath: process.env.VUE_APP_ENV === 'local' ? 'http://0.0.0.0:8080/' : '/static/',
  publicPath: 'http://localhost:8080/',
  outputDir: './dist/',

  chainWebpack: config => {

    config
      .plugin('BundleTracker')
      .use(BundleTracker, [{ filename: './dist/webpack-stats.json' }]);

    config.optimization
      .splitChunks(false);

    config.resolve.alias.set('vue$', 'vue/dist/vue.js');
    config.resolve.alias.set('@', path.resolve(__dirname + '/src'));
    config.resolve.alias.set('__STATIC__', 'static');

    config.devServer
      .public('http://localhost:8080')
      .host('localhost')
      .port(8080)
      // .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['*'] });
  },
};
