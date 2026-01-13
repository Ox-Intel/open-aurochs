<template>
  <div class="card shadow-xl my-5 border-base-300 border">
    <div class="card-body">
      <div class="card-title" :class="{ 'border-b-2': open }">
        <div class="flex w-full justify-between">
          <router-link :to="`/framework/${frameworkAggregate.framework.id}`" class="no-underline">
            <div id="framework-icon" class="flex flex-row justify-center items-end my-3">
              <OxChartIcon
                :chart_id="`activity_icon_${frameworkAggregate.framework.id}`"
                :criteria="frameworkAggregate.framework.criteria"
                :small="true"
                :horns="true"
              />
              <div class="text-2xl ml-2">
                {{ frameworkAggregate.framework.name }}
              </div>
            </div>
          </router-link>
          <div class="flex">
            <div class="btn btn-primary btn-outline whitespace-nowrap" @click="toggleComments()">
              {{ toggleCommentText() }}
            </div>
            <div role="button" class="btn btn-ghost hover:bg-base-300 mr-2" @click="toggleOpen()">
              <div v-if="!open">
                <FontAwesomeIcon :icon="['fad', 'chevron-down']" class="h-4 w-4 inline" />
                Expand
              </div>
              <div v-else>
                <FontAwesomeIcon :icon="['fad', 'chevron-up']" class="h-4 w-4 inline" />
                Collapse
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="overflow-x-auto w-full">
        <div
          v-if="open"
          :style="`min-width: 100%; width: ${560 + (showComments ? frameworkAggregate.scorecards.length * 460 : 0)}px;`"
        >
          <table class="table-fixed">
            <!-- :style="`width: ${frameworkAggregate.scorecards.length * (600 + (showComments ? 600 : 0))}px;`" -->
            <tr class="align-bottom">
              <th>
                <div class="flex justify-between">
                  <!-- <div>Criteria</div> -->
                  <div>Importance</div>
                </div>
              </th>
              <th>Average Score</th>
              <template v-for="(scorecard, idx) in frameworkAggregate.scorecards" :key="idx">
                <th :colspan="showComments ? '2' : '1'" :class="!showComments ? 'w-8 px-4' : 'px-4'">
                  <div class="flex flex-wrap" :class="showComments ? '' : 'place-content-center'">
                    <div v-if="!showComments" class="grow text-left">
                      <div class="whitespace-nowrap text-md text-center ml-0 mb-0">
                        {{ scorecard.scorer.full_name }}
                      </div>
                      <div class="whitespace-nowrap text-sm font-light text-center mb-1">
                        {{ formatDate(scorecard.modified_at_ms) }}
                      </div>
                    </div>
                    <div class="p-2 pt-1">
                      <OxScoreBox :ox-score="Number(scorecard?.ox_score)" :has-skipped="scorecard?.has_skipped" />
                    </div>
                    <div v-if="showComments" class="grow text-left">
                      <div class="whitespace-nowrap text-md text-left ml-8">
                        {{ scorecard.scorer.full_name }}
                      </div>
                      <div class="whitespace-nowrap text-sm font-light text-left ml-8">
                        {{ formatDate(scorecard.modified_at_ms) }}
                      </div>
                    </div>
                  </div>
                </th>
              </template>
              <th v-if="!showComments" class="text-left">
                <!-- Scores -->
              </th>
            </tr>
            <template v-for="(sbc, idx) in frameworkAggregate.scores_by_criteria" :key="idx">
              <tr :data-cy="`all-scorecards-row-${idx}`" :class="idx % 2 ? 'bg-base-100' : 'bg-base-200'">
                <td class="criteria-list-item">
                  <CriteriaListItem :criteria="sbc.criteria" :idx="idx" :bg="idx % 2 ? 'bg-base-100' : 'bg-base-200'" />
                </td>
                <td class="w-20 place-content-center text-center align-middle">
                  <div
                    data-cy="average-score"
                    class="block text-white text-center text-bold text-l rounded p-3 m-6 w-12 h-12"
                    :style="`background-color: var(--criteria-color-${sbc.criteria.index + 1})`"
                  >
                    {{ trimNumber(sbc.average_score) }}
                  </div>
                </td>
                <template v-for="(score, score_idx) in sbc.scores" :key="score_idx">
                  <td class="w-20 text-center place-content-center align-middle">
                    <div class="w-full place-content-center">
                      <div
                        :data-cy="`score-${score_idx}`"
                        class="block text-white text-bold text-l rounded p-3 w-12 h-12"
                        :class="showComments ? 'm-6' : 'my-6 mx-auto'"
                        :style="`background-color: var(--criteria-color-${sbc.criteria.index + 1})`"
                      >
                        {{ trimNumber(score.score) }}
                      </div>
                    </div>
                  </td>
                  <td v-if="showComments" class="align-middle comments">
                    <article
                      :data-cy="`comment-${score_idx}`"
                      class="scorecard-comment max-w-fit prose text-linebreaks p-4 m-4 ml-0"
                    >
                      {{ score.comment ? score.comment : "No comments." }}
                    </article>
                  </td>
                </template>
                <td v-if="!showComments" class="w-1/3"></td>
              </tr>
            </template>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import trimNumber from "../../mixins/trim_number";
import OxScoreBox from "../common/OxScoreBox.vue";
import OxChartIcon from "../common/icons/OxChartIcon.vue";
import CriteriaListItem from "../framework/CriteriaListItem.vue";
import chart_colors from "../../mixins/chart_color";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faChevronDown } from "@fortawesome/pro-duotone-svg-icons/faChevronDown";
import { faChevronUp } from "@fortawesome/pro-duotone-svg-icons/faChevronUp";

library.add(faChevronDown, faChevronUp);

export default {
  components: {
    OxScoreBox,
    OxChartIcon,
    CriteriaListItem,
    FontAwesomeIcon,
  },
  mixins: [formatDate, trimNumber],
  props: {
    frameworkAggregate: {
      type: Object,
      default: () => {},
    },
  },
  setup() {
    const open = ref(true);
    const saving = ref(false);
    const actions_taken = ref(false);
    const showComments = ref(true);
    const editing = ref(false);
    const editingScores = ref({});

    return {
      aurochsData: useAurochsData(),
      open,
      editing,
      saving,
      actions_taken,
      editingScores,
      showComments,
      chart_colors,
    };
  },
  computed: {
    showAlert() {
      return this.editing && !this.actions_taken;
    },
  },
  methods: {
    toggleOpen() {
      this.open = !this.open;
      this.actions_taken = true;
    },
    rowClass(index) {
      if (this.editing) {
        return "bg-base-100";
      } else {
        if (index % 2) {
          return "bg-base-300";
        } else {
          return "bg-base-200";
        }
      }
    },
    toggleComments() {
      this.showComments = !this.showComments;
    },
    getCriteriaColor(idx) {
      const color_idx = idx % this.chart_colors.length;
      return this.chart_colors[color_idx];
    },
    toggleCommentText() {
      return this.showComments ? "Hide Comments" : "Show Comments";
    },
  },
};
</script>

<style scoped>
.criteria-list-item > div {
  max-width: 40rem;
  min-width: 30rem;
  /*min-height: 4rem;*/
}
.scorecard-comment {
  min-width: 30rem;
}
</style>
