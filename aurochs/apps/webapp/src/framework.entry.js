import { createAndLinkApp } from "./mixins/store";
import FrameworkPage from "./pages/FrameworkPage";

import "./css/style.css";
import "./css/framework.css";

const frameworkApp = createAndLinkApp({
  components: {
    FrameworkPage,
  },
});

frameworkApp.mount("#framework");
