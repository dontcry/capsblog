const path = require('path');
const webpack = require('webpack')
const merge = require('webpack-merge');
const package = require('./package.json');
const common = require('./webpack.common.js')
const HtmlWebpackPlugin = require('html-webpack-plugin') 
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
 
const plugins = [
    new CleanWebpackPlugin(), 
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
        path: path.resolve(__dirname, 'dist/js/')
    },
    optimization: {
        removeEmptyChunks: true,
        minimize: true,
        minimizer: [new OptimizeCSSAssetsPlugin({})], 
    },
    // devtool: 'source-map',
    mode: 'production',
    plugins: plugins
} 
 
options.module = {
    rules: [
        {
            test: /\.(le|c)ss$/,
            use: [
                {
                    loader: MiniCssExtractPlugin.loader,
                },
                'css-loader',
                'postcss-loader',
                'less-loader',
            ],
        } 
    ],
};
module.exports = merge(common, options); 