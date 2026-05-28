import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // 👻 Dedemit UMKM — Universal UMKM AI OS color system
        brand: {
          light: "#34D399",  // Emerald Mint (growth/profit)
          DEFAULT: "#10B981", // Dedemit Green
          dark: "#059669",   // Deep Emerald
          ghost: "#F59E0B"   // Amber Gold (money/cuan)
        },
        dark: {
          50: "#FAFAFA",
          100: "#F4F4F5",
          800: "#18181B",
          900: "#09090B",
          950: "#020205"
        },
        umkm: {
          green: "#10B981",
          gold: "#F59E0B",
          teal: "#2DD4BF",
          purple: "#8B5CF6",
          rose: "#F43F5E",
          sky: "#38BDF8"
        }
      },
      fontFamily: {
        sans: ["Outfit", "Inter", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic": "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
        "umkm-glow": "radial-gradient(circle at top right, rgba(16, 185, 129, 0.12), transparent 40%)",
        "ghost-glow": "radial-gradient(circle at bottom left, rgba(245, 158, 11, 0.08), transparent 30%)",
        "streetwear-glow": "radial-gradient(circle at top right, rgba(16, 185, 129, 0.10), transparent 40%)",
      },
    },
  },
  plugins: [],
};

export default config;
