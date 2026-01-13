<template>
  <DefaultLayout>
    <div class="h-full mt-4 mx-4" data-cy="dashboard">
      <!-- <div class="text-2xl font-bold">Recently Used</div> -->
      <div class="w-full mb-8">
        <div class="text-2xl font-bold flex mb-4 relative">
          <div class="absolute mb-1 align-middle h-8 w-8 mt-1"><OxObjectIcon :type="'framework'" /></div>
          <div class="ml-12 mt-1" data-cy="framework-title">
            Frameworks
            <span v-if="sortedFrameworks.length > 1" class="text-medium-grey font-normal text-2xl ml-2"
              >({{ sortedFrameworks.length }} total)</span
            >
          </div>
        </div>
        <div
          data-cy="frameworks"
          class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 w-full shadow-inner bg-base-200 rounded-xl p-8"
        >
          <template v-if="pinnedFramework">
            <OxObjectCard
              :on-dashboard="true"
              :object="pinnedFramework"
              :big="true"
              :allow-pins="true"
              :pinned="true"
              :index="0"
            />
          </template>
          <template v-for="(obj, key) in recentFrameworks" :key="key">
            <OxObjectCard
              :on-dashboard="true"
              :object="obj"
              :big="key == 0 && !pinnedFramework"
              :allow-pins="true"
              :pinned="false"
              :index="key"
            />
          </template>
          <div
            class="h-48 card shadow-md bg-base-300 cursor-pointer border-base-300 hover:border-framework text-medium-grey hover:text-framework border-2"
            data-cy="new-framework"
            @click="createBlankFramework"
          >
            <div class="card-body p-4 text-center place-content-center place-items-center">
              <FontAwesomeIcon :icon="['fad', 'plus']" class="h-12 w-12" />
              <div class="mt-2 text-2xl font-bold">New Framework</div>
            </div>
          </div>
        </div>
      </div>
      <div class="w-full mb-8">
        <div class="text-2xl font-bold flex align-middle mb-4 mt-10">
          <OxObjectIcon :type="'report'" :classes="'h-8 w-8 mr-2 mb-0 align-middle'" />
          Reports
          <span v-if="sortedReports.length > 1" class="text-medium-grey font-normal text-2xl ml-2"
            >({{ sortedReports.length }} total)</span
          >
        </div>
        <div
          data-cy="reports"
          class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-8 w-full shadow-inner bg-base-200 rounded-xl p-8"
        >
          <template v-if="pinnedReport">
            <OxObjectCard
              :on-dashboard="true"
              :object="pinnedReport"
              :big="true"
              :allow-pins="true"
              :pinned="true"
              :index="0"
            />
          </template>
          <template v-for="(obj, key) in recentReports" :key="key">
            <OxObjectCard
              :on-dashboard="true"
              :object="obj"
              :big="key == 0 && !pinnedReport"
              :allow-pins="true"
              :pinned="false"
              :index="key"
            />
          </template>
          <div
            class="h-48 card shadow-md bg-base-300 cursor-pointer border-base-300 hover:border-report text-medium-grey hover:text-report border-2"
            data-cy="new-report"
            @click="createBlankReport"
          >
            <div class="card-body p-4 text-center place-content-center place-items-center">
              <FontAwesomeIcon :icon="['fad', 'plus']" class="h-12 w-12" />
              <div class="mt-2 text-2xl font-bold">New Report</div>
            </div>
          </div>
        </div>
      </div>
      <div class="w-full mb-16 pb-12">
        <div class="text-2xl font-bold flex align-middle mb-4 mt-10">
          <OxObjectIcon :type="'stack'" :classes="'h-8 w-8 mr-2 mb-0 align-middle'" />
          Stacks
          <span v-if="sortedStacks.length > 1" class="text-medium-grey font-normal text-2xl ml-2"
            >({{ sortedStacks.length }} total)</span
          >
        </div>
        <div
          data-cy="stacks"
          class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-8 w-full shadow-inner bg-base-200 rounded-xl p-8"
        >
          <template v-if="pinnedStack">
            <OxObjectCard
              :on-dashboard="true"
              :object="pinnedStack"
              :big="true"
              :allow-pins="true"
              :pinned="true"
              :index="0"
            />
          </template>
          <template v-for="(obj, key) in recentStacks" :key="key">
            <OxObjectCard
              :on-dashboard="true"
              :object="obj"
              :big="key == 0 && !pinnedStack"
              :allow-pins="true"
              :pinned="false"
              :index="key"
            />
          </template>
          <div
            class="h-48 card shadow-md bg-base-300 cursor-pointer border-base-300 hover:border-stack text-medium-grey hover:text-stack border-2"
            data-cy="new-stack"
            @click="createBlankStack"
          >
            <div class="card-body p-4 text-center place-content-center place-items-center">
              <FontAwesomeIcon :icon="['fad', 'plus']" class="h-12 w-12" />
              <div class="mt-2 text-2xl font-bold">New Stack</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "../layouts/DefaultLayout.vue";
