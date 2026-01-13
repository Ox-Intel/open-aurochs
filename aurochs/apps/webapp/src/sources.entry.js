import { createAndLinkApp } from "./mixins/store";
import SourcePage from "./pages/SourcePage";

import "./css/style.css";
import "./css/sources.css";

const sourcesApp = createAndLinkApp({
  components: {
    SourcePage,
  },
});

sourcesApp.mount("#sources");
