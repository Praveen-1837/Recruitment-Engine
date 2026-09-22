/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#0066CC",
          primaryHover: "#0052A3",
          success: "#00B359",
          successBg: "#E8F5E9",
          danger: "#D94A45",
          dangerBg: "#FFEBEE",
          warning: "#FFB900",
          neutralGray: "#F5F5F5",
          darkGray: "#333333",
          lightGray: "#E0E0E0",
          border: "#E5E7EB",
        }
      }
    },
  },
  plugins: [],
}
