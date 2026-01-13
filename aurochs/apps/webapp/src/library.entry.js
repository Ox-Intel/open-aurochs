import { createAndLinkApp } from "./mixins/store";
import LibraryPage from "./pages/LibraryPage";

import "./css/style.css";
import "./css/library.css";

const libraryApp = createAndLinkApp({
  components: {
    LibraryPage,
  },
});

libraryApp.mount("#library");