import OxObjectIcon from "../components/common/icons/OxObjectIcon.vue";
import OxObjectCard from "../components/common/OxObjectCard";
import { useAurochsData } from "../stores/aurochs";
import { checkCanSee } from "../mixins/permissions.js";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";

library.add(faGlobe, faPlus, faUsers);

export default {
  components: {
    DefaultLayout,
    OxObjectCard,
    OxObjectIcon,
    FontAwesomeIcon,
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    sortedReports() {
      if (!this.aurochsData?.reports) {
        return [];
      }
      let all_act = Object.values(this.aurochsData?.reports);
      let act = [];
      for (let a of all_act) {
        if (checkCanSee(a, this.aurochsData.user)) {
          act.push(a);
        }
      }

      return act.sort((a, b) => {
        return b?.modified_at_ms - a?.modified_at_ms;
      });
    },
    sortedFrameworks() {
      if (!this.aurochsData?.frameworks) {
        return [];
      }
      let all_act = Object.values(this.aurochsData?.frameworks);
      let act = [];
      for (let a of all_act) {
        if (checkCanSee(a, this.aurochsData.user)) {
          act.push(a);
        }
      }
      return act.sort((a, b) => {
        return b?.modified_at_ms - a?.modified_at_ms;
      });
    },
    sortedStacks() {
      if (!this.aurochsData?.stacks) {
        return [];
      }
      let all_act = Object.values(this.aurochsData?.stacks);
      let act = [];
      for (let a of all_act) {
        if (checkCanSee(a, this.aurochsData.user)) {
          act.push(a);
        }
      }
      return act.sort((a, b) => {
        return b?.modified_at_ms - a?.modified_at_ms;
      });
    },
    sortedSources() {
      if (!this.aurochsData?.sources) {
        return [];
      }
      let all_act = Object.values(this.aurochsData?.sources);
      let act = [];
      for (let a of all_act) {
        if (checkCanSee(a, this.aurochsData.user)) {
          act.push(a);
        }
      }
      return act.sort((a, b) => {
        return b?.modified_at_ms - a?.modified_at_ms;
      });
    },
    recentFrameworks() {
      let max_num = 8;
      if (this.pinnedFramework) {
        max_num -= 1;
      }
      let return_list = [];
      for (let o of this.sortedFrameworks) {
        if (!this.pinnedFramework || o.id != this.pinnedFramework.id) {
          return_list.push(o);
          if (return_list.length >= max_num) {
            break;
          }
        }
      }
      return return_list;
    },
    recentReports() {
      let max_num = 8;
      if (this.pinnedReport) {
        max_num -= 1;
      }
      let return_list = [];
      for (let o of this.sortedReports) {
        if (!this.pinnedReport || o.id != this.pinnedReport.id) {
          return_list.push(o);
          if (return_list.length >= max_num) {
            break;
          }
        }
      }
      return return_list;
    },
    recentStacks() {
      let max_num = 8;
      if (this.pinnedStack) {
        max_num -= 1;
      }
      let return_list = [];
      for (let o of this.sortedStacks) {
        if (!this.pinnedStack || o.id != this.pinnedStack.id) {
          return_list.push(o);
          if (return_list.length >= max_num) {
            break;
          }
        }
      }
      return return_list;
    },
    recentSources() {
      return this.sortedSources.slice(0, 8);
    },
    pinnedFramework() {
      let pk = this.aurochsData?.user?.pinned_framework_pk || false;
      if (pk) {
        return this.aurochsData.frameworks[pk];
      }
      return false;
    },
    pinnedReport() {
      let pk = this.aurochsData?.user?.pinned_report_pk || false;
      if (pk) {
        return this.aurochsData.reports[pk];
      }
      return false;
    },
    pinnedStack() {
      let pk = this.aurochsData?.user?.pinned_stack_pk || false;
      if (pk) {
        return this.aurochsData.stacks[pk];
      }
      return false;
    },
  },
  mounted() {
    document.title = "Ox Dashboard";
  },
  methods: {
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
  },
};
</script>

<style scoped>
.framework-description {
  @apply text-center text-base tracking-wide py-5 leading-5;
}

html {
  @apply h-full;
}

body {
  @apply h-full;
}
</style>
