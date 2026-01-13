import { createAndLinkApp } from "./mixins/store.js";
import DashboardPage from "./pages/DashboardPage";

import "./css/style.css";
import "./css/dashboard.css";

const dashboardApp = createAndLinkApp({
  components: {
    DashboardPage,
  },
});

dashboardApp.mount("#dashboard");
