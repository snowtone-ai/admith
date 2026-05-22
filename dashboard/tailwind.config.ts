import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Manrope", "Noto Sans JP", "sans-serif"],
        body: ["Inter", "Noto Sans JP", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      colors: {
        canvas: "#06060B",
        surface: { 1: "#0C0D14", 2: "#12131D", 3: "#1A1B28", 4: "#222336" },
        ink: { DEFAULT: "#F0F1F5", muted: "#A0A4B8", subtle: "#6B6F82", ghost: "#3D4055" },
        accent: { DEFAULT: "#7C3AED", hover: "#8B5CF6", pressed: "#6D28D9" },
        positive: { DEFAULT: "#10B981", subtle: "rgba(16,185,129,0.12)" },
        negative: { DEFAULT: "#F43F5E", subtle: "rgba(244,63,94,0.12)" },
        warning: { DEFAULT: "#F59E0B", subtle: "rgba(245,158,11,0.12)" },
        info: { DEFAULT: "#06B6D4", subtle: "rgba(6,182,212,0.12)" },
        hairline: "rgba(255,255,255,0.06)",
        "hairline-strong": "rgba(255,255,255,0.12)",
      },
      borderRadius: {
        sm: "4px",
        DEFAULT: "8px",
        md: "8px",
        lg: "12px",
        xl: "16px",
        xxl: "24px",
      },
      spacing: {
        section: "80px",
        hero: "120px",
      },
    },
  },
  plugins: [],
};

export default config;
