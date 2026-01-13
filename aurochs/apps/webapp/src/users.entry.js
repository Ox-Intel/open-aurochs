import { createApp } from "vue";
import UsersPage from "./pages/admin/UsersPage";

import "./css/style.css";
import "./css/users.css";

const usersApp = createApp({
  components: {
    UsersPage,
  },
});

usersApp.mount("#users");
