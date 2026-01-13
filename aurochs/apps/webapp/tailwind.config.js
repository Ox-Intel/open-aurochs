const purge = require('./purge.config.js');
const defaultTheme = require('tailwindcss/defaultTheme');

const criteriaColors = {
  "ox-score": "#8E24FF",
  "ox-score-content": "rgb(255, 255, 255)",
  // "report": "#e0af0c",
  // "--report-color": "#e0af0c",
  // "report-background-color": "#f0dd9b",
  // "--report-background-color": "#f0dd9b",
  "framework": "hsl(172,86.5%,37.6%)",
  "--framework-color": "hsl(172,86.5%,37.6%)",
  "report": "#e0af0c",
  "--report-color": "#e0af0c",
  "report-background-color": "#f0dd9b",
  "--report-background-color": "#f0dd9b",
  "source": "#00b4ee",
  "--source-color": "#00b4ee",
  "stack": "#e80a00",
  "--stack-color": "#e80a00",
  "medium-grey": "#CCCCCC",
  "--medium-grey": "#CCCCCC",
  "dark-grey": "#888",
  "--dark-grey": "#888",
  "base-400": "hsl(359, 0%, 87%)",
  "--base-400": "hsl(359, 0%, 87%)",
  "base-500": "hsl(359, 0%, 81%)",
  "--base-500": "hsl(359, 0%, 81%)",
  "base-150": "hsl(359, 0%, 97.5%)",
  "--base-150": "hsl(359, 0%, 97.5%)",
  "base-250": "hsl(359, 0%, 94%)",
  "--base-250": "hsl(359, 0%, 94%)",

  "dark-base-100": "hsl(220, 30%, 24%)",
  "--dark-base-100": "hsl(220, 30%, 24%)",
  "dark-base-150": "hsl(220, 30%, 30%)",
  "--dark-base-150": "hsl(220, 30%, 30%)",
  "dark-base-200": "hsl(220, 30%, 36%)",
  "--dark-base-200": "hsl(220, 30%, 36%)",
  "dark-base-250": "hsl(220, 30%, 30%)",
  "--dark-base-250": "hsl(220, 30%, 30%)",
  "dark-base-300": "hsl(220, 30%, 48%)",
  "--dark-base-300": "hsl(220, 30%, 48%)",
  "dark-base-400": "hsl(220, 30%, 56%)",
  "--dark-base-400": "hsl(220, 30%, 56%)",
  "dark-base-500": "hsl(220, 30%, 64%)",
  "--dark-base-500": "hsl(220, 30%, 64%)",
  "dark-medium-grey": "#798eb4",
  "--dark-medium-grey": "#798eb4",
  "dark-dark-grey": "#7196db",
  "--dark-dark-grey": "#7196db",
  
  
  // Copied to chart_color.js (not DRY, keep these synced.)
  "--criteria-color-1": "hsl(251,32.7%,41.4%)",
  "--criteria-color-2": "hsl(207,55.6%,38.8%)",
  "--criteria-color-3": "hsl(191,95.3%,33.7%)",
  "--criteria-color-4": "hsl(172,86.5%,37.6%)",
  "--criteria-color-5": "hsl(158,81.7%,47.3%)",
  "--criteria-color-6": "hsl(113,65.9%,67.8%)",
  "--criteria-color-7": "hsl(82,72.4%,65.9%)",
  "--criteria-color-8": "hsl(58,82.3%,64.5%)",
  "--criteria-color-9": "hsl(43,84.9%,63.5%)",
  "--criteria-color-10": "hsl(30,86.5%,62.4%)",

  "--criteria-color-11": "hsl(251,32.7%,21.4%)",
  "--criteria-color-12": "hsl(207,55.6%,28.8%)",
  "--criteria-color-13": "hsl(191,95.3%,23.7%)",
  "--criteria-color-14": "hsl(172,86.5%,27.6%)",
  "--criteria-color-15": "hsl(158,81.7%,37.3%)",
  "--criteria-color-16": "hsl(113,65.9%,47.8%)",
  "--criteria-color-17": "hsl(82,72.4%,45.9%)",
  "--criteria-color-18": "hsl(58,82.3%,44.5%)",
  "--criteria-color-19": "hsl(43,84.9%,43.5%)",
  "--criteria-color-20": "hsl(30,86.5%,42.4%)",

  "--criteria-color-21": "hsl(251,32.7%,41.4%)",
  "--criteria-color-22": "hsl(207,55.6%,38.8%)",
  "--criteria-color-23": "hsl(191,95.3%,33.7%)",
  "--criteria-color-24": "hsl(172,86.5%,37.6%)",
  "--criteria-color-25": "hsl(158,81.7%,47.3%)",
  "--criteria-color-26": "hsl(113,65.9%,67.8%)",
  "--criteria-color-27": "hsl(82,72.4%,65.9%)",
  "--criteria-color-28": "hsl(58,82.3%,64.5%)",
  "--criteria-color-29": "hsl(43,84.9%,63.5%)",
  "--criteria-color-30": "hsl(30,86.5%,62.4%)",

  "--criteria-color-31": "hsl(251,12.7%,41.4%)",
  "--criteria-color-32": "hsl(207,35.6%,38.8%)",
  "--criteria-color-33": "hsl(191,75.3%,33.7%)",
  "--criteria-color-34": "hsl(172,66.5%,37.6%)",
  "--criteria-color-35": "hsl(158,61.7%,47.3%)",
  "--criteria-color-36": "hsl(113,45.9%,67.8%)",
  "--criteria-color-37": "hsl(82,52.4%,65.9%)",
  "--criteria-color-38": "hsl(58,62.3%,64.5%)",
  "--criteria-color-39": "hsl(43,64.9%,63.5%)",
  "--criteria-color-40": "hsl(30,66.5%,62.4%)",


  "--rounded-box": "1rem", // border radius rounded-box utility class, used in card and other large boxes
  "--rounded-btn": "0.5rem", // border radius rounded-btn utility class, used in buttons and similar element
  "--rounded-badge": "1.9rem", // border radius rounded-badge utility class, used in badges and similar
  "--animation-btn": "0.25s", // duration of animation when you click on button
  "--animation-input": "0.2s", // duration of animation for inputs like checkbox, toggle, radio, etc
  "--btn-text-case": "uppercase", // set default text transform for buttons
  "--btn-focus-scale": "0.95", // scale transform of button when you focus on it
  "--border-btn": "1px", // border width of buttons
  "--tab-border": "1px", // border width of tabs
  "--tab-radius": "0.5rem", // border radius of tabs
}
const colors = require('tailwindcss/colors')
let safelist = Object.keys(criteriaColors);
safelist.push(
  "basis-1/12",
  "basis-2/12",
  "basis-3/12",
  "basis-4/12",
  "basis-5/12",
  "basis-6/12",
  "basis-7/12",
  "basis-8/12",
  "basis-9/12",
  "basis-10/12",
  "basis-11/12",
)


