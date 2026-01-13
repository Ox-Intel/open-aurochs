<template>
  <div class="mt-2 pb-8">
    <TabGroup :selected-index="Number(selectedTab)" @change="changeTab">
      <TabList class="tabs w-full">
        <Tab v-for="tab in tabs" v-slot="{ selected }" :key="tab.name" as="template">
          <div
            class="tab tab-bordered tab-lg indicator focus:outline-none"
            :class="selected ? 'tab-active' : ''"
            :data-cy="`tab-${tab.hash}`"
          >
            <span :class="tab.extraRotation" style="display: inline-block">
              <FontAwesomeIcon :icon="tab.icon" :class="tab.classes" />
            </span>
            <span>{{ tab.name }}</span>
            <span v-if="tab.badge" class="badge indicator-item badge-accent right-2 top-2">{{ tab.badge }}</span>
          </div>
        </Tab>
      </TabList>
      <TabPanels class="mt-8">
        <TabPanel>
          <AnalyticsPanel :report="report" :scorecards-by-framework="scorecardsByFramework" data-cy="overview-panel" />
        </TabPanel>
        <!--   <TabPanel>
          <div data-cy="all-scorecards">
            <ScorecardsPanel v-if="canView" :report="report" :scorecards-by-framework="scorecardsByFramework" />
            <div
              v-if="!canView"
              class="card w-full bg-base-200 card-bordered m-8 max-w-screen-md"
              data-cy="no-permissions"
            >
              <div class="card-body w-full">
                <div class="flex">
                  <div class="w-12 text-center">
                    <FontAwesomeIcon :icon="['fad', 'lock']" class="h-12 w-12 text-medium-grey" />
                  </div>
                  <div class="grow text-left px-4 pt-2 flex justify-between">
                    <div class="text-xl text-medium-grey">You don't have permission to see all scorecards.</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </TabPanel> -->
        <TabPanel>
          <MyScorecardsPanel :report="report" :data-cy="'scorecards'" />
          <div
            v-if="!canScore"
            class="card w-full bg-base-200 card-bordered mt-8 max-w-screen-md"
            data-cy="no-permissions"
          >
            <div class="card-body w-full">
              <div class="flex">
                <div class="w-12 text-center">
                  <FontAwesomeIcon :icon="['fad', 'lock']" class="h-12 w-12 text-medium-grey" />
                </div>
                <div class="grow text-left px-4 pt-2 flex justify-between">
                  <div class="text-xl text-medium-grey">You don't have permission to add new scorecards.</div>
                </div>
              </div>
            </div>
          </div>
        </TabPanel>
        <TabPanel>
          <NotesPanel :target="report" />
        </TabPanel>
        <TabPanel>
          <div class="max-w-screen-md pb-12" data-cy="source-list">
            <div v-for="(s, idx) in report.sources" :key="idx">
              <router-link :to="`/source/${s.id}`"
                ><a>
                  <div
                    :data-cy="`source-${idx}`"
                    class="card w-full bg-base-100 card-bordered shadow-md m-8"
                    role="button"
                  >
                    <div class="card-body w-full">
                      <div class="flex">
                        <div class="w-12 text-center">
                          <OxObjectIcon :target="s" :classes="'h-12 w-12'" />
                        </div>
                        <div class="grow text-left px-4">
                          <div class="text-xl font-bold" data-cy="name">
                            {{ s.name }}
                          </div>
                          <div class="">
                            {{ s.subtitle }}
                          </div>
                          <div class="font-light mt-4">Updated {{ formatDate(s.modified_at_ms) }}</div>
                        </div>
                        <div class="w-12">
                          <div
                            v-if="canScore"
                            data-cy="remove-source"
                            class="btn btn-circle btn-ghost hover:btn-error"
                            role="button"
                            @click.stop.prevent="removeSource(s)"
                          >
                            <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-6 w-6 align-middle" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </div> </a
              ></router-link>
            </div>
            <div v-if="report.sources.length == 0" class="card w-full bg-base-200 card-bordered m-8">
              <div class="card-body w-full">
                <div class="flex">
                  <div class="w-12 text-center">
                    <FontAwesomeIcon :icon="['fad', 'link-horizontal']" class="h-12 w-12 text-medium-grey" />
                  </div>
                  <div class="grow text-left px-4 pt-2 flex justify-between">
                    <div class="text-xl text-medium-grey">No sources added.</div>
                    <label
                      v-if="canScore"
                      data-cy="add-source"
                      for="add-source-modal"
                      class="btn btn-primary -mt-2"
                      role="button"
                    >
                      <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                      Add Source
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="report.sources.length > 0 && canScore" class="pl-8">
            <label for="add-source-modal" class="btn btn-primary -mt-2" role="button" data-cy="add-source">
              <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
              Add Source
            </label>
          </div>
          <input id="add-source-modal" type="checkbox" class="modal-toggle" />
          <div class="modal" data-cy="add-source-modal">
            <div class="modal-box relative">
              <div class="relative">
                <label for="add-source-modal" class="btn btn-sm btn-circle absolute right-0 top-0">
                  <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle" />
                </label>
              </div>
              <h3 class="text-2xl font-bold">
                <FontAwesomeIcon :icon="['fad', 'link-horizontal']" class="mr-2 align-middle text-source" />
                Add Source
              </h3>
              <p class="py-4">Which source would you like to add?</p>
              <OxSearchBox
                :options="aurochsData.sources"
                :exclude="report.sources"
                :placeholder="'Search for a source...'"
                @selected-choice="setAddSource"
              />
              <div class="flex justify-end">
                <div
                  data-cy="add-source-button"
                  role="button"
                  class="mt-4 btn btn-primary"
                  :class="{
                    'btn-disabled': !newSource || addingSource,
                    saving: addingSource,
                  }"
                  @click="addSource()"
                >
                  {{ addingSource ? "Adding..." : "Add Source" }}
                </div>
              </div>
            </div>
          </div>
        </TabPanel>
        <TabPanel>
          <DiscussionPanel :target="report" />
        </TabPanel>
        <TabPanel>
          <PermissionsPanel :target="report" :can-manage="canManage" @permissions-updated="permissionsUpdated" />
        </TabPanel>
        <!-- <TabPanel>
          <div class="max-w-screen-md pb-12" data-cy="stack-list">
            <div v-for="(s, idx) in stacks" :key="idx">
              <router-link :to="`/stack/${s.id}`"><a>
              <div
                  :data-cy="`stack-${idx}`"
                  class="card w-full bg-base-100 card-bordered shadow-md m-8"
                  role="button"
                >
                  <div class="card-body w-full">
                    <div class="flex">
                      <div class="w-12 text-center">
                        <OxObjectIcon :target="s" :classes="'h-12 w-12'" />
                      </div>
                      <div class="grow text-left px-4">
                        <div class="text-xl font-bold" data-cy="name">
                          {{ s.name }}
                        </div>
                        <div class="">
                          {{ s.subtitle }}
                        </div>
                        <div class="font-light mt-4">Updated {{ formatDate(s.modified_at_ms) }}</div>
                      </div>
                      <div class="w-12">
                        <div
                          v-if="canScore"
                          data-cy="remove-stack"
                          class="btn btn-circle btn-ghost hover:btn-error"
                          role="button"
                          @click.stop.prevent="removeStack(s)"
                        >
                          <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-6 w-6 align-middle" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </a></router-link>
            </div>
            <div v-if="stacks.length == 0" class="card w-full bg-base-200 card-bordered m-8">
              <div class="card-body w-full">
                <div class="flex">
                  <div class="w-12 text-center">
                    <FontAwesomeIcon :icon="['fad', 'layer-group']" class="h-12 w-12 text-medium-grey" />
                  </div>
                  <div class="grow text-left px-4 pt-2 flex justify-between">
                    <div class="text-xl text-medium-grey">Not in any stacks.</div>
                    <label
                      v-if="canScore"
                      data-cy="add-stack-to-report"
                      for="add-stack-modal"
                      class="btn btn-primary -mt-2"
                      role="button"
                    >
                      <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                      Add to Stack
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="stacks.length > 0 && canScore" class="pl-8">
            <label for="add-stack-modal" class="btn btn-primary -mt-2" role="button" data-cy="add-stack-to-report">
              <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
              Add to Stack
            </label>
          </div>
          <input id="add-stack-modal" type="checkbox" class="modal-toggle" />
          <div class="modal" data-cy="add-stack-modal">
            <div class="modal-box relative">
              <div class="relative">
                <label for="add-stack-modal" class="btn btn-sm btn-circle absolute right-0 top-0">
                  <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle" />
                </label>
              </div>
              <h3 class="text-2xl font-bold">
                <FontAwesomeIcon :icon="['fad', 'layer-group']" class="mr-2 align-middle text-stack" />
                Add to Stack
              </h3>
              <p class="py-4">To which stack would you like to add this report?</p>
              <OxSearchBox
                :options="aurochsData.stacks"
                :exclude="stacks"
                :placeholder="'Search for a stack...'"
                @selected-choice="setAddStack"
              />
              <div class="flex justify-end">
                <div
                  data-cy="add-stack-to-report-from-modal"
                  role="button"
                  class="mt-4 btn btn-primary"
                  :class="{
                    'btn-disabled': !newStack || addingStack,
                    saving: addingStack,
                  }"
                  @click="addStack()"
                >
                  {{ addingStack ? "Adding..." : "Add to Stack" }}
                </div>
              </div>
            </div>
          </div>
        </TabPanel> -->
      </TabPanels>
    </TabGroup>
  </div>
