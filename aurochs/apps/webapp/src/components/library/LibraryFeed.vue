<template>
  <section aria-labelledby="library-feed-heading" class="overflow-hidden h-full">
    <div class="h-full">
      <div class="bg-base-100 border-base-200">
        <div class="w-full">
          <div class="min-h-40">
            <div class="flex flex-col">
              <div class="flex flex-row align-middle place-items-center">
                <FontAwesomeIcon v-if="private_only" :icon="['fad', 'books']" class="h-6 w-6 mr-2 mt-1 ml-1" />
                <FontAwesomeIcon v-if="!private_only" :icon="['fad', 'globe']" class="h-6 w-6 mr-2 mt-1 ml-1" />
                <div class="font-bold text-2xl mt-2">{{ title }}</div>
                <!-- <div class="">
                  <button
                    type="button"
                    role="button"
                    class="btn btn-primary btn-outline"
                    :data-cy="`library-new-${list_type}`"
                    @click="createRecord"
                  >
                    + New {{ title }}
                  </button>
                </div> -->
              </div>
              <div class="form-control mt-2 z-10 border-base-300">
                <div class="input-group border-base-300">
                  <input
                    v-model="searchText"
                    type="text"
                    name="search"
                    data-cy="search"
                    class="input input-bordered w-1/3 grow focus:outline-none focus-visible:ring focus-visible:ring-primary focus-visible:ring-opacity-5 border-base-300"
                    placeholder="Search..."
                    autofocus="true"
                    @input="updateList"
                  />
                  <select
                    id="filterOrgModel"
                    v-model="filterOrgModel"
                    name="filterOrgModel"
                    class="select select-bordered rounded-none border-base-300"
                    data-cy="filter"
                    @change="updateList"
                  >
                    <option v-for="(opt, idx) in selectOptions" :key="idx" :value="opt">
                      {{ opt.record?.name }}
                    </option>
                  </select>
                  <select
                    id="sortCategory"
                    v-model="sortCategory"
                    name="sortCategory"
                    class="select select-bordered rounded-none border-base-300"
                    data-cy="sort"
                    @change="updateList"
                  >
                    <option value="name">Name</option>
                    <option value="updated">Updated Date</option>
                    <option value="created">Created Date</option>
                  </select>
                  <OxSortToggleIcon :sort-asc="sortAsc" @toggle="toggle" />
                </div>
              </div>
              <div class="w-full flex border border-base-300 mb-6 border-t-0 toggle-group" data-cy="library-filter">
                <div class="caption uppercase align-middle px-4 py-3 font-bold text-sm text-neutral">Show:</div>
                <div class="btn-group w-full">
                  <div
                    class="btn border-l-0 border-t-0 border-y-base-300 border-r-base-300 hover:border-r-base-300 text-neutral hover:border-y-medium-grey relative"
                    :class="
                      showFrameworks
                        ? 'bg-base-100 hover:bg-base-100 '
                        : 'hover:bg-base-200 bg-base-300 text-medium-grey text-opacity-50'
                    "
                    data-cy="filter-framework"
                    @click="toggleFrameworks"
                  >
                    <OxObjectIcon
                      :type="'framework'"
                      :classes="'h-4 w-4 mr-2'"
                      :greyscale="!showFrameworks"
                      :small="true"
                      :scale="0.4"
                    />
                    <div>Frameworks</div>
                  </div>
                  <div
                    class="btn border-l-0 border-t-0 border-y-base-300 border-r-base-300 hover:border-r-base-300 text-neutral hover:border-y-medium-grey relative"
                    :class="
                      showReports
                        ? 'bg-base-100 hover:bg-base-100 '
                        : 'hover:bg-base-200 bg-base-300 text-medium-grey text-opacity-50'
                    "
                    data-cy="filter-report"
                    @click="toggleReports"
                  >
                    <OxObjectIcon :type="'report'" :classes="'h-4 w-4 mr-2'" :greyscale="!showReports" />
                    <div>Reports</div>
                  </div>
                  <div
                    class="btn border-l-0 border-t-0 border-y-base-300 border-r-base-300 hover:border-r-base-300 text-neutral hover:border-y-medium-grey relative"
                    :class="
                      showStacks
                        ? 'bg-base-100 hover:bg-base-100 '
                        : 'hover:bg-base-200 bg-base-300 text-medium-grey text-opacity-50'
                    "
                    data-cy="filter-stack"
                    @click="toggleStacks"
                  >
                    <OxObjectIcon :type="'stack'" :classes="'h-4 w-4 mr-2'" :greyscale="!showStacks" />
                    <div>Stacks</div>
                  </div>
                  <div
                    class="btn border-x-0 border-y-base-300 text-neutral hover:border-y-medium-grey relative"
                    :class="
                      showSources
                        ? 'bg-base-100 hover:bg-base-100 '
                        : 'hover:bg-base-200 bg-base-300 text-medium-grey text-opacity-50'
                    "
                    data-cy="filter-source"
                    @click="toggleSources"
                  >
                    <OxObjectIcon :type="'source'" :classes="'h-4 w-4 mr-2'" :greyscale="!showSources" />
                    <div>Sources</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="py-4 shadow-inner bg-base-200 rounded-xl -mt-4 h-[70vh]">
            <ul role="list" class="flow-root h-full overflow-y-auto px-8 py-2">
              <li
                v-for="(activity, act_idx) in filteredAndSortedFeedObjects"
                :key="act_idx"
                data-cy="library-feed-item"
                class="bg-base-100 border border-base-300 rounded-lg mb-2 flex pt-1 pb-2 space-x-3 hover:border-dark-grey shadow-sm"
              >
                <!-- TODO: updating routing to webapp prefix -->
                <router-link :to="`/${activity.__type}/${activity.id}`" class="w-full">
                  <ActivityListItem
                    :activity="activity"
                    :teams="teams"
                    :search-text="searchText"
                    :private_only="private_only"
                  />
                </router-link>
              </li>
              <li
                v-if="filteredAndSortedFeedObjects.length == 0"
                class="bg-base-200 p-8 mt-8 rounded align-middle text-center border-0"
              >
                No Results Found.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import ActivityListItem from "../common/ActivityListItem";
