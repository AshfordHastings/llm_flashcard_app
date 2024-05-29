const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
    mode: 'development',
    entry: {
      index: './src/index.js',
    },
    output: {
      path: path.resolve(__dirname, 'dist'),
      publicPath: '/',
      clean: true,
      filename: '[name].bundle.js'
    },
    devServer: {
      contentBase: './dist',
    },
    module: {
      rules: [
        {
          test: /\.(js|jsx)$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        },
        {
          test: /\.css$/i,
          use: ['style-loader', 'css-loader']
      },
      ]
    },
    devtool: 'inline-source-map',
    plugins: [
      new HtmlWebpackPlugin({
        title: 'Development',
        template: './src/index.html'
      })
    ]
  };