</template>

<script>
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import AnalyticsPanel from "./AnalyticsPanel.vue";
import MyScorecardsPanel from "./MyScorecardsPanel.vue";
import DiscussionPanel from "../common/DiscussionPanel.vue";
import NotesPanel from "../common/NotesPanel.vue";
import PermissionsPanel from "../common/PermissionsPanel.vue";
import { ref } from "vue";
import OxSearchBox from "../../components/common/OxSearchBox.vue";
import OxObjectIcon from "../../components/common/icons/OxObjectIcon.vue";
import { checkCanScore, checkCanView, checkCanEdit, checkCanManage } from "../../mixins/permissions.js";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faUnlock } from "@fortawesome/pro-duotone-svg-icons/faUnlock";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faFileCsv } from "@fortawesome/pro-duotone-svg-icons/faFileCsv";
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faFilePdf } from "@fortawesome/pro-duotone-svg-icons/faFilePdf";
import { faFilePowerpoint } from "@fortawesome/pro-duotone-svg-icons/faFilePowerpoint";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faLock } from "@fortawesome/pro-duotone-svg-icons/faLock";
import { faRotate } from "@fortawesome/pro-duotone-svg-icons/faRotate";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faMemo } from "@fortawesome/pro-duotone-svg-icons/faMemo";
import { faMemoPad } from "@fortawesome/pro-duotone-svg-icons/faMemoPad";
import { faNote } from "@fortawesome/pro-duotone-svg-icons/faNote";
import { faNotes } from "@fortawesome/pro-duotone-svg-icons/faNotes";
import { faChartCandlestick } from "@fortawesome/pro-duotone-svg-icons/faChartCandlestick";
import { faPollPeople } from "@fortawesome/pro-duotone-svg-icons/faPollPeople";
import { faBarsProgress } from "@fortawesome/pro-duotone-svg-icons/faBarsProgress";
import { faLinkHorizontal } from "@fortawesome/pro-duotone-svg-icons/faLinkHorizontal";