module.exports = {
  darkMode: "media",
  content: purge.content,
  theme: {
    extend: {
      fontFamily: {
        sans: [
          'acf',
          'Helvetica Neue',
          'Helvetica',
          'sans-serif',  
          defaultTheme.fontFamily.sans
        ],
        serif: ['Merriweather', 'serif'],
      },
      colors: {
        ...criteriaColors,
      },
      fontSize: {
        "2xs": '0.7em',
      }
    },
  },
          
  daisyui: {
    themes: [
      {
        light: {
          ...require("daisyui/src/colors/themes")["[data-theme=light]"],
          ...criteriaColors,
          "primary": "#30b89d",
          "secondary": "#155e75",
          "accent": "#d4ff01",
          "accent-content": "#1d2800",
          "neutral": "#222",
          "neutral-content": "#FFF",
          "base-100": "hsl(359, 0%, 99%)",
          "base-150": "hsl(359, 0%, 97.5%)",
          "--base-150": "hsl(359, 0%, 97.5%)",
          "base-200": "hsl(359, 0%, 96%)",
          "base-250": "hsl(359, 0%, 94%)",
          "--base-250": "hsl(359, 0%, 94%)",
          "base-300": "hsl(359, 0%, 92%)",
          "base-400": "hsl(359, 0%, 87%)",
          "--base-400": "hsl(359, 0%, 87%)",
          "base-500": "hsl(359, 0%, 81%)",
          "--base-500": "hsl(359, 0%, 81%)",
          "medium-grey": "#CCCCCC",
          "--medium-grey": "#CCCCCC",
          "dark-grey": "#888",
          "--dark-grey": "#888",
          "info": "#8E24FF",
          "success": "#30b89d",
          "success-content": "#f9fffe",
          "warning": "#fcd34d",
          "error": "#ff531A",
          "mid-content": "220 20% 22%",
          "ui-element-grey": "hsla(var(--bc)/0.2)",
          "--ui-element-grey": "hsla(var(--bc)/0.2)",
        },
        dark: {
          ...require("daisyui/src/colors/themes")["[data-theme=dark]"],
          ...criteriaColors,
          "primary": "#30b89d",
          "secondary": "#155e75",
          "accent": "#d4ff01",
          "accent-content": "#1d2800",
          "neutral": "#FFF",
          "neutral-content": "#222",
          "base-100": "hsl(220, 30%, 24%)",
          "--base-100": "hsl(220, 30%, 24%)",
          "base-150": "hsl(220, 30%, 30%)",
          "--base-150": "hsl(220, 30%, 30%)",
          "base-200": "hsl(220, 30%, 36%)",
          "--base-200": "hsl(220, 30%, 36%)",
          "base-250": "hsl(220, 30%, 30%)",
          "--base-250": "hsl(220, 30%, 30%)",
          "base-300": "hsl(220, 30%, 48%)",
          "base-400": "hsl(220, 30%, 56%)",
          "--base-400": "hsl(220, 30%, 56%)",
          "base-500": "hsl(220, 30%, 64%)",
          "--base-500": "hsl(220, 30%, 64%)",
          "dark-medium-grey": "#798eb4",
          "--dark-medium-grey": "#798eb4",
          "dark-grey": "#7196db",
          "--dark-grey": "#7196db",
          "info": "#8E24FF",
          "success": "#30b89d",
          "success-content": "#f9fffe",
          "warning": "#fcd34d",
          "error": "#ff531A",
          "--bc": "220 20% 92%",
          "mid-content": "220 20% 92%",
          "--tw-prose-body": "hsla(var(--bc)/1)",
        },
      },
    ],
  },
  variants: {},
  safelist: safelist,
  plugins: [
    require('@tailwindcss/forms'),
    // require('@tailwindcss/aspect-ratio'),
    require('@tailwindcss/typography'),
    require('daisyui'),
    // require('tailwindcss-children'),
  ],
};
