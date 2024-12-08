import type { Config } from "tailwindcss";

export default {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/frontend/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "blue": {
          25: "#173047",
          50: "#6C8DA3",
        },
        "pink": {
          25: "#FF7E79",
        },
        "white": {
          25: "#FFFFFF",
          50: "#D9D9D9",
        }
      },
    },
  },
  plugins: [],
} satisfies Config;
