const path = require('path');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const extractSass = new ExtractTextPlugin('css/styles.css');

module.exports = {
  devtool: 'eval',
  entry: [path.join(__dirname, 'js/browser.js')],
  output: {
    path: path.join(__dirname, '../app/static/js'),
    publicPath: '/static/',
    filename: 'js/bundle.js'
  },
  devServer: {
    historyApiFallback: true,
    proxy: { '*': 'http://localhost:5000' }
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        exclude: /(node_modules)/
      },
      {
        test: /\.scss$/,
        use: extractSass.extract({
          use: [
            { loader: 'css-loader' },
            { loader: 'sass-loader' }
          ]
        })
      },
      {
        test: /\.jpe?g$|\.gif$|\.png$/i,
        loader: 'file-loader?name=images/[name].[ext]'
      }
    ]
  },
  plugins: [
    extractSass
  ]
};
