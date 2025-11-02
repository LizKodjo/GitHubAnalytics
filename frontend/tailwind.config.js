// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f5f3ff",
          100: "#ede9fe",
          500: "#8b5cf6",
          600: "#6e40c9",
          700: "#5b21b6",
        },
        github: {
          dark: "#0d1117",
          card: "#161b22",
          border: "#30363d",
          text: {
            primary: "#f0f6fc",
            secondary: "#8b949e",
          },
        },
      },
    },
  },
  plugins: [],
};
