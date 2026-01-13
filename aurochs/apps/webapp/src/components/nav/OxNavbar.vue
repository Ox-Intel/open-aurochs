<template>
  <div class="navbar bg-slate-800 text-slate-100 shadow-sm fixed">
    <div class="flex-1">
      <router-link v-if="user && user.id" class="btn btn-ghost normal-case text-xl ox-nav-logo" to="/dashboard">
        <ox-logo class="w-8 h-8" />
      </router-link>
      <router-link v-if="!user || !user.id" class="btn btn-ghost normal-case text-xl ox-nav-logo" to="/oxgpt">
        <ox-logo class="w-8 h-8" />
      </router-link>
      <div class="flex-none">
        <ul class="menu menu-horizontal p-0">
          <li v-if="user && user.id">
            <router-link to="/dashboard" :class="isActiveNav('dashboard')" data-cy="nav-dashboard">
              Dashboard
            </router-link>
          </li>
          <li v-if="user && user.id">
            <router-link to="/library" :class="isActiveNav('library')" data-cy="nav-library"> Library </router-link>
          </li>
          <li v-if="user && user.public_signup">
            <router-link to="/teams-upgrade" :class="isActiveNav('teams-upgrade')" data-cy="nav-teams-upgrade">
              Teams
            </router-link>
          </li>
          <li v-if="user && user.id">
            <router-link to="/guide" :class="isActiveNav('guide')" data-cy="nav-guide"> Guide </router-link>
          </li>
          <li v-if="!user || !user.id">
            <router-link to="/about-ox" :class="isActiveNav('aboutox')" data-cy="nav-aboutox"> About Ox </router-link>
          </li>
          <template v-if="user && user.id">
            <!-- <li>
            <router-link :href="aurochsRoot.urls.users">Users</router-link>
          </li> -->

            <li tabindex="3">
              <router-link to="" data-cy="nav-new">
                New
                <svg class="fill-current" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24">
                  <path d="M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z" />
                </svg>
              </router-link>
              <ul class="p-2 text-base-content bg-base-100 z-50 shadow-xl">
                <li>
                  <a href="#" data-cy="nav-new-framework" @click="createBlankFramework">Create Framework</a>
                </li>
                <li>
                  <a href="#" data-cy="nav-new-report" @click="createBlankReport">Create Report</a>
                </li>
                <li>
                  <a href="#" data-cy="nav-new-source" @click="createBlankSource">Create Source</a>
                </li>
                <li>
                  <a href="#" data-cy="nav-new-stack" @click="createBlankStack">Create Stack</a>
                </li>
              </ul>
            </li>
          </template>
        </ul>
      </div>
    </div>
    <div class="flex-none gap-2">
      <router-link to="/oxgpt" :class="isActiveNav('oxgpt')" data-cy="nav-oxgpt">
        <div
          class="bg-ox-score btn hover:bg-ox-score hover:brightness-110 text-ox-score-content normal-case"
          :style="!user || !user.id ? 'font-size: 1rem; padding: 0.75rem 0.9rem;' : ''"
        >
          <!-- <div class="btn btn-outline  text-ox-score-content normal-case border-accent hover:border-accent hover:bg-black"> -->
          <!-- bg-ox-score -->
          OxGPT
          <!-- <img v-if="!darkMode()" class="w-40 mx-auto mb-0" :src="image_url('common/img/oxgpt_tiny_horizontal_black_beta.png')" /> -->
          <!-- <img v-if="darkMode()" class="w-40 mx-auto mb-0" :src="image_url('common/img/oxgpt_tiny_horizontal_white_beta.png')" /> -->
          <!-- <img class="h-8 mx-auto -mt-2 mb-0.5" :src="image_url('common/img/oxgpt_tiny_horizontal_white_beta.png')" /> -->
        </div>
      </router-link>
      <ul v-if="!user || !user.id" class="menu menu-horizontal p-0">
        <li>
          <a
            class="btn-ghost btn normal-case"
            href="/accounts/login"
            data-cy="login"
            style="font-size: 1rem; font-weight: 400"
            >Log in</a
          >
        </li>
      </ul>
      <div v-if="user && user.id" class="">
        <div class="form-control">
          <input
            ref="search"
            v-model="searchText"
            v-shortkey.focus="searchKeys"
            type="text"
            :placeholder="`Search  (${searchKeyText})`"
            class="input input-bordered text-base-content"
            data-cy="nav-search-box"
            @change="searchInputChange"
            @input="searchInputChange"
            @keyup.up="moveSearchSelectionUp"
            @keyup.down="moveSearchSelectionDown"
            @keyup.enter="handleEnter"
            @keydown.meta.enter.stop="handleCmdEnter"
            @keydown.ctrl.enter.stop="handleCmdEnter"
            @keyup.escape="handleEscape"
          />
          <!--             v-shortkey.focus="['meta', 'k']" -->
          <div class="w-full" data-cy="nav-search-results">
            <ul
              v-if="searchText.length > 0"
              class="menu bg-base-100 text-base-content w-2/5 overflow-hidden absolute right-0 top-16 mt-2 mr-8 box-rounded rounded-md z-20 shadow-xl p-4 pb-6"
            >
              <template v-for="(r, idx) in searchMatches" :key="idx">
                <li
                  role="button"
                  class="box-rounded rounded-md mb-0 overflow-x-hidden"
                  :class="idx === selectedIndex ? 'bg-base-300 ' : ''"
                  :data-cy="`nav-search-result-${idx}`"
                  @click="openResult(r)"
                >
                  <a class="p-2 align-left text-md flex place-items-start" @mouseover="hoverItem(idx)">
                    <div class="w-12">
                      <OxObjectIcon :target="r" :classes="'h-8 w-8'" />
                    </div>
                    <div>
                      <!-- eslint-disable-next-line vue/no-v-html -->
                      <span v-html="highlighted(r.name)" />
                      <div v-if="isTagged(r)">
                        <div
                          class="badge badge-md text-sm badge-outline bg-base-200 border-base-300 gap-1 mr-2 mb-2 select-none overflow-hidden whitespace-nowrap"
                        >
                          <!-- eslint-disable-next-line vue/no-v-html -->
                          <span v-html="tagName(r)" />
                        </div>
                      </div>
                      <div v-if="isStacked(r)">
                        <div
                          class="badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 my-1 text-xs select-none overflow-hidden whitespace-nowrap"
                        >
                          <OxObjectIcon :type="'stack'" :classes="'h-3 w-3 mr-0.5 align-middle'" />
                          <!-- eslint-disable-next-line vue/no-v-html -->
                          <span v-html="stackName(r)" />
                        </div>
                      </div>
                    </div>
                  </a>
                </li>
              </template>
              <div
                v-if="searchMatches.length == 0"
                class="box-rounded rounded-md text-medium-grey text-center"
                data-cy="nav-no-matches"
              >
                No matches
              </div>
            </ul>
          </div>
        </div>
      </div>
      <label v-if="user && user.id" tabindex="0" class="btn btn-ghost btn-circle" @click="openInbox">
        <router-link to="/inbox" data-cy="nav-inbox">
          <div class="indicator">
            <FontAwesomeIcon :icon="['fad', 'inbox']" class="h-5 w-5 align-middle" />
            <span v-if="inboxBadge > 0" data-cy="inbox-count" class="badge badge-sm indicator-item badge-accent">{{
              inboxBadge
            }}</span>
          </div>
        </router-link>
      </label>

      <div v-if="user && user.id" class="dropdown dropdown-end">
        <label
          tabindex="2"
          class="btn w-10 h-10 bg-slate-800 border-slate-800 hover:bg-slate-800 hover:border-slate-800"
          data-cy="nav-user-menu"
        >
          <div class="absolute top-0 left-0">
            <OxAvatar :user="user" class="mt-0.5 -ml-1" />
          </div>
        </label>
        <ul
          tabindex="2"
          class="mt-3 p-2 shadow menu menu-compact dropdown-content text-base-content bg-base-100 rounded-box w-52 z-50 shadow-lg"
        >
          <li class="menu-title">
            <div class="font-medium" data-cy="menu-full-name">
              <OxAvatar :user="user" :tiny="true" class="align-middle mb-1" />
              {{ user.full_name }}
            </div>
            <div class="font-light" data-cy="menu-username">
              {{ user.username }}
            </div>
          </li>
          <li>
            <router-link to="/account" data-cy="nav-profile">My Profile</router-link>
          </li>
          <li v-if="!user.public_signup">
            <router-link to="/teams" data-cy="nav-teams"> Teams & Organizations</router-link>
          </li>
          <li v-if="user.public_signup">
            <router-link to="/teams-upgrade" data-cy="nav-teams"> Teams & Organizations</router-link>
          </li>
          <li class="border-t" />
          <li>
            <a data-cy="nav-toggle-mode" @click="setNextTheme()">
              {{ nextTheme.name }} Mode
              <FontAwesomeIcon :icon="nextTheme.icon" class="h-4 w-4 align-middle" />
            </a>
          </li>
          <li>
            <a data-cy="nav-release-notes" @click="openReleaseNotes">Release Notes</a>
          </li>
          <li>
            <a data-cy="nav-contact-ox" @click="openContactOx">Contact Ox</a>
          </li>
          <li>
            <a :href="aurochsRoot.urls.logout" data-cy="nav-logout">Logout</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <input v-if="user && user.id" id="release-notes-modal" type="checkbox" class="modal-toggle" />
  <div v-if="user && user.id" class="modal" data-cy="modal-release-notes">
    <div class="modal-box max-w-screen-lg h-full overflow-hidden">
      <div class="overflow-y-auto h-full p-10">
        <ReleaseNotes />
      </div>
    </div>
  </div>
  <input v-if="user && user.id" id="contact-ox-modal" type="checkbox" class="modal-toggle" />
  <div v-if="user && user.id" class="modal" data-cy="modal-contact-ox">
    <div class="modal-box max-w-screen-md max-h- p-10" :class="contactOxModalOpen ? ' ' : ''">
      <ContactOx />
    </div>
  </div>
