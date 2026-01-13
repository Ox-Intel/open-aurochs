<template>
  <DefaultLayout class="">
    <div v-if="!source || !canSee">
      <div class="w-full min-h-[75vh]">
        <div class="card w-full bg-base-200 card-bordered mt-32 mx-auto max-w-screen-md" data-cy="not-found">
          <div v-if="!source" class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <OxObjectIcon :type="'source'" :classes="'h-12 w-12'" :greyscale="true" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Source not found.</div>
                <div class="text-xl text-dark-grey">
                  This source either doesn't exist, or you don't have permissions to view it.
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
                <div class="text-2xl w-full font-bold">Source is private.</div>
                <div class="text-xl text-dark-grey">
                  You don't have permissions to view this source. If you think this is incorrect, please contact an
                  administrator: {{ admin_list }}.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <main v-if="source && canSee" class="" data-cy="source">
      <div class="w-full">
        <!-- Main Space -->
        <div class="w-full min-h-[75vh]">
          <div class="w-full">
            <div class="w-full">
              <div class="w-full">
                <article class="prose max-w-none w-full">
                  <div class="flex flex-nowrap mb-4 w-full gap-2 lg:flex-nowrap flex-wrap">
                    <OxObjectIcon
                      :type="'source'"
                      :classes="(source?.subtitle || editing ? 'w-12 h-12' : 'w-12 h-12') + ' mr-2 align-middle'"
                    />
                    <div class="block grow">
                      <h1 class="py-0 my-0">
                        <div v-if="!editing" data-cy="name" :class="source?.subtitle ? 'mt-0.5' : 'mt-1'">
                          {{ source?.name }}
                        </div>
                        <div v-if="editing" class="w-full max-w-[70vw]">
                          <input
                            v-model="formData.name"
                            data-cy="input-source-name"
                            placeholder="source Title"
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
                          data-cy="input-source-subtitle"
                          type="text"
                          placeholder="Source subtitle..."
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
                        {{ source?.subtitle }}
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
                        @click="saveSource"
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
                      <button
                        v-if="canEdit"
                        data-cy="edit"
                        type="button"
                        role="button"
                        title="Edit Source"
                        class="btn btn-outline btn-primary"
                        @click="startEditing"
                      >
                        <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2 align-middle" />
                        Edit
                      </button>
                      <!--                         <button
                        data-cy="open-permissions"
                        type="button"
                        role="button"
                        title="Permissions"
                        class="btn btn-outline btn-primary "
                        @click="openPermissions"
                      >
                        <FontAwesomeIcon :icon="['fad', 'unlock']" class="mr-2 align-middle" />
                        Permissions
                      </button> -->
                      <button
                        v-if="canManage"
                        type="button"
                        role="button"
                        data-cy="delete"
                        title="Delete Source"
                        class="btn btn-outline btn-error"
                        :class="deleting ? 'disabled btn-disabled' : ''"
                        :disabled="deleting"
                        @click="deleteSource"
                      >
                        <FontAwesomeIcon :icon="['fad', 'trash-can']" class="mr-2 align-middle" />
                        Delete
                      </button>
                    </template>
                  </div>
                  <OxTags v-if="!editing" :target="source" :can-edit="canEdit" />
                </article>
              </div>
            </div>
          </div>
          <div class="mt-2 pb-8">
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
                    <FontAwesomeIcon :icon="tab.icon" :class="tab.class" class="mr-2 align-middle" />
                    <span>{{ tab.name }}</span>
                  </div>
                </Tab>
              </TabList>
              <TabPanels class="mt-8">
                <TabPanel>
                  <NotesPanel :target="source" />
                </TabPanel>
                <TabPanel>
                  <div class="max-w-screen-lg" data-cy="report-list">
                    <div v-for="(r, idx) in reports" :key="idx">
                      <router-link :to="`/report/${r.id}`"
                        ><a>
                          <div class="card w-full bg-base-100 card-bordered shadow-md" role="button">
                            <div class="card-body w-full">
                              <div class="flex">
                                <div class="w-12 text-center">
                                  <OxObjectIcon :type="'report'" :classes="'h-12 w-12 mr-2 align-middle'" />
                                </div>
                                <div class="grow text-left px-4">
                                  <div class="text-xl font-bold" data-cy="name">
                                    {{ r.name }}
                                  </div>
                                  <div class="text-linebreaks">
                                    {{ r.subtitle }}
                                  </div>
                                  <div class="font-light mt-4">Updated {{ formatDate(r.modified_at_ms) }}</div>
                                </div>
                                <div class="w-12">
                                  <OxScoreBox :ox-score="Number(r.ox_score)" :has-skipped="r.has_skipped" />
                                </div>
                                <div class="w-12 ml-6">
                                  <div
                                    class="btn btn-circle btn-ghost hover:btn-error"
                                    role="button"
                                    @click.stop.prevent="removeReport(r)"
                                  >
                                    <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-6 w-6 align-middle" />
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div> </a
                      ></router-link>
                    </div>
                  </div>
                  <div v-if="reports.length == 0" class="card w-full bg-base-200 card-bordered max-w-screen-lg">
                    <div class="card-body w-full">
                      <div class="flex">
                        <FontAwesomeIcon
                          :icon="['fad', 'file-lines']"
                          class="h-12 w-12 mr-2 align-middle text-medium-grey"
                        />
                        <div class="grow text-left px-4 pt-2 flex justify-between">
                          <div class="text-xl text-medium-grey">Not added to any reports.</div>
                          <label for="add-report-modal" class="btn btn-primary -mt-2" role="button">
                            <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                            Add to Report
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="reports.length > 0" class="pt-8">
                    <label for="add-report-modal" class="btn btn-primary -mt-2" role="button">
                      <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                      Add to Report
                    </label>
                  </div>
                </TabPanel>
                <TabPanel>
                  <DiscussionPanel :target="source" />
                </TabPanel>
                <TabPanel>
                  <PermissionsPanel
                    :target="source"
                    :can-manage="canManage"
                    @permissions-updated="permissionsUpdated"
                  />
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
        @confirm="deleteSource"
      />
      <input id="add-report-modal" type="checkbox" class="modal-toggle" />
      <div class="modal">
        <div class="modal-box relative">
          <div class="relative">
            <label for="add-report-modal" class="btn btn-sm btn-circle absolute right-0 top-0">
              <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle fa-swap-opacity" />
            </label>
          </div>
          <h3 class="text-2xl font-bold">
            <OxObjectIcon :type="'report'" :classes="'mr-2 align-middle'" />

            Add Source to Report
          </h3>
          <p class="py-4">Which report would you like to add this source to?</p>
          <OxSearchBox
            :options="writeableReports"
            :exclude="reports"
            :placeholder="'Search for a report...'"
            @selected-choice="setAddReport"
          />
          <div class="flex justify-end">
            <div
              role="button"
              class="mt-4 btn btn-primary"
              :class="newReport && !addingReport ? '' : 'btn-disabled'"
              @click="addReport()"
            >
              {{ addingReport ? "Adding..." : "Add to Report" }}
            </div>
          </div>
        </div>
      </div>
    </main>
    <OxOwnerFooter :object="source" />
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
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faMemoPad } from "@fortawesome/pro-duotone-svg-icons/faMemoPad";
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
  faMemoPad,
  faLinkHorizontal
);

