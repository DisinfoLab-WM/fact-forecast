/* this is straight from https://vite.dev/guide/backend-integration.html */
/*
export default defineConfig({
  server: {
    cors: {
      // the origin you will be accessing via browser
      origin: process.env.BACKEND_URL,
    },
  },
  build: {
    // generate .vite/manifest.json in outDir
    manifest: true,
    rollupOptions: {
      // overwrite default .html entry
      input: process.env.FRONT_END_PATH + "main.js",
    },
  },
});
*/

export default {
  build: {
    sourcemap: true,
  },
};
