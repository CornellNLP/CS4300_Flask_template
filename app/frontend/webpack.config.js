const webpack = require('webpack');
const config = {
    entry:  __dirname + '/src/index.jsx',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css'],
    },
    module: {
      rules: [
        {
          test: /\.jsx?/,
          exclude: /node_modules/,
          loader: 'babel-loader',
          query: {
            presets:['react', 'es2015']
          }
        },
        {
          test: /\.css$/,
          exclude: /node_modules/,
          loaders: ['style-loader', 'css-loader'],
        },
        {
          test: /\.(eot|svg|ttf|woff|woff2)$/,
          loader: 'file-loader'
        }
      ]
    },
    devtool: '#eval-source-map'
};
module.exports = config;