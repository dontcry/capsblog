const path = require('path')
const plugins = []
let options = {
    module: {
        rules: [ 
            {   test: /\.js|jsx$/, 
                use: 'babel-loader',
                exclude: /node_modules/ },
            {
                test: /\.(html)$/,
                use: {
                    loader: 'html-loader',
                    options: {
                        attrs: [':data-src']
                    }
                }
            },
            {
                test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                            name: 'demo/images/[name].[hash:7].[ext]'
                        }
                    }
                ]
            },
        ]
    },
    plugins: plugins
};

module.exports = options;