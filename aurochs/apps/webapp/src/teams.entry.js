import { createApp } from "vue";
import TeamsPage from "./pages/admin/TeamsPage";

import "./css/style.css";
import "./css/teams.css";

const teamsApp = createApp({
  components: {
    TeamsPage,
  },
});

teamsApp.mount("#teams");