import OxSortToggleIcon from "../common/OxSortToggleIcon.vue";
import OxObjectIcon from "../common/icons/OxObjectIcon.vue";
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import { checkCanSee } from "../../mixins/permissions.js";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faLock } from "@fortawesome/pro-duotone-svg-icons/faLock";
import { faUser } from "@fortawesome/pro-duotone-svg-icons/faUser";
import { faBooks } from "@fortawesome/pro-duotone-svg-icons/faBooks";
import { faUserPlus } from "@fortawesome/pro-duotone-svg-icons/faUserPlus";

library.add(faGlobe, faLock, faUser, faBooks, faUserPlus);

export default {
  components: {
    ActivityListItem,
    OxSortToggleIcon,
    OxObjectIcon,
    FontAwesomeIcon,
  },
  props: {
    activities: {
      type: Array,
      required: false,
      default: () => [],
    },
    title: {
      type: String,
      default: "",
    },
    list_type: {
      type: String,
      default: "",
    },
    private_only: {
      type: Boolean,
      default: true,
    },
  },
  // emits: ["createRecord"],
  setup() {
    const sortAsc = ref(true);
    const sortCategory = ref("created");
    const searchText = ref("");
    // const filteredAndSortedFeedObjects = ref([]);
    const filterOrgModel = ref({
      label: "All",
      key: "all",
      record: { name: "All" },
      icon: "collection",
    });
    const showFrameworks = ref(true);
    const showReports = ref(true);
    const showSources = ref(true);
    const showStacks = ref(true);

    const selectOptions = ref([]);
    const user = ref({});
    const teams = ref({});
    const organizations = ref({});

    return {
      sortAsc,
      sortCategory,
      searchText,
      selectOptions,
      user,
      teams,
      organizations,
      aurochsData: useAurochsData(),
      filterOrgModel,
      // filteredAndSortedFeedObjects,
      showFrameworks,
      showReports,
      showSources,
      showStacks,
    };
  },
  computed: {
    userId() {
      return this.user.id;
    },
    filteredAndSortedFeedObjects() {
      let allActivities = [];
      let allPotentialActivities = [];
      let matches = [];
      let frameworks = [];
      if (this.showFrameworks) {
        frameworks = Object.values(this.aurochsData.frameworks || []);
      }
      let reports = [];
      if (this.showReports) {
        reports = Object.values(this.aurochsData.reports || []);
      }
      let sources = [];
      if (this.showSources) {
        sources = Object.values(this.aurochsData.sources || []);
      }
      let stacks = [];
      if (this.showStacks) {
        stacks = Object.values(this.aurochsData.stacks || []);
      }
      allPotentialActivities = [...frameworks, ...reports, ...sources, ...stacks];
      for (let act of allPotentialActivities) {
        if (checkCanSee(act, this.aurochsData.user)) {
          allActivities.push({ ...act });
        }
      }

      let use_search = false;
      let lower_search_text = "";
      // console.log(this.searchText);
      if (this.searchText && this.searchText.length > 0) {
        lower_search_text = this.searchText.toLowerCase();
        use_search = true;
      }
      for (let a of allActivities) {
        // console.log(a.value)
        let matches_filter = false;
        let i_am_only_admin = false;
        let entirely_private = false;

        // See if it's in the search
        if (!use_search || a.search_text.toLowerCase().indexOf(lower_search_text) != -1) {
          // See if I'm the only admin.
          let found_me = false;
          for (let perm in a.permissions) {
            if (
              perm.substring(0, 2) == "U-" &&
              perm.substring(2) == this.aurochsData.user.id &&
              a.permissions[perm].substring(3) == "1"
            ) {
              found_me = true;
              break;
            }
          }
          if (found_me) {
            let num_admins = 0;
            for (let p in a.permissions) {
              if (a.permissions[p].substring(3) == 1) {
                num_admins++;
              }
            }
            if (num_admins == 1) {
              i_am_only_admin = true;
            }
          }
          if (i_am_only_admin) {
            if (Object.keys(a.permissions).length == 1) {
              entirely_private = true;
            }
          }
          a.i_am_only_admin = i_am_only_admin;
          a.entirely_private = entirely_private;

          // We're not searching or it's in the search.
          if (this.filterOrgModel.key != "all") {
            if (!this.private_only) {
              if (this.filterOrgModel.key.startsWith("team_")) {
                for (let perm in a.permissions) {
                  if (
                    perm.substring(0, 2) == "T-" && // It's a team
                    perm.substring(2) == this.filterOrgModel.pk && // That matches the filter ID
                    (a.permissions[perm].substring(0, 1) == "1" || a.permissions[perm].substring(1, 2) == "1") // With at least score or view permissions.
                  ) {
                    matches_filter = true;
                  }
                }
              }
              if (this.filterOrgModel.key.startsWith("organization_")) {
                for (let perm in a.permissions) {
                  if (
                    perm.substring(0, 2) == "O-" && // It's an org
                    perm.substring(2) == this.filterOrgModel.pk && // That matches the filter ID
                    (a.permissions[perm].substring(0, 1) == "1" || a.permissions[perm].substring(1, 2) == "1") // With at least score or view permissions.
                  ) {
                    matches_filter = true;
                  }
                }
              }
            } else {
              if (this.filterOrgModel.key == "private" && a.i_am_only_admin && a.entirely_private) {
                matches_filter = true;
              }
              if (this.filterOrgModel.key == "shared" && a.i_am_only_admin && !a.entirely_private) {
                matches_filter = true;
              }
            }
          } else {
            matches_filter = true;
          }
        }
        if (
          (this.private_only && i_am_only_admin && matches_filter) ||
          (!this.private_only && !i_am_only_admin && matches_filter)
        ) {
          matches.push(a);
        }
      }
      // console.log(matches)
      if (this.sortCategory) {
        matches.sort((a, b) => {
          switch (this.sortCategory) {
            case "name":
              if (!this.sortAsc) {
                return a.name.localeCompare(b.name);
              } else {
                return b.name.localeCompare(a.name);
              }
            case "updated":
              if (!this.sortAsc) {
                return a.modified_at_ms - b.modified_at_ms;
              } else {
                return b.modified_at_ms - a.modified_at_ms;
              }
            default:
              // case "created":
              if (!this.sortAsc) {
                return a.created_at_ms - b.created_at_ms;
              } else {
                return b.created_at_ms - a.created_at_ms;
              }
          }
        });
      }
      // console.log(matches)
      // this.filteredAndSortedFeedObjects = matches;
      return matches;
      // console.log(this.filteredAndSortedFeedObjects)
    },
  },
  mounted() {
    // this.sortActivities();
    this.user = this.aurochsData.user;
    const teams = this.aurochsData?.teams ? Object.values(this.aurochsData.user.teams) : [];
    const organizations = this.aurochsData?.organizations ? Object.values(this.aurochsData.user.organizations) : [];

    if (this.private_only) {
      const all = [
        {
          label: "All",
          key: "all",
          record: { name: "All" },
          icon: "collection",
        },
      ];
      const mine = [
        {
          key: "private",
          label: "Private",
          icon: "user",
          record: { name: "Private" },
        },
      ];
      const shared = [
        {
          key: "shared",
          label: "Shared",
          icon: "user",
          record: { name: "Shared" },
        },
      ];

      this.selectOptions = [...all, ...mine, ...shared];
    } else {
      const all = [
        {
          label: "All",
          key: "all",
          record: { name: "All" },
          icon: "collection",
        },
      ];
      const select_organizations = organizations.map((org) => {
        return {
          key: `organization_${org.id}`,
          label: org?.name,
          pk: org?.id,
          icon: "usersgroup",
          record: org,
        };
      });
      const select_teams = teams.map((team) => {
        return {
          key: `team_${team.id}`,
          label: team?.name,
          pk: team?.id,
          icon: "users",
          record: team,
        };
      });
      // Pulling this for two-column layout now.
      // const mine = [
      //   {
      //     key: "mine",
      //     label: "Mine",
      //     icon: "user",
      //     record: { name: "Mine" },
      //   },
      // ];

      this.selectOptions = [
        ...all,
        ...select_organizations,
        ...select_teams,
        // ...mine,
      ];
    }
    this.updateList();
  },
  methods: {
    updateList() {},
    toggle() {
      this.sortAsc = !this.sortAsc;
      this.updateList();
    },
    toggleFrameworks() {
      this.showFrameworks = !this.showFrameworks;
      this.updateList();
    },
    toggleReports() {
      this.showReports = !this.showReports;
      this.updateList();
    },
    toggleSources() {
      this.showSources = !this.showSources;
      this.updateList();
    },
    toggleStacks() {
      this.showStacks = !this.showStacks;
      this.updateList();
    },
  },
};
</script>
<style scoped>
.input-group .btn {
  height: 3rem;
  min-height: 3rem;
  /*@apply bg-base-100 border-l-0 border-t-0 border-y-base-300 border-r-base-300 text-neutral hover:text-neutral hover:bg-base-200;*/
  /*background-color: hsl(var(--bc) / var(--tw-border-opacity));*/
}
.input-group .btn-group .btn {
  @apply rounded-none;
}
.input-group :last-child {
  @apply rounded-bl-none rounded-br-none;
}
.input-group :first-child {
  @apply rounded-bl-none rounded-br-none;
}
.toggle-group {
  @apply rounded-bl-md rounded-br-md;
}
.toggle-group :last-child,
.toggle-group .btn-group :last-child {
  @apply rounded-bl-none rounded-br-md;
}
.toggle-group :first-child {
  @apply rounded-bl-md rounded-br-none;
}
.toggle-group .btn-group,
.toggle-group .btn-group .btn {
  @apply rounded-none;
}
.toggle-group .btn-group .btn {
  @apply flex-grow;
}
</style>
