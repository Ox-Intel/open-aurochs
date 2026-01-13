<template>
  <div :data-cy="dataCy">
    <template v-for="(sc, idx) in orderedScorecards" :key="idx">
      <div v-if="sc.scorer.id == aurochsData.user.id" class="card shadow-xl bg-base-100 mt-8 border-base-300 border">
        <MyScorecardsScorecard
          :scorecard="sc"
          :report="report"
          :mine="true"
          :sc_idx="String(sc.id)"
          :data_cy_idx="idx"
        />
      </div>
    </template>
    <template v-if="canView">
      <template v-for="(sc, idx) in orderedScorecards" :key="idx">
        <div
          v-if="sc.scorer.id != aurochsData.user.id && canViewScorecard(sc)"
          class="card shadow-xl bg-base-100 mt-8 border-base-300 border"
        >
          <MyScorecardsScorecard
            :scorecard="sc"
            :report="report"
            :mine="false"
            :sc_idx="String(sc.id)"
            :data_cy_idx="idx"
          />
        </div>
      </template>
    </template>
    <span v-if="!canView && !canScore" data-cy="no-permissions"></span>
    <div
      v-if="report?.scorecards.length == 0 && canScore"
      class="card w-full bg-base-200 card-bordered my-8 max-w-screen-md"
      data-cy="no-scorecards"
    >
      <div class="card-body w-full">
        <div class="flex">
          <div class="w-12 text-center">
            <FontAwesomeIcon :icon="['fad', 'bars-progress']" class="h-12 w-12 text-medium-grey" />
          </div>
          <div class="grow text-left px-4 pt-2 flex justify-between">
            <div class="text-xl text-medium-grey">You have not added any scorecards.</div>
            <label
              v-if="canScore"
              for="add-scorecard-modal"
              class="btn btn-primary -mt-2"
              role="button"
              data-cy="add-scorecard"
            >
              <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
              Add Scorecard
            </label>
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="report?.has_hidden_scorecards"
      class="card w-full bg-base-200 card-bordered my-8 max-w-screen-md"
      data-cy="hidden-scorecards"
    >
      <div class="card-body w-full">
        <div class="flex">
          <div class="w-12 text-center">
            <FontAwesomeIcon :icon="['fad', 'lock']" class="h-12 w-12 text-medium-grey" />
          </div>
          <div class="grow text-left px-4 -pt-2 -mt-1 flex justify-between">
            <div class="text-xl text-medium-grey">
              One or more scorecards are hidden because you do not have permissions to view them.
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="orderedScorecards.length > 0" class="max-w-screen-md mt-8">
      <label v-if="canScore" for="add-scorecard-modal" class="btn btn-primary -mt-2" role="button">
        <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
        Add Scorecard
      </label>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import { checkCanEdit, checkCanScore, checkCanView } from "../../mixins/permissions.js";
import MyScorecardsScorecard from "./MyScorecardsScorecard.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faUnlock } from "@fortawesome/pro-duotone-svg-icons/faUnlock";
import { faLock } from "@fortawesome/pro-duotone-svg-icons/faLock";
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
import { faRotate } from "@fortawesome/pro-duotone-svg-icons/faRotate";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faDownload } from "@fortawesome/pro-duotone-svg-icons/faDownload";
import { faBarsProgress } from "@fortawesome/pro-duotone-svg-icons/faBarsProgress";

library.add(
  faUnlock,
  faLock,
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
  faRotate,
  faPlus,
  faDownload,
  faBarsProgress
);

export default {
  components: {
    MyScorecardsScorecard,
    FontAwesomeIcon,
  },
  mixins: [formatDate],
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    dataCy: {
      type: String,
      default: () => "",
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    canEdit() {
      return checkCanEdit(this.report, this.aurochsData.user);
    },
    canScore() {
      return checkCanScore(this.report, this.aurochsData.user);
    },
    canView() {
      return checkCanView(this.report, this.aurochsData.user);
    },
    orderedScorecards() {
      if (this.report.scorecards && this.report.scorecards.length > 0) {
        let sorted_scorecards = this.report.scorecards;
        sorted_scorecards.sort((a, b) => b.created_at_ms - a.created_at_ms);
        return sorted_scorecards;
      }
      return [];
    },
  },
  methods: {
    toggleOpen(sc) {
      sc.open = !sc.open;
    },
    canViewScorecard(sc) {
      return this.aurochsData.frameworks && this.aurochsData.frameworks[String(sc.framework.id)] != undefined;
    },
  },
};
</script>
