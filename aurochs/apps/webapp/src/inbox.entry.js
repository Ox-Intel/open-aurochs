import { createAndLinkApp } from "./mixins/store";
import InboxPage from "./pages/InboxPage";

import "./css/style.css";
import "./css/framework.css";

const inboxApp = createAndLinkApp({
  components: {
    InboxPage,
  },
});

inboxApp.mount("#inbox");
