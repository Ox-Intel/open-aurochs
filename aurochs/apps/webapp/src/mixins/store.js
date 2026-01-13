import { createApp } from "vue";
import vClickOutside from "click-outside-vue3";
import vueShortkey from "vue3-shortkey";
import mitt from "mitt";
import * as VueRouter from "vue-router";
import { useAurochsData } from "../stores/aurochs";
import { sendEvent } from "../mixins/events";
import { featureFlipApp } from "../mixins/feature_flips";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import Tailwind from "primevue/passthrough/tailwind";
import VueSimpleWebsocket from "vue-simple-websocket";

import DashboardPage from "../pages/DashboardPage";
import InboxPage from "../pages/InboxPage";
import LibraryPage from "../pages/LibraryPage";
import OxGPTPage from "../pages/OxGPTPage";
import ReportsPage from "../pages/ReportsPage";
import FrameworkPage from "../pages/FrameworkPage";
import SourcePage from "../pages/SourcePage";
import StackPage from "../pages/StackPage";
import TeamsPage from "../pages/TeamsPage";
import GuidePage from "../pages/GuidePage";
import AboutOxPage from "../pages/AboutOxPage";
import OrgsTeamUpgradePage from "../pages/OrgsTeamUpgradePage";
import NotFoundPage from "../pages/NotFoundPage";
import AccountPage from "../pages/account/AccountPage";

// const DEFAULT_TITLE = "Ox";
const routes = [
  {
    path: "/",
    component: DashboardPage,
    meta: {
      title: "Dashboard",
    },
  },
  {
    path: "/dashboard",
    component: DashboardPage,
    meta: {
      title: "Dashboard",
    },
  },
  {
    path: "/library",
    component: LibraryPage,
    meta: {
      title: "Library",
    },
  },
  {
    path: "/oxgpt",
    component: OxGPTPage,
    meta: {
      title: "OxGPT",
    },
  },
  {
    path: "/about-ox",
    component: AboutOxPage,
    meta: {
      title: "About Ox",
    },
  },
  {
    path: "/guide",
    component: GuidePage,
    meta: {
      title: "guide",
    },
  },
  {
    path: "/inbox",
    component: InboxPage,
    meta: {
      title: "Inbox",
    },
  },
  {
    path: "/teams",
    component: TeamsPage,
    meta: {
      title: "Teams",
    },
  },
  {
    path: "/teams-upgrade",
    component: OrgsTeamUpgradePage,
    meta: {
      title: "Organizations and Teams",
    },
  },
  {
    path: "/account",
    component: AccountPage,
    meta: {
      title: "Your Profile",
    },
  },
  {
    path: "/report/:id",
    component: ReportsPage,
    props: (route) => ({
      id: String(route.params.id),
      new: route.query.new == "true",
    }),
  },
  {
    path: "/framework/:id",
    component: FrameworkPage,
    props: (route) => ({
      id: String(route.params.id),
      new: route.query.new == "true",
    }),
  },
  {
    path: "/source/:id",
    component: SourcePage,
    props: (route) => ({
      id: String(route.params.id),
      new: route.query.new == "true",
    }),
  },
  {
    path: "/stack/:id",
    component: StackPage,
    props: (route) => ({
      id: String(route.params.id),
      new: route.query.new == "true",
    }),
  },
  { path: "/:pathMatch(.*)*", component: DashboardPage },
  { path: "/:pathMatch(.*)", name: "bad-not-found", component: NotFoundPage },
];

const router = VueRouter.createRouter({
  history: VueRouter.createWebHistory(),
  routes,
});

// router.afterEach((to) => {
//   document.title = to.meta.title || document.title || DEFAULT_TITLE;
// });

