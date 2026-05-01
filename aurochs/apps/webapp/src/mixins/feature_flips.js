import * as Sentry from "@sentry/vue";

export const featureFlipApp = function (app) {
  // AIRGAPPED FEATURE FLIP
  if (window?.aurochs?.data?.config?.bugsink_dsn) {
    Sentry.init({
      app,
      dsn: window.aurochs.data.config.bugsink_dsn,
      tunnel: "/api/error-handling/",
      tracesSampleRate: 0,
      sendDefaultPii: false,
      beforeSend(event) {
        const ua = navigator.userAgent || "";
        if (/bot|crawl|spider|slurp|bingpreview|mediapartners|google|baidu|yandex|duckduck|facebookexternalhit|linkedinbot|twitterbot|applebot|semrush|ahrefs|mj12bot|dotbot|petalbot|bytespider|gptbot|claudebot/i.test(ua)) {
          return null;
        }
        return event;
      },
    });
  }
  // END AIRGAPPED FEATURE FLIP
  return app;
};
