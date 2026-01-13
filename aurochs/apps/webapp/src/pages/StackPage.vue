<template>
  <DefaultLayout class="">
    <div v-if="!stack || !canSee">
      <div class="w-full min-h-[75vh]">
        <div class="card w-full bg-base-200 card-bordered mt-32 mx-auto max-w-screen-md" data-cy="not-found">
          <div v-if="!stack" class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <OxObjectIcon :type="'stack'" :classes="'h-12 w-12'" :greyscale="true" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Stack not found.</div>
                <div class="text-xl text-dark-grey">
                  This stack either doesn't exist, or you don't have permissions to view it.
                </div>
              </div>
            </div>
          </div>
          <div v-else class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <FontAwesomeIcon :icon="['fad', 'lock']" class="h-12 w-12 text-medium-grey" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Stack is private.</div>
                <div class="text-xl text-dark-grey">
                  You don't have permissions to view this stack. If you think this is incorrect, please contact an
                  administrator: {{ admin_list }}.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <main v-if="stack && canSee" class="" data-cy="stack">
      <div class="w-full">
        <!-- Main Space -->
        <div class="w-full min-h-[75vh]">
          <div class="w-full">
            <div class="w-full">
              <div class="w-full">
                <article class="prose max-w-none">
                  <div class="flex flex-nowrap mb-4 w-full gap-2 lg:flex-nowrap flex-wrap">
                    <OxObjectIcon
                      :type="'stack'"
                      :classes="(stack?.subtitle || editing ? 'w-12 h-12' : 'w-12 h-12') + ' mr-2 align-middle'"
                    />
                    <div class="block grow">
                      <h1 class="py-0 my-0">
                        <div v-if="!editing" data-cy="name" :class="stack?.subtitle ? 'mt-0.5' : 'mt-1'">
                          {{ stack?.name }}
                        </div>
                        <div v-if="editing" class="w-full max-w-[70vw]">
                          <input
                            v-model="formData.name"
                            data-cy="input-stack-name"
                            placeholder="stack Title"
                            autofocus
                            type="text"
                            class="w-auto max-w-100 text-4xl p-0 font-extra-bold border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-medium-grey focus:border-medium-grey text-neutral mt-0.5"
                            :style="`width: ${
                              3 + (formData?.name?.length || 0) * 0.8
                            }ch; max-width: 100%; min-width: 250px;`"
                          />
                        </div>
                      </h1>
                      <div v-if="editing" class="w-full max-w-[70vw]">
                        <input
                          v-model="formData.subtitle"
                          data-cy="input-stack-subtitle"
                          type="text"
                          placeholder="Stack subtitle..."
                          class="w-auto max-w-100 text-lg font-light p-0 border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-medium-grey focus:border-medium-grey text-neutral"
                          :style="`width: ${
                            3 + (formData?.subtitle?.length || 0) * 0.7
                          }ch; max-width: 100%; min-width: 250px;`"
                        />
                      </div>
                      <p
                        v-if="!editing"
                        class="text-lg font-light prose-p pr-4 my-0 max-h-20 p-0 overflow-hidden"
                        data-cy="subtitle"
                      >
                        {{ stack?.subtitle }}
                      </p>
                    </div>
                    <template v-if="editing">
                      <button
                        type="button"
                        role="button"
                        data-cy="cancel"
                        class="ml-8 btn btn-outline btn-base-300 hover:btn-error"
                        @click="cancel"
                      >
                        <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2 w-4 h-4 align-middle" />
                        Cancel
                      </button>
                      <button
                        type="button"
                        role="button"
                        data-cy="save"
                        class="btn btn-success"
                        :class="saving ? 'saving' : ''"
                        :disabled="saving"
                        @click="saveStack"
                      >
                        <FontAwesomeIcon v-if="!saving" :icon="['fad', 'check']" class="mr-2 w-4 h-4 align-middle" />
                        <FontAwesomeIcon
                          v-if="saving"
                          :icon="['fad', 'rotate']"
                          class="mr-2 w-4 h-4 align-middle fa-spin"
                        />
                        {{ saving ? "Saving..." : "Save" }}
                      </button>
                    </template>

                    <template v-if="!editing">
                      <label
                        v-if="canEdit"
                        data-cy="add-report-to-stack"
                        role="button"
                        class="btn btn-primary"
                        for="add-report-modal"
                      >
                        <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2 align-middle" />
                        Add Report
                      </label>

                      <button
                        v-if="canEdit"
                        type="button"
                        data-cy="edit"
                        title="Edit Stack"
                        role="button"
                        class="btn btn-outline btn-primary"
                        @click="startEditing"
                      >
                        <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2 align-middle" />
                        Edit
                      </button>
                      <div class="dropdown dropdown-end -ml-2">
                        <button
                          v-if="canView"
                          data-cy="download-report"
                          type="button"
                          role="button"
                          title="Download Report"
                          class="btn btn-outline btn-primary whitespace-nowrap block ml-2"
                          tabindex="40"
                        >
                          <FontAwesomeIcon :icon="['fad', 'download']" class="mr-2 align-middle" />
                          Export
                        </button>
                        <ul
                          tabindex="0"
                          class="dropdown-content menu p-2 mt-0 shadow-md bg-base-100 rounded-box w-auto whitespace-nowrap"
                        >
                          <li>
                            <a href="#" class="no-underline" @click="openDownload()">
                              <FontAwesomeIcon :icon="['fad', 'file-pdf']" class="mr-2 w-8 h-8" />
                              Download PDF
                            </a>
                          </li>
                          <li>
                            <a href="#" class="no-underline" @click="downloadCSV()">
                              <FontAwesomeIcon :icon="['fad', 'file-csv']" class="mr-2 w-8 h-8" />
                              Download CSV
                            </a>
                          </li>
                          <!-- <li>
                            <a href="#" class="no-underline" @click="downloadPPT()">
                              <FontAwesomeIcon :icon="['fad', 'file-powerpoint']" class="mr-2 w-8 h-8" />
                              Download Powerpoint
                            </a>
                          </li> -->
                        </ul>
                      </div>
                      <!--                    <button
                        data-cy="open-permissions"
                        type="button"
                        role="button"
                        title="Permissions"
                        class="btn btn-outline btn-primary"
                        @click="openPermissions"
                      >
                        <FontAwesomeIcon :icon="['fad', 'unlock']" class="mr-2 align-middle" />
                        Permissions
                      </button> -->
                      <button
                        v-if="canManage"
                        type="button"
                        data-cy="delete"
                        title="Delete Stack"
                        role="button"
                        class="btn btn-outline btn-error"
                        @click="deleteStack"
                      >
                        <FontAwesomeIcon :icon="['fad', 'trash-can']" class="mr-2 align-middle" />
                        Delete
                      </button>
                    </template>
                  </div>

                  <OxTags v-if="!editing" :target="stack" :can-edit="canEdit" />
                </article>
              </div>
            </div>
          </div>
          <div class="mx-auto mt-2 pb-8">
            <TabGroup :selected-index="Number(selectedTab)" @change="changeTab">
              <TabList class="tabs w-full">
                <Tab
                  v-for="tab in tabs"
                  v-slot="{ selected }"
                  :key="tab.name"
                  :data-cy="`tab-${tab.hash}`"
                  as="template"
                >
                  <div class="tab tab-bordered tab-lg focus:outline-none" :class="selected ? 'tab-active' : ''">
                    <span :class="tab.extraRotation" style="display: inline-block">
                      <FontAwesomeIcon v-if="!tab.frameworkIcon" :icon="tab.icon" :class="tab.class" />
                      <OxObjectIcon
                        v-if="tab.frameworkIcon"
                        :type="'framework'"
                        :classes="'h-8 w-8 mt-1 -mr-0.5'"
                        :greyscale="true"
                        :tab-icon="true"
                      />
                    </span>
                    <span>{{ tab.name }}</span>
                  </div>
                </Tab>
              </TabList>
              <TabPanels class="mt-8">
                <TabPanel>
                  <div ref="overview" class="mr-24 relative addExportPadding" data-cy="overview">
                    <DownloadButton
                      v-if="reports?.length > 0"
                      class="right-0 top-0 absolute btn btn-ghost btn-border-base-200 removedInExport"
                      @click.stop.prevent="downloadArea($refs.overview, stack?.name)"
                    />
                    <div v-for="(r, idx) in reports" :key="idx" class="flex m-2 h-16" :data-cy="`report-${idx}`">
                      <div class="w-1/4 text-md font-bold h-16 pt-4">
                        <router-link :to="`/report/${r.id}`"
                          ><a>
                            <div class="flex cursor-pointer">
                              <OxObjectIcon :type="'report'" :classes="'h-6 w-6 mr-1 '" />
                              <div class="" data-cy="name">
                                {{ r.name }}
                              </div>
                            </div>
                          </a></router-link
                        >
                      </div>
                      <div
                        class="mr-2 mt-0.5 w-16 h-14 box rounded border border-base-300 text-medium-grey text-center align-middle px-1 pt-2 pb-0"
                      >
                        <div class="text-xs mb-0">Scores</div>
                        <div class="text-xl font-bold -mt-1 mb-0" data-cy="scorecard-count">
                          {{ r.scorecards.length }}
                        </div>
                      </div>
                      <div class="w-full">
                        <div
                          v-if="r.scorecards.length == 0"
                          class="text-medium-grey w-full text-lg inline-block p-2 py-3 mt-1"
                        >
                          No scores.
                        </div>
                        <div
                          v-if="r.scorecards.length > 0"
                          :style="`width: ${r.ox_score}%;`"
                          class="rounded-sm text-ox-score-content p-4 py-3 mt-1 text-xl font-bold inline-block"
                          :class="r.has_skipped ? 'bg-medium-grey' : 'bg-ox-score'"
                          data-cy="ox-bar"
                        >
                          <span v-if="r.ox_score > 6"
                            >{{ r.ox_score }}<span class="text-sm">%</span>
                            <div
                              v-if="r?.has_skipped"
                              class="star inline-block tooltip tooltip-right cursor-pointer"
                              data-tip="At least one criteria was skipped by all scorers."
                            >
                              <div class="text-md">*</div>
                            </div></span
                          >
                          <span v-if="r.ox_score <= 6">&nbsp;</span>
                        </div>
                        <div
                          v-if="r.scorecards.length > 0 && r.ox_score <= 6"
                          class="inline-block font-bold text-xl py-4 px-2"
                        >
                          {{ r.ox_score }}<span class="text-sm">%</span>
                          <div
                            v-if="r?.has_skipped"
                            class="star inline-block tooltip tooltip-right cursor-pointer"
                            data-tip="At least one criteria was skipped by all scorers."
                          >
                            <div class="text-md">*</div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </TabPanel>
                <TabPanel>
                  <!-- Frameworks -->
                  <div class="" data-cy="explorer">
                    <AnalyticsPanel
                      :report="{}"
                      :scorecards-by-framework="dataByFramework"
                      :hide-confidence="true"
                      :hide-ox-score="true"
                      :hide-noise="true"
                      :show-average-noise-warning="true"
                      :hide-suggestions="true"
                      :allow-group-by-report="true"
                    />
                  </div>
                </TabPanel>

                <TabPanel>
                  <div class="w-full" data-cy="reports">
                    <!-- Reports -->
                    <div data-cy="report-list" class="w-full">
                      <div
                        v-for="(r, idx) in reports"
                        :key="idx"
                        :ref="`report-${idx}`"
                        class="flex cursor-pointer"
                        :data-cy="`report-${slugify(r.name)}`"
                      >
                        <div class="card w-full bg-base-200 card-bordered mb-16 mr-24 shadow-inner">
                          <div class="card-body w-full">
                            <div class="flex">
                              <OxObjectIcon :type="'report'" :classes="'mr-2 align-middle h-8 w-8'" />
                              <div class="text-2xl font-bold flex-grow" data-cy="name">
                                <router-link :to="`/report/${r.id}`"
                                  ><a>
                                    <span>{{ r.name }}</span>
                                  </a></router-link
                                >
                              </div>
                              <div class="m-2 align-middle">Updated {{ formatDate(r.modified_at_ms) }}</div>
                              <DownloadButton
                                class="btn btn-ghost btn-border-base-200 removedInExport"
                                @click.stop.prevent="queueNestedDownload($refs[`report-${idx}`][0], r.name, idx)"
                              />
                              <button
                                class="ml-2 btn btn-outline hover:btn-error removedInExport"
                                role="button"
                                data-cy="remove"
                                @click.stop.prevent="removeReport(r)"
                              >
                                <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-4 w-4 align-middle mr-2" />
                                Remove
                              </button>
                              <OxScoreBox
                                :ox-score="Number(r.ox_score)"
                                :has-skipped="r?.has_skipped"
                                data-cy="average-ox-score"
                                class="ml-4"
                              />
                            </div>
                            <AnalyticsPanel
                              :ref="`report-${idx}-panel`"
                              :report="r"
                              :scorecards-by-framework="getScorecardsForReport(r)"
                              :start-open="false"
                              :toggle-bar="true"
                              :hide-confidence="true"
                              :allow-group-by-report="false"
                              :embedded="true"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                    <div v-if="reports?.length == 0">
                      <div class="card card-bordered bg-base-200 max-w-screen-md ml-4">
                        <div class="card-body w-full">
                          <div class="flex">
                            <div class="w-12 text-center">
                              <OxObjectIcon :type="'report'" :greyscale="true" :classes="'h-12 w-12 text-base-500'" />
                            </div>
                            <div class="grow text-left px-4 pt-2 flex justify-between">
                              <div class="text-xl text-base-500">No reports yet.</div>
                              <label
                                v-if="canEdit"
                                data-cy="add-report-to-stack"
                                role="button"
                                class="btn btn-primary"
                                for="add-report-modal"
                              >
                                <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                                Add Report
                              </label>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </TabPanel>
                <TabPanel>
                  <NotesPanel :target="stack" />
                </TabPanel>
                <TabPanel>
                  <DiscussionPanel :target="stack" />
                </TabPanel>
                <TabPanel>
                  <PermissionsPanel :target="stack" :can-manage="canManage" @permissions-updated="permissionsUpdated" />
                </TabPanel>
              </TabPanels>
            </TabGroup>
          </div>
        </div>
      </div>
      <ConfirmDelete
        :open="showConfirmDelete"
        :message="confirmDeleteMsg"
        @close="closeConfirmDelete"
        @confirm="deleteStack"
      />
      <input id="add-report-modal" type="checkbox" class="modal-toggle" />
      <div class="modal" data-cy="add-report-modal">
        <div class="modal-box relative">
          <div class="relative">
            <label for="add-report-modal" class="btn btn-sm btn-circle absolute right-0 top-0">
              <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle fa-swap-opacity" />
            </label>
          </div>
          <h3 class="text-2xl font-bold">
            <OxObjectIcon :type="'report'" :classes="'mr-2 align-middle'" />

            Add Report to Stack
          </h3>
          <p class="py-4">Which report would you like to add to this stack?</p>
          <OxSearchBox
            :options="writeableReports"
            :exclude="reports"
            :placeholder="'Search for a report...'"
            @selected-choice="setAddReport"
          />
          <div class="flex justify-end">
            <div
              role="button"
              data-cy="add-report-to-stack-from-modal"
              class="mt-4 btn btn-primary"
              :class="newReport && !addingReport ? '' : 'btn-disabled'"
              @click="addReport()"
            >
              {{ addingReport ? "Adding..." : "Add Report" }}
            </div>
          </div>
        </div>
      </div>
      <DownloadPDFModal :target="stack" :download-type="'Stack'" :is-open="downloadModalOpen" @close="closeDownload" />
    </main>
    <OxOwnerFooter :object="stack" />
  </DefaultLayout>
</template>

<script>
/**
 * TODO: Replace hardcoded  links
 *
 */
import "regenerator-runtime/runtime";
import DefaultLayout from "../layouts/DefaultLayout.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faUnlock } from "@fortawesome/pro-duotone-svg-icons/faUnlock";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faFileCsv } from "@fortawesome/pro-duotone-svg-icons/faFileCsv";
import { faFilePdf } from "@fortawesome/pro-duotone-svg-icons/faFilePdf";
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faLayerGroup } from "@fortawesome/pro-duotone-svg-icons/faLayerGroup";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faMemoPad } from "@fortawesome/pro-duotone-svg-icons/faMemoPad";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faLinkHorizontal } from "@fortawesome/pro-duotone-svg-icons/faLinkHorizontal";
library.add(
  faUnlock,
  faTrashCan,
  faFilePdf,
  faFileCsv,
  faClone,
  faPen,
  faFileLines,
  faLayerGroup,
  faChartSimpleHorizontal,
  faCompass,
  faMessages,
  faFiles,
  faMemoPad,
  faXmark,
  faLinkHorizontal
);

import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import { ref, nextTick } from "vue";
import { useAurochsData } from "../stores/aurochs";
import OxTags from "../components/common/OxTags.vue";
import OxScoreBox from "../components/common/OxScoreBox.vue";
import OxSearchBox from "../components/common/OxSearchBox.vue";
import OxObjectIcon from "../components/common/icons/OxObjectIcon.vue";
import OxOwnerFooter from "../components/common/OxOwnerFooter.vue";
import { checkCanEdit, checkCanManage, checkCanView, checkCanSee } from "../mixins/permissions.js";
import { getReportScorecardsByFramework, getStackScorecardsByFramework } from "../mixins/format_scorecards.js";
import ConfirmDelete from "../components/common/ConfirmDelete";
import PermissionsPanel from "../components/common/PermissionsPanel.vue";
import formatDate from "../mixins/format_date";
import DiscussionPanel from "../components/common/DiscussionPanel.vue";
import NotesPanel from "../components/common/NotesPanel.vue";
import AnalyticsPanel from "../components/reports/AnalyticsPanel.vue";
import DownloadButton from "../components/common/DownloadButton.vue";
import downloadArea from "../mixins/download_area";
import DownloadMixin from "../mixins/download_file";
import DownloadPDFModal from "../components/common/DownloadPDFModal.vue";

export default {
  components: {
    DefaultLayout,
    ConfirmDelete,
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    DiscussionPanel,
    NotesPanel,
    AnalyticsPanel,
    PermissionsPanel,
    OxTags,
    OxScoreBox,
    OxSearchBox,
    OxOwnerFooter,
    OxObjectIcon,
    FontAwesomeIcon,
    DownloadButton,
    DownloadPDFModal,
  },
  mixins: [formatDate, downloadArea, DownloadMixin],
  props: {
    id: {
      type: String,
      required: true,
    },
    new: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const showCreateModal = ref(false);
    const permissionsModalOpen = ref(false);
    const expanded = ref(false);
    const showConfirmDelete = ref(false);
    const showEditStack = ref(false);
    const saving = ref(false);
    const addingReport = ref(false);
    const newReport = ref(false);
    const tabs = [
      {
        name: "Overview",
        hash: "overview",
        class: "mr-2",
        icon: ["fad", "chart-simple-horizontal"],
      },
      {
        name: "Frameworks",
        hash: "frameworks",
        class: "mr-2",
        icon: ["fad", ""],
        frameworkIcon: true,
      },
      {
        name: "Reports",
        hash: "reports",
        class: "mr-2",
        icon: ["fad", "file-lines"],
      },
      {
        name: "Notes",
        hash: "notes",
        class: "mr-2",
        // icon: ["fad", "memo"],
        // icon: ["fad", "note"],
        // icon: ["fad", "notes"],
        icon: ["fad", "memo-pad"],
      },
      {
        name: "Discussion",
        hash: "discussion",
        class: "mr-2",
        icon: ["fad", "messages"],
      }, // badge: 2
      {
        name: "Permissions",
        hash: "permissions",
        class: "mr-2",
        icon: ["fad", "lock"],
      },
    ];

    const is_new = ref(props.new);
    const stackId = ref(props.id);
    const editing = ref(props.new);
    const selectedTab = ref(0);
    const formData = {};
    const downloadModalOpen = ref(false);
    // const stack = ref({})

    return {
      tabs,
      aurochsData: useAurochsData(),
      expanded,
      showCreateModal,
      permissionsModalOpen,
      showConfirmDelete,
      showEditStack,
      editing,
      saving,
      addingReport,
      newReport,
      stackId,
      is_new,
      selectedTab,
      formData: ref(formData),
      downloadModalOpen,
    };
  },
  computed: {
    stack() {
      if (this.aurochsData.stacks && this.id && String(this.id)) {
        return this.aurochsData.stacks[String(this.id)];
      }
      return null;
    },
    canEdit() {
      return checkCanEdit(this.stack, this.aurochsData.user);
    },
    canManage() {
      return checkCanManage(this.stack, this.aurochsData.user);
    },
    canView() {
      return checkCanView(this.stack, this.aurochsData.user);
    },
    canSee() {
      return checkCanSee(this.stack, this.aurochsData.user);
    },
    admin_list() {
      let admin_str = "";
      if (this.stack) {
        for (let p_id in this.stack.permissions) {
          if (this.stack.permissions[p_id].substring(3, 4) == "1") {
            admin_str += this.aurochsData.users[p_id.substring(2)].full_name + ", ";
          }
        }
        if (admin_str.length > 2) {
          admin_str = admin_str.slice(0, -2);
        }
      }
      return admin_str;
    },
    dataByFramework() {
      return getStackScorecardsByFramework(this.stack);
      // console.log(d);
      // return d;
    },
    writeableReports() {
      let report_list = [];
      for (let i in this.aurochsData.reports) {
        if (checkCanEdit(this.aurochsData.reports[i], this.aurochsData.user)) {
          report_list.push(this.aurochsData.reports[i]);
        }
      }
      return report_list;
    },
    confirmDeleteMsg() {
      return `Are you sure you want to delete the stack ${this.stack?.name}?`;
    },
    createdBy() {
      if (this.stack) {
        return this.stack?.created_by;
      }
      return null;
    },
    reports() {
      if (this.stack && this.stack.reports?.length > 0) {
        // let sortedReports = [...this.stack.reports];
        return this.stack.reports.slice().sort((a, b) => {
          return b.ox_score - a.ox_score;
        });
      }
      return [];
    },
    average_ox_score() {
      let total = 0;
      let num = 0;
      for (var r in this.reports) {
        total += Number(this.reports[r].ox_score);
        num += 1;
      }
      if (num == 0) {
        return false;
      }
      return Math.round(total / num);
    },
    max_ox_score() {
      if (this.reports.length > 0) {
        return this.reports[0].ox_score;
      }
      return 1;
    },
  },
  watch: {
    id: {
      handler: function (newVal) {
        this.stackId = newVal;
        document.title = this.aurochsData.stacks[String(newVal)].name;
        this.is_new = this.$route.query.new == "true";
        this.editing = this.$route.query.new == "true";
      },
    },
    new: {
      handler: function (newVal) {
        this.is_new = newVal || newVal == "true" ? true : false;
        if (this.is_new) {
          this.editing = true;
        }
      },
    },
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
    // this.stack = this.aurochsData.stacks[String(this.stackId)];
    document.title = this.stack?.name || "Ox Stack";
    if (this.$route.query.new) {
      this.editing = true;
    }
    if (this.is_new) {
      this.formData = {
        name: "New Stack",
        subtitle: "",
      };
    }
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
    // this.getNotes();
  },
  created() {},
  methods: {
    getScorecardsForReport(report) {
      return getReportScorecardsByFramework(report);
    },
    confirmDeleteStack() {
      this.showConfirmDelete = true;
    },
    closeConfirmDelete() {
      this.showConfirmDelete = false;
    },
    openPermissions() {
      this.$router.push(`/stack/${this.stack.id}/#permissions`);
    },
    permissionsUpdated() {},
    startEditing() {
      this.formData = {
        name: this.stack?.name || "",
        subtitle: this.stack?.subtitle || "",
      };

      this.editing = true;
    },
    stopEditing() {
      this.editing = false;
    },
    cancel() {
      this.stopEditing();
      this.formData = {
        name: this.stack?.name,
        subtitle: this.stack?.subtitle,
      };
    },
    async saveStack() {
      this.saving = true;
      const data = {
        id: this.stack.id,
        name: this.formData.name,
        subtitle: this.formData.subtitle,
      };
      await this.$sendEvent("update_stack", data);
      this.saving = false;
      this.stopEditing();
    },
    async deleteStack() {
      this.deleting = true;
      if (confirm("Are you sure you want to delete this stack?")) {
        var data = {
          id: this.stack.id,
        };
        await this.$sendEvent("delete_stack", data);
        this.$router.push("/library");
      }
      this.deleting = false;
    },
    setAddReport(report) {
      this.newReport = report;
    },
    async addReport() {
      this.addingReport = true;
      var data = {
        report_id: this.newReport.id,
        stack_id: this.stack.id,
      };
      await this.$sendEvent("add_report_to_stack", data);
      this.addingReport = false;
      this.emitter.emit("clearSearchBox", { previousSelected: this.newReport });
      this.newStack = false;
      document.getElementById("add-report-modal").checked = false;
    },
    async removeReport(r) {
      if (window.confirm("Are you sure you want remove this report from the stack?")) {
        var data = {
          report_id: r.id,
          stack_id: this.stack.id,
        };
        await this.$sendEvent("remove_report_from_stack", data);
      }
      return false;
    },
    changeTab(tab) {
      this.$router.push(`/stack/${this.stack.id}/#${this.tabs[tab].hash}`);
    },
    slugify(name) {
      return name.toLowerCase().replaceAll(" ", "_").replaceAll('"', "'");
    },
    async queueDownload(scorecard, name) {
      var wasOpen = this.open;
      this.open = true;
      await nextTick();
      var ctx = this;
      this.downloadArea(scorecard, name).then(function () {
        ctx.open = wasOpen;
      });
    },
    async queueNestedDownload(scorecard, name, idx) {
      var wasOpen = this.open;
      this.open = true;
      this.$refs[`report-${idx}-panel`][0].setOpen(true);
      await nextTick();
      var ctx = this;
      this.downloadArea(scorecard, name).then(function () {
        ctx.open = wasOpen;
        ctx.$refs[`report-${idx}-panel`][0].resetOpen();
      });
    },
    openDownload() {
      this.downloadModalOpen = true;
      document.getElementById("download-modal").checked = true;
    },
    closeDownload() {
      this.downloadModalOpen = false;
      document.getElementById("download-modal").checked = false;
    },
    downloadCSV() {
      var now = new Date();
      this.downloadFile(
        "/export/stack/csv/" + this.id,
        this.stack?.name.replace(" ", "_").replace('"', "'") + "-" + now.toISOString(),
        ".csv"
      );
    },
  },
};
</script>

<style scoped>
html {
  @apply h-full;
}

body {
  @apply h-full;
}
.left-bar {
  @apply h-full w-4 absolute;
}

.ox-stack-nav {
  @apply inline-flex items-center px-3 py-2 border border-transparent hover:shadow-sm text-lg leading-4  focus:outline-none;
}

.stack-action-icon {
  @apply h-4 w-4 mr-1;
}

.reports-btn {
  @apply text-white bg-sky-600 hover:bg-sky-700;
}

.discussion-btn {
  @apply text-white bg-indigo-600 hover:bg-indigo-700;
}
</style>
