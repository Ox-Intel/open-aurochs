import Rollbar from "rollbar";

export const featureFlipApp = function (app) {
  // AIRGAPPED FEATURE FLIP
  if (window?.aurochs?.data?.config?.rollbar) {
    app.config.globalProperties.$rollbar = new Rollbar({
      // eslint-disable-next-line no-undef
      accessToken: process.env.VUE_APP_ROLLBAR_CLIENT_TOKEN,
      captureUncaught: true,
      captureUnhandledRejections: true,
      payload: {
        // Track your events to a specific version of code for better visibility into version health
        code_version: "1.0.0",
        // Add custom data to your events by adding custom key/value pairs like the one below
        custom_data: "foo",
      },
    });
    app.config.errorHandler = (err, vm) => {
      // , info param
      vm.$rollbar.error(err);
      throw err; // rethrow
    };
  }
  // END AIRGAPPED FEATURE FLIP
  return app;
};
