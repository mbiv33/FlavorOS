import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        bg: {
          base: "var(--bg-base)",
          1: "var(--bg-1)",
          2: "var(--bg-2)",
          3: "var(--bg-3)",
        },
        ink: {
          DEFAULT: "var(--ink)",
          2: "var(--ink-2)",
          3: "var(--ink-3)",
        },
        line: {
          DEFAULT: "var(--line)",
          2: "var(--line-2)",
        },
        card: {
          DEFAULT: "var(--card)",
          solid: "var(--card-solid)",
        },
        accent: "var(--accent)",
        warn: "var(--warn)",
        ok: "var(--ok)",
        kha: "var(--kha)",
        sin: "var(--sin)",
        max: "var(--max)",
        kyl: "var(--kyl)",
        sco: "var(--sco)",
      },
      borderColor: {
        DEFAULT: "var(--line)",
      },
      borderRadius: {
        card: "var(--radius)",
        sm2: "var(--radius-sm)",
      },
      boxShadow: {
        sm2: "var(--shadow-sm)",
        md2: "var(--shadow-md)",
      },
      fontFamily: {
        sans: [
          "Inter",
          "-apple-system",
          "BlinkMacSystemFont",
          "system-ui",
          "sans-serif",
        ],
      },
      keyframes: {
        pulse: {
          "0%,100%": { opacity: "1" },
          "50%": { opacity: "0.45" },
        },
        orbPulse: {
          "0%,100%": {
            boxShadow:
              "0 0 0 4px rgba(228,103,78,.18), 0 0 0 12px rgba(228,103,78,.06)",
          },
          "50%": {
            boxShadow:
              "0 0 0 6px rgba(228,103,78,.3), 0 0 0 18px rgba(228,103,78,.08)",
          },
        },
      },
      animation: {
        pulse: "pulse 1.6s ease-in-out infinite",
        orbPulse: "orbPulse 2.2s ease-in-out infinite",
      },
    },
  },
  plugins: [],
};

export default config;
