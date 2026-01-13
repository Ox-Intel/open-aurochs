import { createApp } from "vue";
import AccountPage from "./pages/account/AccountPage";

import "./css/style.css";
import "./css/account.css";

const accountApp = createApp({
  components: {
    AccountPage,
  },
});

accountApp.mount("#account");
