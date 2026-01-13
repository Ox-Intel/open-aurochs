module.exports = {
    plugins: [
      require("tailwindcss/nesting"),
      require('postcss-import'),
      require('tailwindcss'),
      require('postcss-nested'),
      require('autoprefixer'),
    ]
}