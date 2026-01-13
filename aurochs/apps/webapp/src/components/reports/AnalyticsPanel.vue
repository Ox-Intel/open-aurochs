<template>
  <div class="w-full" :data-cy="dataCy">
    <div
      v-if="Object.keys(scorecardsByFramework).length == 0"
      class="card card-bordered bg-base-200"
      data-cy="no-scorecards"
      :class="graphOnly || embedded ? 'mt-8' : 'm-8 w-full max-w-screen-md'"
    >
      <div class="card-body w-full">
        <div class="flex">
          <div class="w-12 text-center fa-rotate-270 mb-2">
            <FontAwesomeIcon
              :icon="['fad', 'chart-candlestick']"
              class="h-12 w-12 text-medium-grey fa-rotate-90 fa-flip-vertical"
            />
          </div>
          <div class="grow text-left px-4 pt-2 flex justify-between">
            <div class="text-xl text-medium-grey">No scorecards yet.</div>
            <label
              v-if="canScore && !embedded"
              for="add-scorecard-modal"
              class="btn btn-primary -mt-2"
              role="button"
              data-cy="add-scorecard-from-panel"
            >
              <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
              Add Scorecard
            </label>
          </div>
        </div>
      </div>
    </div>
    <div v-for="(frameworkAggregate, key, idx) in scorecardsByFramework" :key="key">
      <AnalyticsFrameworkPane
        :ref="`analyticsframeworkpane-${key}`"
        :framework-aggregate="frameworkAggregate"
        :report="report"
        :idx="String(idx)"
        :hide-confidence="hideConfidence"
        :hide-ox-score="hideOxScore"
        :hide-noise="hideNoise"
        :hide-suggestions="hideSuggestions"
        :show-average-noise-warning="showAverageNoiseWarning"
        :start-open="startOpen"
        :graph-only="graphOnly"
        :toggle-bar="toggleBar"
        :allow-group-by-report="allowGroupByReport"
      />
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import { checkCanEdit, checkCanScore } from "../../mixins/permissions.js";
import AnalyticsFrameworkPane from "./AnalyticsFrameworkPane.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faChartCandlestick } from "@fortawesome/pro-duotone-svg-icons/faChartCandlestick";

library.add(faChartCandlestick);

export default {
  components: {
    AnalyticsFrameworkPane,
    FontAwesomeIcon,
  },
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    scorecardsByFramework: {
      type: Object,
      default: () => {},
    },
    dataCy: {
      type: String,
      default: () => "",
    },
    hideConfidence: {
      type: Boolean,
      default: () => false,
    },
    hideOxScore: {
      type: Boolean,
      default: () => false,
    },
    hideNoise: {
      type: Boolean,
      default: () => false,
    },
    hideSuggestions: {
      type: Boolean,
      default: () => false,
    },
    showAverageNoiseWarning: {
      type: Boolean,
      default: () => false,
    },
    startOpen: {
      type: Boolean,
      default: () => true,
    },
    toggleBar: {
      type: Boolean,
      default: () => false,
    },
    allowGroupByReport: {
      type: Boolean,
      default: () => false,
    },
    graphOnly: {
      type: Boolean,
      default: () => false,
    },
    embedded: {
      type: Boolean,
      default: () => false,
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
      previousOpenState: ref({}),
    };
  },
  computed: {
    canEdit() {
      return checkCanEdit(this.report, this.aurochsData.user);
    },
    canScore() {
      return checkCanScore(this.report, this.aurochsData.user);
    },
  },
  methods: {
    setOpen(val) {
      for (let j in this.scorecardsByFramework) {
        this.previousOpenState[j] = this.$refs[`analyticsframeworkpane-${j}`][0].getOpen();
        this.$refs[`analyticsframeworkpane-${j}`][0].setOpen(val);
      }
    },
    resetOpen() {
      for (let j in this.scorecardsByFramework) {
        this.$refs[`analyticsframeworkpane-${j}`][0].setOpen(this.previousOpenState[j]);
      }
    },
  },
};
</script>
