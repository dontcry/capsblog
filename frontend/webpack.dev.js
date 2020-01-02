const path = require('path')
const webpack = require('webpack')
const merge = require('webpack-merge')
const common = require('./webpack.common.js')
const HtmlWebpackPlugin = require('html-webpack-plugin')

const plugins = [
    new webpack.NamedModulesPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new HtmlWebpackPlugin({
        template: path.join(__dirname, `/src/index.html`),
        filename: path.join(__dirname, `/dist/index.html`),
    })
]
const options = {
    entry: __dirname + "/src/index.jsx",
    output: {
        filename: '[name].bundle.js',
        path: path.resolve(__dirname, 'dist/')
    },
    devtool: 'inline-source-map',
    devServer: {
        // host: '192.168.101.63',
        // port: 8082,
        quiet: false,
        contentBase: './dist',
        hot: true
    },
    plugins: plugins
}
options.module = {
    rules: [{
            test: /\.css$/,
            use: ['style-loader', 'css-loader', 'postcss-loader'],
        },
        {
            test: /\.less$/,
            use: [
                'style-loader',
                'css-loader',
                'postcss-loader',
                'less-loader'
            ]
        },
    ],
};
module.exports = merge(common, options)