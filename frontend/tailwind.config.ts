import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        display: ["Space Grotesk", "Inter", "system-ui", "sans-serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"]
      },
      boxShadow: {
        brutal: "6px 6px 0 #111111",
        brutalSm: "3px 3px 0 #111111"
      },
      colors: {
        ink: "#111111",
        paper: "#fffaf0",
        cream: "#f6e8c8",
        slack: "#611f69",
        signal: "#17a34a",
        amber: "#f4b400",
        danger: "#e5484d",
        electric: "#2f6df6"
      }
    }
  },
  plugins: []
};

export default config;
