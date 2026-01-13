const path = require('path');
// Uncomment to enable bundle analysis
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
   

module.exports = {
  filenameHashing: false,
  runtimeCompiler: true,
  publicPath: '/static/',
  outputDir: path.resolve('./static/compiled/'),
  productionSourceMap: false,
  css: {
    extract: true,
  },
  // Uncomment to enable bundle analysis
  // configureWebpack: {
  //    plugins: [new BundleAnalyzerPlugin()]
  // },
  chainWebpack: (config) => {
    // console.log(config)
    // Don't write to disk with hot reload files
    config.plugins.delete('hmr');
    // Remove html generation
    config.plugins.delete('html');
    config.plugins.delete('preload');
    config.plugins.delete('prefetch');
    // If you wish to remove the standard entry point
    config.entryPoints.delete('app');

    // then add your own

    config.entry('home').add('./src/home.entry.js').end();
    
    // config.entry('app').add('./src/app.entry.js').end();
    // config
    //   .entry('framework')
    //   .add('./src/framework.entry.js')
    //   .end();

    // config
    //   .entry('library')
    //   .add('./src/library.entry.js')
    //   .end();

    // config
    //   .entry('reports')
    //   .add('./src/reports.entry.js')
    //   .end();

    // config
    //   .entry('sources')
    //   .add('./src/sources.entry.js')
    //   .end();

    // config
    //   .entry('dashboard')
    //   .add('./src/dashboard.entry.js')
    //   .end();

    // // admin pages
    // config.entry('users').add('./src/users.entry.js').end();

    // config.entry('teams').add('./src/teams.entry.js').end();

    // // account pages
    // config
    //   .entry('account')
    //   .add('./src/account.entry.js')
    //   .end();

    // config
    //   .entry('auth')
    //   .add('./src/auth.entry.js')
    //   .end();

    // config
    //   .entry('inbox')
    //   .add('./src/inbox.entry.js')
    //   .end();

    config.optimization.splitChunks({
      chunks: 'all',
      cacheGroups: {
        common: {
          name: 'common',
          chunks: 'initial',
          minChunks: 1,
        },
      },
    });
  },
};