</template>

<script>
import "regenerator-runtime/runtime";
import platform from "platform-detect";
import { ref } from "vue";
import * as DOMPurify from "dompurify";
import OxLogo from "../logo/OxLogo";
import OxObjectIcon from "../common/icons/OxObjectIcon.vue";
import OxAvatar from "../common/OxAvatar.vue";
import { useAurochsData, useAurochsRoot } from "../../stores/aurochs";
import ReleaseNotes from "./ReleaseNotes.vue";
import ContactOx from "./ContactOx.vue";
import { checkCanSee } from "../../mixins/permissions.js";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faFileCsv } from "@fortawesome/pro-duotone-svg-icons/faFileCsv";
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faInbox } from "@fortawesome/pro-duotone-svg-icons/faInbox";
import { faBrightness } from "@fortawesome/pro-duotone-svg-icons/faBrightness";
import { faMoon } from "@fortawesome/pro-duotone-svg-icons/faMoon";
import { faCircleHalf } from "@fortawesome/pro-duotone-svg-icons/faCircleHalf";
library.add(
  faFileCsv,
  faClone,
  faPen,
  faFileLines,
  faChartSimpleHorizontal,
  faCompass,
  faMessages,
  faFiles,
  faInbox,
  faBrightness,
  faMoon,
  faCircleHalf
);