export const handleEvent = function (data) {
  let store = useAurochsData();

  const unescape_obj = (obj) => {
    var i;
    if (typeof obj == "string") {
      if (obj.indexOf("__AUROCHS_START_PARSER_") !== -1) {
        // Unescape this.
        var parts = obj
          .replace("__AUROCHS_START_PARSER_", "")
          .replace("__AUROCHS_END_PARSER_", "")
          .split("_AUROCHS_MID_");
        return window.aurochs.data[parts[0]][parts[1]];
      } else {
        return obj;
      }
    } else if (obj instanceof Array) {
      var ret_list = [];
      for (i in obj) {
        ret_list.push(unescape_obj(obj[i]));
      }
      return ret_list;
    } else if (obj instanceof Object) {
      var ret_dict = {};
      for (i in obj) {
        ret_dict[i] = unescape_obj(obj[i]);
      }
      return ret_dict;
    }
    return obj;
  };
  const unescape_dict = (dict) => {
    var d = {};
    for (var k in dict) {
      d[k] = unescape_obj(dict[k]);
    }
    return d;
  };
  const updateState = (model, pk, value) => {
    // console.log(model)
    // console.log(pk)
    // console.log(value)
    try {
      if (value.indexOf("|| {}") === -1) {
        store[model] = store[model] || {};
        store[model][pk] = store[model][pk] || {};
        window.aurochs.data[model] = window.aurochs.data[model] || {};
        // console.log(unescape_dict(JSON.parse(value.replace(/window.aurochs.data.(\w+)\['([A-z0-9]+)'\]/g, '"__AUROCHS_START_PARSER_$1_AUROCHS_MID_$2__AUROCHS_END_PARSER_"'))))
        var newVal = unescape_dict(
          JSON.parse(
            value.replace(
              /window.aurochs.data.(\w+)\['([A-z0-9]+)'\]/g,
              '"__AUROCHS_START_PARSER_$1_AUROCHS_MID_$2__AUROCHS_END_PARSER_"'
            )
          )
        );
        // if (!deepEqual(store[model][pk], newVal)) {
        store[model][pk] = newVal;
        window.aurochs.data[model][pk] = store[model][pk];
        // Handle the current user
        if (model == "users" && pk == store.user.id) {
          store.user = store[model][pk];
          window.aurochs.data.user = store.user;
        }
        // }
      } else {
        if (model && pk) {
          store[model] = store[model] || {};
          store[model][pk] = store[model][pk] || {};
        }
      }
      return { ...store };
    } catch (e) {
      // Handles errors (logout, etc) without taking down the app.
      return store;
    }
  };

  // Parse response, update window.aurochs.data
  let d = JSON.parse(JSON.parse(data)["data"]);
  if (d.success) {
    for (var i in d["objs"]) {
      for (var k in d["objs"][i]) {
        if (k && d["objs"][i][k]) {
          var model = k.replace("window.aurochs.data.", "");
          if (model.indexOf("[") !== -1) {
            // We got data for an object.
            var pk = model.substring(model.indexOf("['") + 2, model.indexOf("']"));
            model = model.substring(0, model.indexOf("['"));
            if (d["objs"][i][k].charAt(d["objs"][i][k].length - 1) === ";") {
              d["objs"][i][k] = d["objs"][i][k].substring(0, d["objs"][i][k].length - 1);
            }
            if (d["objs"][i][k] && d["objs"][i][k] != "") {
              updateState(model, pk, d["objs"][i][k]);
            }
          } else {
            // We got a scoping statement.
            updateState(model, false, "store." + model + " || {}");
          }
        }
      }
    }
  } else {
    // console.log("Error:" + d.error_message);
    // console.log(data);
  }
  for (var delete_index in d["deleted"]) {
    var obj = d["deleted"][delete_index];
    if (store[obj.type] && store[obj.type][obj.pk]) {
      delete store[obj.type][obj.pk];
    }
    if (window.aurochs.data[obj.type] && window.aurochs.data[obj.type][obj.pk]) {
      delete window.aurochs.data[obj.type][obj.pk];
    }
  }
  if (d?.objs && Object.keys(d.objs).length > 0) {
    window.aurochs.emitter.emit("reindexSearch");
  }
  return d;
};

export const createAndLinkApp = function (app_data) {
  const emitter = mitt();
  const pinia = createPinia();
  let app = createApp(app_data);

  app = featureFlipApp(app);
  app.config.globalProperties.$aurochsData = window.aurochs;

  app.config.globalProperties.emitter = emitter;
  window.aurochs.emitter = emitter;
  app.use(vClickOutside);
  app.use(vueShortkey);
  app.use(router);
  app.use(pinia);
  app.use(PrimeVue, { unstyled: true, pt: Tailwind });

  let ws_options = {
    reconnectEnabled: true,
    reconnectInterval: 5000,
  };
  if (document.location.protocol.indexOf("https") != -1) {
    window.aurochs.data.config.ws_path = window.aurochs.data.config.ws_path.replace("ws:/", "wss:/");
  }
  // If the line below is erroring, there's very likely a syntax error in the data dump.
  app.use(VueSimpleWebsocket, window.aurochs.data.config.ws_path, ws_options);
  app.config.globalProperties.$socketClient.onMessage = (msg) => {
    // console.log("onmessage")
    let msg_data = JSON.parse(msg.data);
    // let ret = handleEvent(msg_data)
    if (msg_data.type == "data_update") {
      handleEvent(msg.data);
    } else {
      if (msg_data.type == "oxgpt_event") {
        app.config.globalProperties.emitter.emit("oxgpt_event", msg_data);
      }
      if (msg_data.type == "export_event") {
        app.config.globalProperties.emitter.emit("export_event", msg_data);
      }
    }
    // app.config.globalProperties.emitter.emit("eventHandled", {});
    // console.log("emitted")
    // console.log(ret)
    // console.log(app.config.globalProperties.$aurochsData.data)
  };
  app.config.globalProperties.$sendSocketEvent = async function (event_type, data) {
    data["event_type"] = event_type;
    return app.config.globalProperties.$socketClient.sendObj(data);
  };
  app.config.globalProperties.$sendEvent = async function (event_type, data) {
    let store = useAurochsData();
    return sendEvent(event_type, data, store);
  };
  return app;
};
