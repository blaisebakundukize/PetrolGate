const intro = `/*!
 * Build: ${(new Date()).toISOString()}
 */`;

import cleanup from 'rollup-plugin-cleanup';

export default {
  entry: 'scripts/bootstrap.js',
  dest: 'static/scripts/bootstrap.js',
  plugins: [
    cleanup()
  ],
  intro
};