import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import { ref } from "vue";
import OxTags from "../components/common/OxTags.vue";
import OxScoreBox from "../components/common/OxScoreBox.vue";
import OxSearchBox from "../components/common/OxSearchBox.vue";
import OxObjectIcon from "../components/common/icons/OxObjectIcon.vue";
import OxOwnerFooter from "../components/common/OxOwnerFooter.vue";
import { useAurochsData } from "../stores/aurochs";
import { checkCanEdit, checkCanManage, checkCanSee } from "../mixins/permissions.js";
import DownloadMixins from "../mixins/download_file";
import ConfirmDelete from "../components/common/ConfirmDelete";
import PermissionsPanel from "../components/common/PermissionsPanel.vue";
import formatDate from "../mixins/format_date";
import DiscussionPanel from "../components/common/DiscussionPanel.vue";
import NotesPanel from "../components/common/NotesPanel.vue";

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
    PermissionsPanel,
    OxTags,
    OxScoreBox,
    OxSearchBox,
    OxObjectIcon,
    OxOwnerFooter,
    FontAwesomeIcon,
  },
  mixins: [DownloadMixins, formatDate],
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
    const showEditSource = ref(false);
    const saving = ref(false);
    const deleting = ref(false);
    const addingReport = ref(false);
    const newReport = ref(false);
    const tabs = [
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
        name: "Reports",
        hash: "reports",
        class: "mr-2",
        icon: ["fad", "file-lines"],
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
    const sourceId = ref(props.id);
    const editing = ref(props.new);
    const selectedTab = ref(0);
    const formData = {};

    return {
      tabs,
      aurochsData: useAurochsData(),
      expanded,
      showCreateModal,
      permissionsModalOpen,
      showConfirmDelete,
      showEditSource,
      editing,
      saving,
      deleting,
      addingReport,
      newReport,
      sourceId,
      is_new,
      selectedTab,
      formData: ref(formData),
    };
  },
  computed: {
    source() {
      if (this.aurochsData.sources && this.id && String(this.id)) {
        return this.aurochsData.sources[String(this.id)];
      }
      return null;
    },
    canEdit() {
      return checkCanEdit(this.source, this.aurochsData.user);
    },
    canManage() {
      return checkCanManage(this.source, this.aurochsData.user);
    },
    canSee() {
      return checkCanSee(this.source, this.aurochsData.user);
    },
    admin_list() {
      let admin_str = "";
      if (this.source) {
        for (let p_id in this.source.permissions) {
          if (this.source.permissions[p_id].substring(3, 4) == "1") {
            admin_str += this.aurochsData.users[p_id.substring(2)].full_name + ", ";
          }
        }
        if (admin_str.length > 2) {
          admin_str = admin_str.slice(0, -2);
        }
      }
      return admin_str;
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
      return `Are you sure you want to delete the source ${this.source?.name}?`;
    },
    createdBy() {
      if (this.source) {
        return this.source?.created_by;
      }
      return null;
    },
    reports() {
      var report_list = [];
      for (var i in this.source?.report_id_list) {
        report_list.push(this.aurochsData.reports[String(this.source?.report_id_list[i])]);
      }
      return report_list;
    },
  },
  watch: {
    id: {
      handler: function (newVal) {
        this.sourceId = newVal;
        document.title = this.aurochsData.sources[String(newVal)].name;
        this.canEdit = checkCanEdit(this.source, this.aurochsData.user);
        this.canManage = checkCanManage(this.source, this.aurochsData.user);
        this.is_new = this.$route.query.new == "true";
        this.editing = this.$route.query.new == "true";
        this.formData = {
          name: this.source?.name || "",
          subtitle: this.source?.subtitle || "",
        };
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
    document.title = this.source?.name || "Ox Source";
    this.formData = {
      name: this.source?.name || "",
      subtitle: this.source?.subtitle || "",
    };
    if (this.$route.query.new) {
      this.editing = true;
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
  },
  created() {},
  methods: {
    confirmDeleteSource() {
      this.showConfirmDelete = true;
    },
    closeConfirmDelete() {
      this.showConfirmDelete = false;
    },
    openPermissions() {
      this.$router.push(`/source/${this.source.id}/#permissions`);
    },
    permissionsUpdated() {
      this.canEdit = checkCanEdit(this.source, this.aurochsData.user);
      this.canManage = checkCanManage(this.source, this.aurochsData.user);
    },
    startEditing() {
      this.editing = true;
    },
    stopEditing() {
      this.editing = false;
    },
    cancel() {
      this.stopEditing();
      this.formData = {
        name: this.source?.name,
        subtitle: this.source?.subtitle,
      };
    },
    async saveSource() {
      this.saving = true;
      const data = {
        id: this.source.id,
        name: this.formData.name,
        subtitle: this.formData.subtitle,
      };
      await this.$sendEvent("update_source", data);
      this.saving = false;
      this.stopEditing();
    },
    async deleteSource() {
      this.deleting = true;
      if (confirm("Are you sure you want to delete this source?")) {
        var data = {
          id: this.source.id,
        };
        await this.$sendEvent("delete_source", data);
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
        source_id: this.source.id,
      };
      await this.$sendEvent("add_source_to_report", data);
      this.addingReport = false;
      this.emitter.emit("clearSearchBox", { previousSelected: this.newReport });
      this.newSource = false;
      document.getElementById("add-report-modal").checked = false;
    },
    async removeReport(r) {
      if (window.confirm("Are you sure you want remove this source from the report?")) {
        var data = {
          report_id: r.id,
          source_id: this.source.id,
        };
        await this.$sendEvent("remove_source_from_report", data);
      }
      return false;
    },
    changeTab(tab) {
      this.$router.push(`/source/${this.source.id}/#${this.tabs[tab].hash}`);
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

.ox-source-nav {
  @apply inline-flex items-center px-3 py-2 border border-transparent hover:shadow-sm text-lg leading-4  focus:outline-none;
}

.source-action-icon {
  @apply h-4 w-4 mr-1;
}

.reports-btn {
  @apply text-white bg-sky-600 hover:bg-sky-700;
}

.discussion-btn {
  @apply text-white bg-indigo-600 hover:bg-indigo-700;
}
</style>
