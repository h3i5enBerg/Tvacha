/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx,ts,tsx}', './components/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        canvas: '#F2F2F7',
        surface: '#FFFFFF',
        border: '#E5E5EA',
        inkPrimary: '#1C1C1E',
        inkSecondary: '#6E6E73',
        accent: '#007AFF',
      },
    },
  },
  plugins: [],
};
