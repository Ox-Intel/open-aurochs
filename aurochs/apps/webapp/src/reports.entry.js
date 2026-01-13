import { createAndLinkApp } from "./mixins/store";
import ReportsPage from "./pages/ReportsPage";

import "./css/style.css";
import "./css/reports.css";

const reportsApp = createAndLinkApp({
  components: {
    ReportsPage,
  },
});

reportsApp.mount("#reports");