library.add(
  faUnlock,
  faTrashCan,
  faFileCsv,
  faClone,
  faPen,
  faFileLines,
  faChartSimpleHorizontal,
  faCompass,
  faMessages,
  faFiles,
  faFilePdf,
  faFilePowerpoint,
  faXmark,
  faCheck,
  faLock,
  faRotate,
  faPlus,
  faMemo,
  faMemoPad,
  faNote,
  faNotes,
  faChartCandlestick,
  faPollPeople,
  faBarsProgress,
  faLinkHorizontal
);

export default {
  components: {
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    AnalyticsPanel,
    // ScorecardsPanel,
    MyScorecardsPanel,
    DiscussionPanel,
    NotesPanel,
    PermissionsPanel,
    FontAwesomeIcon,
    OxSearchBox,
    // OxSlider,
    // OxTextarea,
    OxObjectIcon,
    // OxOwnerBadges,
    // OxTags,
    // OxAvatar,
  },
  mixins: [formatDate],
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    scorecardsByFramework: {
      type: Object,
      default: () => {},
    },
  },
  emits: ["permissions-updated"],
  setup() {
    const tabs = [
      {
        name: "Overview",
        hash: "overview",
        classes: "mr-2 fa-rotate-90 fa-flip-vertical",
        icon: ["fad", "chart-candlestick"],
        extraRotation: "fa-rotate-270 mb-2",
      },
      // {
      //   name: "All Scorecards",
      //   hash: "allscorecards",
      //   classes: "mr-2",
      //   icon: ["fad", "poll-people"],
      // },
      {
        name: "Scorecards",
        hash: "scorecards",
        classes: "mr-2",
        icon: ["fad", "poll-people"],
        // icon: ["fad", "bars-progress"],
      },
      {
        name: "Notes",
        hash: "notes",
        classes: "mr-2",
        // icon: ["fad", "memo"],
        // icon: ["fad", "note"],
        // icon: ["fad", "notes"],
        icon: ["fad", "memo-pad"],
      },
      {
        name: "Sources",
        hash: "sources",
        classes: "mr-2",
        icon: ["fad", "link-horizontal"],
      },
      // {
      //   name: "Stacks",
      //   hash: "stacks",
      //   classes: "mr-2",
      //   icon: ["fad", "layer-group"],
      // },
      {
        name: "Discussion",
        hash: "discussion",
        classes: "mr-2",
        icon: ["fad", "messages"],
      }, // badge: 2
      {
        name: "Permissions",
        hash: "permissions",
        classes: "mr-2",
        icon: ["fad", "lock"],
      },
    ];
    const addingSource = ref(false);
    const addingStack = ref(false);
    const newSource = ref(false);
    const newStack = ref(false);
    const selectedTab = ref(0);

    return {
      tabs,
      aurochsData: useAurochsData(),
      addingSource,
      newSource,
      addingStack,
      newStack,
      selectedTab,
    };
  },
  computed: {
    // stacks() {
    //   let stacks = [];
    //   for (let j in this.report.stack_ids) {
    //     stacks.push(this.aurochsData.stacks[this.report.stack_ids[j]]);
    //   }
    //   return stacks;
    // },
    canScore() {
      return checkCanScore(this.report, this.aurochsData.user);
    },
    canView() {
      return checkCanView(this.report, this.aurochsData.user);
    },
    canEdit() {
      return checkCanEdit(this.report, this.aurochsData.user);
    },
    canManage() {
      return checkCanManage(this.report, this.aurochsData.user);
    },
  },
  watch: {
    $route: {
      deep: true,
      handler: function (newVal) {
        if (newVal.hash) {
          for (var t in this.tabs) {
            if (this.tabs[t].hash == newVal.hash.substring(1)) {
              this.selectedTab = t;
              break;
            }
          }
        } else {
          this.selectedTab = 0;
        }
      },
    },
  },
  mounted() {
    if (this.$route.hash) {
      for (var t in this.tabs) {
        if (this.tabs[t].hash == this.$route.hash.substring(1)) {
          this.selectedTab = t;
          break;
        }
      }
    } else {
      this.selectedTab = 0;
    }
  },
  methods: {
    setAddSource(source) {
      this.newSource = source;
    },
    permissionsUpdated() {
      // console.log("permissionsUpdated");
      this.canScore = checkCanScore(this.report, this.aurochsData.user);
      this.canView = checkCanView(this.report, this.aurochsData.user);
      this.canEdit = checkCanEdit(this.report, this.aurochsData.user);
      this.canManage = checkCanManage(this.report, this.aurochsData.user);
      this.$emit("permissions-updated");
    },
    async addSource() {
      this.addingSource = true;
      var data = {
        report_id: this.report.id,
        source_id: this.newSource.id,
      };
      await this.$sendEvent("add_source_to_report", data);
      this.addingSource = false;
      this.newSource = false;
      this.emitter.emit("clearSearchBox", { previousSelected: this.newSource });
      document.getElementById("add-source-modal").checked = false;
    },
    async removeSource(s) {
      if (window.confirm("Are you sure you want remove this source from the report?")) {
        var data = {
          report_id: this.report.id,
          source_id: s.id,
        };
        await this.$sendEvent("remove_source_from_report", data);
      }
      return false;
    },
    setAddStack(stack) {
      this.newStack = stack;
    },
    async addStack() {
      this.addingStack = true;
      var data = {
        report_id: this.report.id,
        stack_id: this.newStack.id,
      };
      await this.$sendEvent("add_report_to_stack", data);
      this.addingStack = false;
      this.newStack = false;
      this.emitter.emit("clearSearchBox", { previousSelected: this.newStack });
      document.getElementById("add-stack-modal").checked = false;
    },
    async removeStack(s) {
      if (window.confirm("Are you sure you want remove this report from the stack?")) {
        var data = {
          report_id: this.report.id,
          stack_id: s.id,
        };
        await this.$sendEvent("remove_report_from_stack", data);
      }
      return false;
    },
    changeTab(tab) {
      this.$router.push(`/report/${this.report.id}/#${this.tabs[tab].hash}`);
    },
  },
};
</script>
