/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./pages/**/*.html', './partials/**/*.html', './build.py'],
  theme: {
    extend: {
      colors: {
        paper:   '#F5F3EC',   // warm bone background
        paper2:  '#EEEBE1',   // slightly deeper paper (alt bands)
        surface: '#FFFFFF',   // cards / raised
        ink:     '#1A1D24',   // headings (near-black, cool)
        body:    '#454A54',   // body copy
        muted:   '#6F6A5B',   // captions / meta (warm grey, AA on paper)
        line:    '#DAD5C7',   // hairline rules on paper
        navy:    '#002349',   // Sotheby's blue — links, accents, footer
        navy2:   '#0A305C',   // hover navy
      },
      fontFamily: {
        sans: ['"Libre Franklin"', 'ui-sans-serif', 'system-ui', '-apple-system', '"Segoe UI"', 'Roboto', '"Helvetica Neue"', 'Arial', 'sans-serif'],
      },
      letterSpacing: {
        label: '0.22em',
        nav: '0.14em',
      },
      maxWidth: {
        page: '84rem',
        prose: '38rem',
      },
    },
  },
};
