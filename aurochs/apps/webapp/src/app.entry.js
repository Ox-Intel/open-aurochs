import { createAndLinkApp } from "./mixins/store.js";
import HomePage from "./pages/HomePage";

import "./css/style.css";
import "./css/app.css";

const app = createAndLinkApp({
  components: {
    HomePage,
  },
});

app.mount("#app");
