const fs = require("fs");
const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const TerserPlugin = require("terser-webpack-plugin");
var BundleTracker = require("webpack-bundle-tracker");
var WriteFilePlugin = require("write-file-webpack-plugin");
const Dotenv = require("dotenv-webpack");

module.exports = (env) => ({
  mode: "production",
  entry: {
    main: path.resolve(__dirname, "src/index.js"),
  },
  optimization: {
    minimize: true,
    minimizer: [
      // This is only used in production mode
      // new TerserPlugin({
      //   terserOptions: {
      //     parse: {
      //       ecma: 8,
      //     },
      //     compress: {
      //       ecma: 5,
      //       warnings: false,
      //       comparisons: true,
      //       inline: 2,
      //     },
      //     mangle: {
      //       safari10: true,
      //     },
      //     // Added for profiling in devtools
      //     keep_classnames: true,
      //     keep_fnames: true,
      //     output: {
      //       ecma: 5,
      //       comments: false,
      //       ascii_only: true,
      //     },
      //   },
      // }),
      // This is only used in production mode
      new CssMinimizerPlugin(),
    ],
  },
  watch: true,
  watchOptions: {
    ignored: ["/node_modules/"],
    aggregateTimeout: 500, // wait to build file
  },
  output: {
    path: path.resolve(__dirname, "../static/reactUI/"),
    filename: "js/[name].js",
    clean: true,
    publicPath: "/static/reactUI/",
    assetModuleFilename: "media/[name][ext]",
  },
  resolve: {
    extensions: ["*", ".js", ".jsx"],
  },
  devtool: "source-map",
  module: {
    rules: [
      {
        test: /\.(sa|sc|c)ss$/,
        exclude: /\.module\.(scss|sass)$/,
        use: [
          MiniCssExtractPlugin.loader,

          {
            loader: "css-loader",
            options: { url: true },
          },
          {
            loader: "postcss-loader",
          },
          {
            loader: "sass-loader",
          },
        ],
      },

      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: [
          {
            loader: "babel-loader",
            options: {
              presets: ["@babel/preset-env", "@babel/preset-react"],
            },
          },
        ],
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/, // to import images and fonts
        loader: "url-loader",
        options: { limit: false },
      },
      {
        test: /\.(png|svg|jpe?g|gif)$/i,
        type: "asset/resource",
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
    new BundleTracker({
      filename: "webpack-stats.json",
    }),
    new WriteFilePlugin(),
    new Dotenv({
      path: `./.env.staging`,
    }),
  ],
});
