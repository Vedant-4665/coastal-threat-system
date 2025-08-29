/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'coastal-blue': '#1e40af',
        'coastal-teal': '#0d9488',
        'alert-red': '#dc2626',
        'alert-yellow': '#ca8a04',
        'alert-green': '#16a34a'
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
