import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        soil: "#42362a",
        leaf: "#527853",
        wheat: "#f1d18a",
        paper: "#fffaf0"
      },
      fontFamily: {
        display: ["Georgia", "serif"],
        sans: ["Aptos", "sans-serif"]
      }
    }
  },
  plugins: []
};

export default config;
