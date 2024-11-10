// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  app: {
    head: {
      script: [
        {
          src: "https://kit.fontawesome.com/07c8d25392.js",
          crossorigin: "anonymous",
        },
      ],
    },
  },
  modules: ["@nuxtjs/tailwindcss"],
  tailwindcss: {
    cssPath: ["~/assets/css/tailwind.css", { injectPosition: "first" }],
    configPath: "tailwind.config",
    exposeConfig: {
      level: 2,
    },
    config: {},
    viewer: true,
  },
})
