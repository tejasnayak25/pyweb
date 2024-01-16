/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["**/*"],
  theme: {
    extend: {},
  },
  variants: { // all the following default to ['responsive']
    imageRendering: ['responsive'],
  },
  plugins: [require("daisyui"), require("tailwindcss-image-rendering")()],
}

