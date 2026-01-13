<!-- eslint-disable vue/no-v-html -->
<template>
  <div
    :data-cy="`ox-object-${object.__type}-${pinned ? 'pinned' : index}`"
    class="card bg-base-100 shadow-md cursor-pointer border border-base-200 hover:border-dark-grey"
    :class="big ? 'col-span-2 row-span-2 h-auto' : 'h-48'"
  >
    <router-link :to="`/${object.__type}/${object.id}`"
      ><a>
        <div v-if="big" class="card-body w-full p-4 overflow-hidden h-96">
          <div class="flex space-x-3">
            <div
              v-if="allowPins"
              data-cy="pin"
              class="block absolute z-50 btn-sm btn-circle hover:bg-base-300 place-items-center place-content-center flex"
              :class="object?.__type == 'report' && oxScore ? 'right-12 top-4 mr-1' : 'right-2 top-2'"
              @click.stop.prevent="pinObject(object)"
            >
              <FontAwesomeIcon v-if="pinned" :icon="['fas', 'thumbtack']" class="h-4 w-4" />
              <FontAwesomeIcon v-if="!pinned" :icon="['far', 'thumbtack']" class="h-4 w-4 text-medium-grey" />
            </div>
            <div class="flex-shrink-0">
              <OxObjectIcon :target="object" :classes="'h-6 w-6'" :small="true" :scale="0.6" />
            </div>
            <div class="min-w-0 flex-grow">
              <p
                class="text-xl font-bold mr-8 mb-1 two-lines grow"
                data-cy="item-name"
                :class="object?.__type == 'report' && oxScore ? 'mr-16' : 'mr-8'"
              >
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span class="leading-none" v-html="highlighted(object.name)" />
              </p>
              <div
                v-for="(t, tag_idx) in collapsedTags"
                :key="tag_idx"
                class="inline-block mr-1 mb-1"
                @click.stop.prevent="searchForTag(t)"
              >
                <div
                  class="badge badge-sm badge-outline bg-base-300 border-base-300 hover:border-dark-grey gap-1 mb-1 text-xs select-none overflow-hidden whitespace-nowrap"
                >
                  <!-- eslint-disable-next-line vue/no-v-html -->
                  <span v-html="highlighted(t.name)" />
                </div>
              </div>
              <div v-if="object.__type == 'report' && stacks.length > 0">
                <div
                  v-for="(s, idx) in stacks"
                  :key="idx"
                  class="badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 mb-1 text-xs select-none overflow-hidden whitespace-nowrap"
                >
                  <router-link :to="`/stack/${s.id}`"
                    ><a>
                      <OxObjectIcon :type="'stack'" :classes="'h-3 w-3 mr-0.5 align-middle'" />
                      {{ s.name }}
                    </a></router-link
                  >
                </div>
              </div>
            </div>
          </div>
          <div class="w-full h-full">
            <template v-if="object.__type == 'framework'">
              <!--           <p
            v-if="object.subtitle"
            class="text-linebreaks text-sm text-ellipsis w-90 h-6 mx-8 -mt-1 mb-2  border-error block"
          >
            {{ truncatedFeatured(object.subtitle) }}
          </p> -->
              <div class="flex w-full h-full">
                <div class="w-1/2 justify-center mt-4 max-h-56 h-56 w-56">
                  <OxObjectIcon :target="object" :classes="'h-56 w-56'" />
                </div>
                <div class="w-1/2 mt-4 ml-4 max-h-56">
                  <ul v-for="(criteria, c_key) in object.criteria" :key="c_key">
                    <li v-if="c_key < 8" class="mb-1">
                      <div class="flex w-full relative">
                        <div
                          data-cy="weight"
                          class="font-bold leading-none rounded-full text-center text-xs w-6 h-6 mr-2 flex place-content-center place-items-center"
                          :style="`${getCriteriaColorStyle(criteria)}`"
                        >
                          <div class="w-6">
                            {{ Math.round(Number(criteria.weight)) }}
                          </div>
                        </div>
                        <div class="text-md truncate whitespace-nowrap w-auto" data-cy="name">
                          <!-- pr-2 hover:fixed hover:ml-8 hover:z-50 hover:bg-base-100 hover:rounded-md hover:overflow-visible  -->
                          {{ criteria.name }}
                        </div>
                      </div>
                    </li>
                    <li v-if="c_key == 8" class="mb-1">
                      <span
                        data-cy="weight"
                        class="font-bold leading-none rounded-full text-center text-xs pt-1.5 w-6 h-6 mr-2 inline-block bg-base-300"
                      >
                        <FontAwesomeIcon :icon="['fas', 'ellipsis']" class="" />
                      </span>
                      <span class="text-md" data-cy="name"> {{ object.criteria.length - 8 }} More Criteria </span>
                    </li>
                  </ul>
                  <div class="absolute bottom-4 left-10 flex flex-row flex-wrap">
                    <div class="flex flex-col mr-5">
                      <p class="text-xs text-medium-grey mt-1">
                        {{ byline }}
                      </p>
                      <!-- <p class="text-xs text-medium-grey">
                    {{ createdAt }}
                  </p> -->
                      <p class="text-xs text-medium-grey">
                        {{ updatedAt }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </template>
            <template v-if="object.__type == 'report'">
              <div class="h-full w-full">
                <div
                  v-if="oxScore && object.__type == 'report'"
                  class="block absolute right-2 top-2"
                  style="transform: scale(0.6); transform-origin: 0 0'"
                >
                  <!-- class="block absolute right-10 top-2" -->
                  <OxScoreBox :ox-score="oxScore" :has-skipped="hasSkipped" />
                </div>
                <p
                  v-if="!object?.scorecards.length"
                  class="w-full text-linebreaks text-sm my-2 mx-4 text-ellipsis w-full h-6 border-error block"
                >
                  {{ truncatedFeatured(object.subtitle) }}
                </p>

                <div
                  class="max-h-60 overflow-hidden text-clip"
                  :class="object?.scorecards.length ? 'ml-8 mr-4' : 'mx-4'"
                >
                  <AnalyticsPanel
                    :report="object"
                    :scorecards-by-framework="scorecardsByFramework(object)"
                    :graph-only="true"
                    :hide-confidence="true"
                    :hide-ox-score="true"
                    :hide-noise="true"
                    data-cy="overview-panel"
                  />
                </div>
                <div class="absolute bottom-4 left-10 flex flex-row flex-wrap">
                  <div class="flex flex-col mr-5">
                    <p class="text-xs text-medium-grey mt-1">
                      {{ byline }}
                    </p>
                    <!-- <p class="text-xs text-medium-grey">
                    {{ createdAt }}
                  </p> -->
                    <p class="text-xs text-medium-grey">
                      {{ updatedAt }}
                    </p>
                  </div>
                </div>
              </div>
            </template>
            <template v-if="object.__type == 'stack'">
              <div class="w-full pb-8">
                <p
                  v-if="object.subtitle"
                  class="text-linebreaks text-sm mt-2 mx-4 text-ellipsis w-full h-auto min-h-6 border-error block"
                >
                  {{ truncatedFeatured(object.subtitle) }}
                </p>
                <div class="max-h-64 overflow-hidden">
                  <div
                    v-for="(r, idx) in sortedReports(object)"
                    :key="idx"
                    class="w-full flex m-2 mx-4 h-8 place-content-center"
                  >
                    <template v-if="idx < 5">
                      <div class="w-1/4 text-sm font-bold h-16 pt-4" :title="r.name.length > 19 ? r.name : ''">
                        <div class="flex cursor-pointer">
                          <OxObjectIcon :type="'report'" :classes="'h-4 w-4 mr-1 '" />
                          <div class="text-ellipsis whitespace-nowrap truncate w-48">
                            {{ r.name }}
                          </div>
                        </div>
                      </div>
                      <div
                        class="mr-2 mt-2 w-12 h-9 box rounded border border-base-300 text-medium-grey text-center align-middle pt-0 pb-0.5 px-1 scale-90"
                      >
                        <div class="text-2xs mb-0">Scores</div>
                        <div class="text-sm font-bold -mt-1">
                          {{ r.scorecards.length }}
                        </div>
                      </div>
                      <div class="grow">
                        <div
                          :style="`width: ${r.ox_score}%;`"
                          class="bg-ox-score rounded-sm text-ox-score-content p-1 mt-2.5 text-md font-bold inline-block"
                        >
                          <span v-if="r.ox_score > 6">{{ r.ox_score }} %</span>
                          <span v-if="r.ox_score <= 6">&nbsp;</span>
                        </div>
                        <div v-if="r.ox_score <= 6" class="inline-block font-bold text-md py-4 px-2">
                          {{ r.ox_score }} %
                        </div>
                      </div>
                    </template>
                    <template v-if="idx == 5">
                      <div class="w-full text-sm h-16 pt-4">
                        <div class="flex cursor-pointer">
                          <OxObjectIcon :type="'report'" :classes="'h-4 w-4 mr-1 '" />
                          <div class="">and {{ sortedReports(object).length - 5 }} more reports.</div>
                        </div>
                      </div>
                    </template>
                  </div>
                </div>
                <div class="absolute bottom-4 left-10 flex flex-row flex-wrap">
                  <div class="flex flex-col mr-5">
                    <p class="text-xs text-medium-grey mt-1">
                      {{ byline }}
                    </p>
                    <!-- <p class="text-xs text-medium-grey">
                  {{ createdAt }}
                </p> -->
                    <p class="text-xs text-medium-grey">
                      {{ updatedAt }}
                    </p>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
        <div v-if="!big" class="card-body w-full p-4 pb-16 max-h-36 overflow-hidden">
          <div
            v-if="allowPins"
            data-cy="pin"
            class="block absolute z-50 btn-sm btn-circle hover:bg-base-300 place-items-center place-content-center flex"
            :class="object?.__type == 'report' && oxScore ? 'right-12 top-4 ' : 'right-2 top-2'"
            @click.stop.prevent="pinObject(object)"
          >
            <FontAwesomeIcon v-if="pinned" :icon="['fas', 'thumbtack']" class="h-4 w-4" />
            <FontAwesomeIcon
              v-if="!pinned"
              :icon="['far', 'thumbtack']"
              class="h-4 w-4 text-medium-grey text-medium-grey"
            />
          </div>
          <div
            v-if="oxScore && object?.__type == 'report'"
            class="block absolute right-2 top-2"
            style="transform: scale(0.6); transform-origin: 0 0'"
          >
            <OxScoreBox :ox-score="oxScore" :has-skipped="hasSkipped" />
          </div>
          <div class="flex space-x-3 -mb-1">
            <div class="flex-shrink-0">
              <OxObjectIcon :target="object" :classes="'h-6 w-6'" :small="true" :scale="0.6" />
            </div>
            <div class="min-w-0 flex-grow">
              <p
                class="text-xl font-bold mb-0 two-lines grow"
                data-cy="item-name"
                :class="object?.__type == 'report' && oxScore ? 'mr-16' : 'mr-8'"
              >
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span class="leading-none" v-html="highlighted(object.name)" />
              </p>
            </div>
          </div>
          <div class="flex mb-16 mx-1">
            <div class="min-w-0 flex-grow">
              <div v-if="collapsedTags?.length > 0" class="overflow-hidden h-6">
                <div
                  v-for="(t, tag_idx) in collapsedTags"
                  :key="tag_idx"
                  class="inline-block mr-1 mt-1"
                  @click.stop.prevent="searchForTag(t)"
                >
                  <div
                    class="badge badge-sm badge-outline bg-base-300 border-base-300 hover:border-dark-grey gap-1 mb-1 text-xs select-none overflow-hidden whitespace-nowrap"
                  >
                    <!-- eslint-disable-next-line vue/no-v-html -->
                    <span v-html="highlighted(t.name)" />
                  </div>
                </div>
              </div>
              <!-- <div>
            <div
              v-for="(t, team_idx) in objTeams"
              :key="team_idx"
              class="inline-block mr-1"
            >
              <div
                class="badge badge-lg badge-outline opacity-50 border-medium-grey gap-1 mb-1 text-sm select-none overflow-hidden whitespace-nowrap"
              >
                <FontAwesomeIcon
                  :icon="['fad', 'users']"
                  class="mr-1"
                />
                eslint-disable-next-line vue/no-v-html
                <span v-html="highlighted(t.name)" />
              </div>
            </div>
            <div
              v-for="(o, org_idx) in objOrganizations"
              :key="org_idx"
              class="inline-block mr-1"
            >
              <div
                class="badge badge-lg badge-outline opacity-50 border-medium-grey gap-1 mb-1 text-sm select-none overflow-hidden whitespace-nowrap"
              >
                <FontAwesomeIcon
                  :icon="['fad', 'globe']"
                  class="mr-1"
                />
                eslint-disable-next-line vue/no-v-html
                <span v-html="highlighted(o.name)" />
              </div>
            </div>
          </div> -->

              <div v-if="object.__type == 'report' && stacks.length > 0">
                <div
                  v-for="(s, idx) in stacks"
                  :key="idx"
                  class="badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 mb-1 text-xs select-none overflow-hidden whitespace-nowrap"
                >
                  <router-link :to="`/stack/${s.id}`"
                    ><a>
                      <OxObjectIcon :type="'stack'" :classes="'h-3 w-3 mr-0.5 align-middle'" />
                      {{ s.name }}
                    </a></router-link
                  >
                </div>
              </div>
              <p class="text-sm three-lines" :class="onDashboard ? ' mt-1 leading-tight' : ' mt-2 leading-snug'">
                <!-- eslint-disable-next-line vue/no-v-html -->
                <span v-if="object.subtitle" v-html="withLinebreaks(object.subtitle)" />
              </p>
            </div>
            <div class="absolute bottom-4 left-6 flex flex-row flex-wrap">
              <div class="flex flex-col mr-5">
                <p class="text-xs text-medium-grey mt-1">
                  {{ byline }}
                </p>
                <!-- <p class="text-xs text-medium-grey">
              {{ createdAt }}
            </p> -->
                <p class="text-xs text-medium-grey">
                  {{ updatedAt }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </a></router-link
    >
  </div>
</template>

<script>
import * as DOMPurify from "dompurify";

import OxObjectIcon from "./icons/OxObjectIcon.vue";
import OxScoreBox from "./OxScoreBox.vue";
import AnalyticsPanel from "../../components/reports/AnalyticsPanel.vue";
import { useAurochsData } from "../../stores/aurochs";
import chart_colors from "../../mixins/chart_color";
import formatDate from "../../mixins/format_date";
import { getReportScorecardsByFramework } from "../../mixins/format_scorecards";

// // Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import { faEllipsis } from "@fortawesome/pro-solid-svg-icons/faEllipsis";
import { faThumbtack as faThumbtackSolid } from "@fortawesome/pro-solid-svg-icons/faThumbtack";
import { faThumbtack as faThumbtackOutline } from "@fortawesome/pro-regular-svg-icons/faThumbtack";

library.add(faGlobe, faUsers, faEllipsis, faThumbtackSolid, faThumbtackOutline);

export default {
  components: {
    OxScoreBox,
    OxObjectIcon,
    AnalyticsPanel,
    FontAwesomeIcon,
  },
  mixins: [formatDate],
  props: {
    object: {
      type: Object,
      required: true,
      default: () => {},
    },
    tag: {
      type: String,
      default: () => "",
    },
    searchText: {
      type: String,
      default: () => "",
    },
    big: {
      type: Boolean,
      default: () => false,
    },
    allowPins: {
      type: Boolean,
      default: () => false,
    },
    pinned: {
      type: Boolean,
      default: () => false,
    },
    onDashboard: {
      type: Boolean,
      default: () => false,
    },
    index: {
      type: Number,
      default: () => 0,
    },
  },
  emits: ["set-featured"],
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    teams() {
      return this.aurochsData.teams;
    },
    organizations() {
      return this.aurochsData.organizations;
    },
    objOrganizations() {
      return this.object?.permissions?.administer?.organizations || [];
    },
    objTeams() {
      return this.object?.permissions?.administer?.teams || [];
    },
    stacks() {
      if (this.object.__type == "report" && this.object.stack_ids?.length > 0) {
        let stacks = [];
        for (let s_id of this.object.stack_ids) {
          stacks.push(this.aurochsData.stacks[s_id]);
        }
        return stacks;
      }
      return [];
    },
    tags() {
      if (this.object.tags?.length > 0) {
        let tags = [];
        for (let tag of this.object.tags) {
          tags.push(tag);
        }
        return tags;
      }
      return [];
    },
    collapsedTags() {
      let names = {};
      let tags = [];
      for (let t_index in this.object.tags) {
        if (this.object.tags[t_index].name in names) {
          // Skip this.
        } else {
          names[this.object.tags[t_index].name] = true;
          tags.push(this.object.tags[t_index]);
        }
      }
      return tags;
    },
    // orgs() {
    //   return this.object.permissions.administer?.organizations;
    // },
    // obj_teams() {
    //   return this.object.permissions.administer?.teams;
    // },
    createdUser() {
      let user = this.object.created_by ? this.object.created_by : null;
      let name = null;
      if (user) {
        name = user.first_name + " " + user.last_name;
      }
      return name;
    },
    byline() {
      let byline = "";
      if (this.object.createdUser) {
        byline += "By " + this.object.createdUser;
      }
      return byline;
    },
    createdAt() {
      return "Created on " + this.formatDate(this.object.created_at_ms);
    },
    updatedAt() {
      return "Updated on " + this.formatDate(this.object.modified_at_ms);
    },
    oxScore() {
      let score;
      if (this.object) {
        score = Number(this.object.ox_score);
      } else {
        score = Number(this.object.ox_score);
      }
      return score;
    },
    hasSkipped() {
      let skip;
      if (this.object) {
        skip = this.object.has_skipped;
      } else {
        skip = this.object.has_skipped;
      }
      return skip;
    },
  },
  methods: {
    setFeatured(object) {
      this.$emit("set-featured", object);
    },
    highlighted(name) {
      if (this.searchText) {
        return DOMPurify.sanitize(name).replace(new RegExp(this.searchText, "gi"), (match) => {
          return '<span class="font-bold">' + match + "</span>";
        });
      }
      return name;
    },
    withLinebreaks(str) {
      let clean = DOMPurify.sanitize(str);
      clean = clean.replace("\n", "<br/>");
      return clean;
    },
    truncated(str) {
      let max_length = 100;
      if (str && str.length > max_length) {
        return str.slice(0, max_length) + "...";
      }
      // str = str.replace("\n", "<br/>")
      return str;
    },
    truncatedFeatured(str) {
      let max_length = 160;
      if (str && str.length > max_length) {
        return str.slice(0, max_length) + "...";
      }
      return str;
    },
    scorecardsByFramework(object) {
      return getReportScorecardsByFramework(object);
    },
    sortedReports(object) {
      let reports = [...object.reports];
      reports.sort((a, b) => {
        return b.ox_score - a.ox_score;
      });
      return reports;
    },
    getCriteriaColorStyle(criteria) {
      return `background-color: ${chart_colors[criteria.index]}; color:#FFF; `;
    },
    async pinObject(obj) {
      let data = {};
      data[`pinned_${obj.__type}`] = obj.id;
      data["unpin"] = this.pinned;
      await this.$sendEvent("update_my_pins", data);
    },
    searchForTag(tag) {
      this.emitter.emit("updateSearch", { query: "tag:" + tag.name });
    },
  },
};
</script>
<style scoped>
.three-lines {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3; /* number of lines to show */
  line-clamp: 3;
  -webkit-box-orient: vertical;
}
.two-lines {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* number of lines to show */
  line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