export default {
  components: {
    OxLogo,
    OxObjectIcon,
    OxAvatar,
    FontAwesomeIcon,
    ReleaseNotes,
    ContactOx,
  },
  setup() {
    const showCreateFramework = false;
    const theme = ref("light");

    var allPossibleSearchResults = {};
    var allPossibleSearchNameResults = {};
    const searchMatches = ref([]);
    const exact = ref(false);
    const selectedIndex = ref(0);
    const releaseNotesModalOpen = ref(false);
    const contactOxModalOpen = ref(false);
    const themes = ref([
      {
        name: "Light",
        theme: "light",
        icon: ["fad", "brightness"],
      },
      {
        name: "Dark",
        theme: "dark",
        icon: ["fad", "moon"],
      },
      {
        name: "Set Auto",
        theme: "auto",
        icon: ["fad", "circle-half"],
      },
    ]);
    const theme_index = ref(0);
    const searchText = ref("");

    return {
      aurochsData: useAurochsData(),
      aurochsRoot: useAurochsRoot(),
      showCreateFramework,
      theme,
      searchText,
      allPossibleSearchResults,
      allPossibleSearchNameResults,
      searchMatches,
      exact,
      selectedIndex,
      releaseNotesModalOpen,
      contactOxModalOpen,
      themes,
      theme_index,
    };
  },
  computed: {
    user() {
      return this.aurochsData.user;
    },
    inboxBadge() {
      var count = 0;
      for (var i in this.aurochsData.inboxitems) {
        if (!this.aurochsData.inboxitems[i].read) {
          count += 1;
        }
      }
      return count;
    },
    searchKeys() {
      if (platform.ios || platform.macos) {
        return ["meta", "k"];
      }
      return ["ctrl", "k"];
    },
    searchKeyText() {
      if (platform.ios || platform.macos) {
        return "⌘+K";
      }
      return "Ctrl+K";
    },
    nextTheme() {
      let next_index = this.theme_index;
      if (next_index == this.themes.length - 1) {
        next_index = 0;
      } else {
        next_index++;
      }
      return this.themes[next_index];
    },
  },
  watch: {
    searchText() {
      this.exact = false;
      this.selectedIndex = 0;
      this.updateSearchResults();
    },
  },
  mounted() {
    let defaultSearchText = this.aurochsData.searchText ? this.aurochsData.searchText : "";
    this.searchText = defaultSearchText;

    // for (var i in this.aurochsData.reports) {
    //   let obj = this.aurochsData.reports[i];
    //   this.allPossibleSearchResults[`reports_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.reports[i];
    //   this.allPossibleSearchNameResults[`reports_${obj.id}_${this.aurochsData.reports[i].name.toLowerCase()}`] =
    //     this.aurochsData.reports[i];
    // }
    // for (i in this.aurochsData.sources) {
    //   let obj = this.aurochsData.sources[i];
    //   this.allPossibleSearchResults[`sources_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.sources[i];
    //   this.allPossibleSearchNameResults[`sources_${obj.id}_${this.aurochsData.sources[i].name.toLowerCase()}`] =
    //     this.aurochsData.sources[i];
    // }
    // for (i in this.aurochsData.stacks) {
    //   let obj = this.aurochsData.stacks[i];
    //   this.allPossibleSearchResults[`stacks_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.stacks[i];
    //   this.allPossibleSearchNameResults[`stacks_${obj.id}_${this.aurochsData.stacks[i].name.toLowerCase()}`] =
    //     this.aurochsData.stacks[i];
    // }
    // for (i in this.aurochsData.frameworks) {
    //   let obj = this.aurochsData.frameworks[i];
    //   this.allPossibleSearchResults[`frameworks_${obj.id}_${obj.search_text.toLowerCase()}`] =
    //     this.aurochsData.frameworks[i];
    //   this.allPossibleSearchNameResults[`frameworks_${obj.id}_${this.aurochsData.frameworks[i].name.toLowerCase()}`] =
    //     this.aurochsData.frameworks[i];
    // }
    //  let generateResults = function() {
    // );
    this.emitter.on("reindexSearch", this.generateResults);
    this.emitter.on("updateSearch", (e) => {
      this.searchText = e.query;
      this.selectedIndex = 0;
      this.exact = true;
      if (this.$refs && this.$refs.search) {
        this.$refs.search.focus();
      }
      this.updateSearchResults();
    });
    this.generateResults();
    // this.$pollTimeout = setTimeout(this.pollUpdates, 10000);

    if (localStorage.getItem("theme")) {
      document.documentElement.setAttribute("data-theme", localStorage.getItem("theme"));
      this.aurochsData.theme = localStorage.getItem("theme");
      window.aurochs.data.theme = localStorage.getItem("theme");
      this.theme = localStorage.getItem("theme");
      for (let t_index in this.themes) {
        if (this.theme == this.themes[t_index].theme) {
          this.theme_index = t_index;
          this.setTheme(this.themes[t_index].theme);
          break;
        }
      }
    }
  },
  // beforeUnmount() {
  //   clearTimeout(this.$pollTimeout);
  // },
  methods: {
    // async pollUpdates() {
    //   // await this.$sendEvent("get_my_user", {});
    //   // this.$sendEvent("get_my_user", {});
    //   this.$pollTimeout = setTimeout(this.pollUpdates, 10000);
    // },
    generateResults() {
      let results = {};
      let nameResults = {};
      for (var i in this.aurochsData.reports) {
        let obj = this.aurochsData.reports[i];
        if (checkCanSee(obj, this.aurochsData.user)) {
          results[`reports_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.reports[i];
          nameResults[`reports_${obj.id}_${obj.name.toLowerCase()}`] = this.aurochsData.reports[i];
        }
      }
      for (i in this.aurochsData.sources) {
        let obj = this.aurochsData.sources[i];
        if (checkCanSee(obj, this.aurochsData.user)) {
          results[`sources_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.sources[i];
          nameResults[`sources_${obj.id}_${obj.name.toLowerCase()}`] = this.aurochsData.sources[i];
        }
      }
      for (i in this.aurochsData.stacks) {
        let obj = this.aurochsData.stacks[i];
        if (checkCanSee(obj, this.aurochsData.user)) {
          results[`stacks_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.stacks[i];
          nameResults[`stacks_${obj.id}_${obj.name.toLowerCase()}`] = this.aurochsData.stacks[i];
        }
      }
      for (i in this.aurochsData.frameworks) {
        let obj = this.aurochsData.frameworks[i];
        if (checkCanSee(obj, this.aurochsData.user)) {
          results[`frameworks_${obj.id}_${obj.search_text.toLowerCase()}`] = this.aurochsData.frameworks[i];
          nameResults[`frameworks_${obj.id}_${obj.name.toLowerCase()}`] = this.aurochsData.frameworks[i];
        }
      }
      this.allPossibleSearchResults = results;
      this.allPossibleSearchNameResults = nameResults;
      this.updateSearchResults();
    },
    searchInputChange() {},
    updateSearchResults() {
      var matches = {};
      let terms = [];
      if (this.searchText && this.searchText.length > 0) {
        if (this.exact) {
          terms = [this.searchText + "|"];
        } else {
          terms = this.searchText.split(" ");
        }
      }
      // Matches full search: very high
      for (var k in this.allPossibleSearchNameResults) {
        if (k.indexOf(this.searchText) != -1) {
          let slug = this.allPossibleSearchNameResults[k].__type + "_" + this.allPossibleSearchNameResults[k].id;
          if (matches[slug] == undefined) {
            matches[slug] = {
              obj: this.allPossibleSearchNameResults[k],
              rank: 100, // Higher because it's matching the name.
            };
          } else {
            matches[slug].rank += 100;
          }
        }
      }
      for (let split_term of terms) {
        let term = split_term.toLowerCase();
        if (term.length > 0) {
          for (k in this.allPossibleSearchNameResults) {
            if (k.indexOf(term) != -1) {
              let slug = this.allPossibleSearchNameResults[k].__type + "_" + this.allPossibleSearchNameResults[k].id;
              if (matches[slug] == undefined) {
                matches[slug] = {
                  obj: this.allPossibleSearchNameResults[k],
                  rank: 10, // Higher because it's matching the name.
                };
              } else {
                matches[slug].rank += 10;
              }
            }
          }
          for (k in this.allPossibleSearchResults) {
            if (k.indexOf(term) != -1) {
              let slug = this.allPossibleSearchResults[k].__type + "_" + this.allPossibleSearchResults[k].id;
              if (matches[slug] == undefined) {
                matches[slug] = {
                  obj: this.allPossibleSearchResults[k],
                  rank: 1,
                };
              } else {
                matches[slug].rank++;
              }
            }
          }
        }
      }

      this.searchMatches = Object.keys(matches)
        .sort(function (a, b) {
          return matches[b].rank - matches[a].rank;
        })
        .map(function (k) {
          return matches[k].obj;
        })
        .slice(0, 8);
    },
    isActiveNav(page) {
      return {
        "ox-nav-active-link": this.aurochsRoot.page == page,
        "ox-nav-link": this.aurochsRoot.page != page,
      };
    },
    setNextTheme() {
      if (this.theme_index == this.themes.length - 1) {
        this.theme_index = 0;
      } else {
        this.theme_index++;
      }

      this.setTheme(this.themes[this.theme_index].theme);
    },
    setTheme(theme) {
      if (theme == "auto") {
        document.documentElement.removeAttribute("data-theme");
        localStorage.removeItem("theme", theme);
        this.theme = theme;
        this.aurochsData.theme = null;
        window.aurochs.data.theme = null;
      } else {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        this.theme = theme;
        this.aurochsData.theme = theme;
        window.aurochs.data.theme = theme;
      }
    },
    openResult(r) {
      this.$router.push(`/${r.__type}/${r.id}`);
      this.handleEscape();
    },
    highlighted(name) {
      if (this.exact) {
        return DOMPurify.sanitize(name).replace(new RegExp(this.searchText, "gi"), (match) => {
          return "<strong>" + match + "</strong>";
        });
      } else {
        let escape_string = "⌓⌓⌓";
        let highlighted_name = DOMPurify.sanitize(name);
        for (let term of this.searchText.split(" ")) {
          if (term.length > 0) {
            // via: https://stackoverflow.com/questions/3446170/escape-string-for-use-in-javascript-regex
            let regex_term = term.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

            highlighted_name = highlighted_name.replaceAll(new RegExp(regex_term, "gi"), (match) => {
              return "<" + escape_string + match + "</" + escape_string;
            });
          }
        }
        highlighted_name = highlighted_name.replaceAll(new RegExp(escape_string, "g"), "strong>");
        return highlighted_name;
      }
    },
    isTagged(r) {
      const chunks = r.search_text.split("|");
      for (let term of this.searchText.toLowerCase().split(" ")) {
        if (term.length > 0) {
          for (var i in chunks) {
            var chunk = chunks[i];
            if (chunk.substring(0, 4) == "tag:" && chunk.toLowerCase().indexOf(term) != -1) {
              return true;
            }
          }
        }
      }
      return false;
    },
    tagName(r) {
      const chunks = r.search_text.split("|");
      for (let term of this.searchText.toLowerCase().split(" ")) {
        if (term.length > 0) {
          for (var i in chunks) {
            var chunk = chunks[i];
            if (chunk.substring(0, 4) == "tag:" && chunk.toLowerCase().indexOf(term) != -1) {
              return this.highlighted(chunk.substring(4));
            }
          }
        }
      }
    },
    isStacked(r) {
      const chunks = r.search_text.split("|");
      for (let term of this.searchText.toLowerCase().split(" ")) {
        if (term.length > 0) {
          for (var i in chunks) {
            var chunk = chunks[i];
            if (chunk.substring(0, 6) == "instk:" && chunk.toLowerCase().indexOf(term) != -1) {
              return true;
            }
          }
        }
      }
      return false;
    },
    stackName(r) {
      const chunks = r.search_text.split("|");
      for (let term of this.searchText.toLowerCase().split(" ")) {
        if (term.length > 0) {
          for (var i in chunks) {
            var chunk = chunks[i];
            if (chunk.substring(0, 6) == "instk:" && chunk.toLowerCase().indexOf(term) != -1) {
              return this.highlighted(chunk.substring(6));
            }
          }
        }
      }
    },
    moveSearchSelectionUp() {
      if (this.selectedIndex === false) {
        this.selectedIndex = this.searchMatches.length - 1;
      } else {
        if (this.selectedIndex > 0) {
          this.selectedIndex -= 1;
        }
      }
    },
    moveSearchSelectionDown() {
      if (this.selectedIndex === false) {
        this.selectedIndex = 0;
      } else {
        if (this.selectedIndex < this.searchMatches.length - 1) {
          this.selectedIndex += 1;
        }
      }
    },
    hoverItem(idx) {
      this.selectedIndex = idx;
    },
    handleEnter() {
      if (this.selectedIndex !== false) {
        var r = this.searchMatches[this.selectedIndex];
        this.$router.push(`/${r.__type}/${r.id}`);
        this.handleEscape();
      }
    },
    handleCmdEnter() {
      if (this.selectedIndex !== false) {
        var r = this.searchMatches[this.selectedIndex];
        let routeData = this.$router.resolve(`/${r.__type}/${r.id}`);
        window.open(routeData.href, "_blank");
        this.handleEscape();
      }
    },
    handleEscape() {
      this.selectedIndex = false;
      this.searchText = "";
    },
    async saveFramework(framework) {
      let ret_data = await this.$sendEvent("create_framework", framework);
      this.$router.push(`/framework/${ret_data.obj_pk}`);
    },
    async createBlankFramework() {
      let ret_data = await this.$sendEvent("create_framework", {
        name: "New Framework",
      });
      this.$router.push({
        path: `/framework/${ret_data.obj_pk}`,
        query: { new: true },
      });
    },
    async createBlankSource() {
      let ret_data = await this.$sendEvent("create_source", {
        name: "New Source",
      });
      this.$router.push({
        path: `/source/${ret_data.obj_pk}`,
        query: { new: true },
      });
    },
    async createBlankStack() {
      let ret_data = await this.$sendEvent("create_stack", {
        name: "New Stack",
      });
      this.$router.push({
        path: `/stack/${ret_data.obj_pk}`,
        query: { new: true },
      });
    },
    async createBlankReport() {
      let ret_data = await this.$sendEvent("create_report", {
        name: "New Report",
      });
      this.$router.push({
        path: `/report/${ret_data.obj_pk}`,
        query: { new: true },
      });
    },
    openReleaseNotes() {
      this.releaseNotesModalOpen = true;
      document.getElementById("release-notes-modal").checked = true;
    },
    openContactOx() {
      this.contactOxModalOpen = true;
      document.getElementById("contact-ox-modal").checked = true;
    },
    closeReleaseNotes() {
      this.releaseNotesModalOpen = false;
      document.getElementById("release-notes-modal").checked = false;
    },
    image_url(file_name) {
      let url =
        window.aurochs.data.config.guide_image_url.substring(
          0,
          window.aurochs.data.config.guide_image_url.indexOf("/intel") + 1
        ) + file_name;
      return url.replaceAll("/images/guide", "");
    },
    darkMode() {
      return (
        (!this.theme && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ||
        this.theme == "dark"
      );
    },
  },
};
</script>

<style scoped>
.logo {
  width: 26px;
  height: 29px;
  margin-right: 10px;
}

.logo > a {
  fill: rgb(255, 255, 255);
}

.ox-link {
  @apply px-3 py-2  text-sm font-medium;
}

.ox-nav-link {
}
.ox-nav-active-link {
  @apply font-bold;
}

.ox-search-input {
  @apply block w-full pl-10 pr-3 py-2 border border-transparent  leading-5 bg-gray-700 text-gray-300 placeholder-gray-400 focus:outline-none focus:bg-white focus:border-white focus:ring-white focus:text-gray-900 sm:text-sm;
}

.ox-mobile-button {
  @apply inline-flex items-center justify-center p-2  hover:text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white;
}

.ox-nav-menu-items {
  @apply origin-top-right absolute z-10 right-0 mt-2 w-48  shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none divide-y divide-gray-100;
}

.ox-create-menu-items {
  @apply origin-top-right absolute z-10 right-0 mt-2 w-48  shadow-lg py-1 bg-teal-600 ring-1 ring-slate-100 ring-opacity-5 focus:outline-none;
}

.active-menu-item {
  @apply bg-gray-100;
}

.inactive-menu-item {
  /*@apply block px-4 py-2 text-sm text-gray-700;*/
}

.new-item-menu-button {
  @apply bg-sky-400  flex text-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-sky-500 focus:ring-white;
}

.active-create-menu-item {
  @apply bg-sky-700;
}

.inactive-create-menu-item {
  @apply hover:bg-sky-700 block px-4 py-2 text-sm text-slate-100;
}

.profile-menu-button {
  @apply bg-gray-800  flex text-sm text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white;
}

.mobile-notification-button {
  @apply flex-shrink-0 bg-gray-800 p-1  hover:text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-800 focus:ring-white;
}

.mobile-drop-down-menu {
  @apply block px-3 py-2  text-base font-medium hover:text-white hover:bg-gray-700;
}
.ox-nav-logo {
  @apply py-1 px-2;
}
.modal h2 {
  @apply mt-8 mb-2;
}
.modal article {
  @apply overflow-y-auto p-2 mt-4;
  max-height: 70vh;
}
.navbar {
  z-index: 100;
}
strong {
  @apply font-bold;
}
</style>
