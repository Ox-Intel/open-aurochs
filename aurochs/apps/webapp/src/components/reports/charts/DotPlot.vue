<!-- eslint-disable vue/no-v-html -->
<template>
  <div class="relative">
    <div
      ref="dotplot"
      class="w-full h-full pb-2 pt-1.5 relative"
      data-cy="dot-plot"
      :style="`height: ${graphHeight}px`"
    >
      <div class="ox-chart relative top-0 left-0 h-full w-full">
        <div v-if="!isEmpty || !hideBarIfEmpty" class="baseline absolute bottom-4" />
        <div
          v-if="isEmpty && hideBarIfEmpty"
          class="text-medium-grey align-middle text-center flex h-full w-full place-content-center place-items-center"
        >
          <div class="ml-4">No Scores</div>
        </div>
        <div
          v-if="
            scoresWithOffsets.length > 0 && (scores_by_criteria.average_score || scores_by_criteria.average_score === 0)
          "
          class="average-area cursor-pointer absolute w-full h-full z-10"
        >
          <div
            class="absolute average-point-block h-full bottom-0"
            :style="`left: ${Math.round(average.score * 10) + 0.5}%;  z-index: 0; padding-left: 2px;`"
            :data-cy="`point-average-${String(Number(average.score).toFixed(1)).replace('.', '_')}`"
            @mouseover="startAverageHover(average)"
            @mouseout="endAverageHover(average)"
          >
            <div v-if="average.hovering" class="label average" :style="`bottom: ${averageBottom};margin-left: -75px;`">
              <div class="caption border-ox-score">
                <!-- :style="`border-color: ${dotColor(avarage}; `" -->
                Average Score
              </div>
              <div class="score_container">
                <!-- :style="`background-color: ${dotColor(avarage};`" -->
                <div class="score_box bg-ox-score">
                  <div class="score_number">
                    {{ trimNumber(average.score) }}
                  </div>
                </div>
              </div>
              <!-- :style="`border-top-color: ${dotColor(avarage};`" -->
              <div class="down-arrow border-ox-score" />
            </div>
            <div class="average-line absolute bottom-0" />
            <!-- :style="`border-color: ${dotColor(avarage};`" -->
          </div>
          <!-- <div
          class="absolute stdev-point-block"
          :style="`left: ${(average.score - 3.4) * 10}%; bottom: ${
            30 + maxOffsets * 10
          }px; z-index: 0;`"
          :data-cy="`stdev-average-${String(
            Number(average.score).toFixed(1)
          ).replace('.', '_')}`"
        >
        </div> -->
        </div>
        <div class="plot-area absolute top-0 w-full h-full">
          <template v-for="(score, dot_idx) in scoresWithOffsets" :key="dot_idx">
            <div
              v-if="score.score != undefined && score.score != null"
              class="absolute inline-block"
              :class="isHovering(score, dot_idx) ? 'z-50' : 'z-10'"
              :style="`left: ${Math.round(Number(score.score) * 10)}%; bottom: ${scoreBottom(score)}px; `"
              :data-cy="`point-${String(Number(score.score).toFixed(1)).replace('.', '_')}`"
              @mouseover="startHover(score, dot_idx)"
              @mouseout="endHover(score, dot_idx)"
            >
              <div v-if="isHovering(score, dot_idx)" class="label">
                <div class="caption" :style="`border-color: ${dotColor(score)}; `" v-html="scoreCaption(score)"></div>
                <div class="score_container">
                  <div class="score_box" :style="`background-color: ${dotColor(score)}; `">
                    <div class="score_number">
                      {{ trimNumber(score.score) }}
                    </div>
                  </div>
                </div>
                <div class="down-arrow" :style="`border-top-color: ${dotColor(score)}; `" />
              </div>
              <div v-if="!isReport(score) && score.scorer">
                <OxAvatar :user="score.scorer" :small="true" class="absolute -mt-2 cursor-pointer" />
              </div>
              <div
                v-if="isReport(score) || !score.scorer"
                class="dot absolute text-xs text-center align-middle w-6 h-6"
                :style="
                  score.average
                    ? `border-color: ${dotColor(score)}; color: ${dotColor(score)};`
                    : `background-color: ${dotColor(score)}; `
                "
                role="button"
                :class="
                  (score.average ? 'average-dot' : 'text-white') +
                  ' ' +
                  (isReport(score) && !score.average ? 'rounded-sm' : 'rounded-full')
                "
              ></div>
              <div
                v-if="isReport(score) || !score.scorer"
                class="absolute text-xs text-center align-middle w-6 h-6 -top-2 left-0 font-bold"
                role="button"
                :class="score.average ? '' : 'text-white'"
                :style="score.average ? `color: ${dotColor(score)};` : ''"
              >
                <!-- style="z-index: 99999" -->
                {{ getInitials(score) }}
              </div>
              <div
                v-if="score.gpt_scored_last"
                class="absolute bottom-0 right-0 p-0 text-center bg-ox-score text-ox-score-content text-xs"
                style="
                  font-size: 0.4rem;
                  line-height: 0.75rem;
                  vertical-align: middle;
                  width: 0.75rem;
                  height: 0.75rem;
                  right: -0.25rem;
                  bottom: -0.25rem;
                "
              >
                AI
              </div>
            </div>
          </template>
        </div>
        <!--  <div
        v-if="
          scores_by_criteria.average_score ||
          Number(scores_by_criteria.average_score) === 0
        "
        class="relative"
        :style="`left: ${average.score * 10}%`"
        :data-cy="`point-average-${String(
          Number(average.score).toFixed(1)
        ).replace('.', '_')}`"
        @mouseover="startAverageHover(average)"
        @mouseout="endAverageHover(average)"
      >
        <div v-if="average.hovering" class="label">
          <div
            class="caption"
            :style="`border-color: ${dotColor(score)}; `"
          >Average Score</div>
          <div class="score_container">
            <div class="score_box" :style="`background-color: ${dotColor(score)};`">
              <div class="score_number">
                {{ trimNumber(average.score) }}
              </div>
            </div>
          </div>
          <div class="down-arrow" :style="`border-top-color: ${dotColor(score)};`" />
        </div>
        <div
          class="dot average-dot absolute rounded-full bg-white border w-6 h-6"
          :style="`border-color: ${dotColor(score)};`"
          role="button"
        />
      </div>
    </div> -->
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../../stores/aurochs";
import chart_colors from "../../../mixins/chart_color";
import trimNumber from "../../../mixins/trim_number";
import { standardDeviation } from "../../../mixins/stats.js";

import OxAvatar from "../../common/OxAvatar.vue";

export default {
  components: {
    OxAvatar,
  },
  mixins: [trimNumber],
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    scores_by_criteria: {
      type: Object,
      default: () => {},
    },
    color: {
      type: String,
      default: "",
    },
    theme: {
      type: String,
      default: "",
    },
    idx: {
      type: Number,
      default: 0,
    },
    groupByReport: {
      type: Boolean,
      default: () => false,
    },
    hideBarIfEmpty: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const average = ref({
      score: Number(props.scores_by_criteria.average_score),
      name: "Average Score",
      hovering: false,
    });
    const hovering_list = ref({});
    return {
      chart_colors,
      average,
      hovering_list,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    scoresWithOffsets() {
      let scores = [];
      let score_counts = [];
      for (let score of this.scores_by_criteria.scores) {
        if (score_counts[score.score] == undefined) {
          score_counts[score.score] = 0;
        } else {
          score_counts[score.score] += 1;
        }
        score.offset = score_counts[score.score];
        scores.push(score);
      }
      // scores.push({
      //   score: Number(this.scores_by_criteria.average_score),
      //   scorer: {"full_name": "Average Score"},
      //   average: true,
      //   hovering: false,
      // })
      return scores;
      // this.scores_by_criteria.scores[i]
    },
    isEmpty() {
      if (this.scores_by_criteria.scores.length == 0) {
        return true;
      }
      for (let sc of this.scores_by_criteria.scores) {
        if (
          (sc.score && sc.score != null && sc.score > 0) ||
          (!isNaN(Number(sc.score)) && sc.score === 0) ||
          sc.score === "0.0"
        )
          return false;
      }
      return true;
    },
    stddev() {
      let scores = [];
      for (let score of this.scores_by_criteria.scores) {
        scores.push(Number(score.score));
      }
      return standardDeviation(scores);
    },
    maxOffsets() {
      let score_counts = [];
      let max_offsets = 0;
      for (let score of this.scores_by_criteria.scores) {
        if (score_counts[score.score] == undefined) {
          score_counts[score.score] = 0;
        } else {
          score_counts[score.score] += 1;
        }
        if (score_counts[score.score] > max_offsets) {
          max_offsets = score_counts[score.score];
        }
      }
      return max_offsets;
    },
    graphHeight() {
      return 80 + (this.maxOffsets > 0 ? 0 : 0) + this.maxOffsets * 20;
    },
    averageBottom() {
      return 14 + (this.maxOffsets > 0 ? 0 : 0) + this.maxOffsets * 18;
    },
  },
  watch: {
    "scores_by_criteria.average_score": {
      deep: true,
      handler: function (newVal) {
        this.average.score = Number(newVal);
        this.hovering_list = {};
      },
    },
    groupByReport: {
      handler: function () {
        this.hovering_list = {};
      },
    },
  },
  methods: {
    scoreBottom(score) {
      // if (!score.score && ) {
      //   return 0;
      // }
      return (
        6 +
        (this.isReport(score) ? 12 : 0) +
        // this.maxOffsets * 24 +
        Number(score.offset) * (this.isReport(score) ? 24 : 24)
      );
    },
    dotColor(score) {
      if (this.color) {
        return this.color;
      }
      let colors = [
        "hsl(200, 30%, 80%)",
        "hsl(200, 30%, 70%)",
        "hsl(200, 30%, 60%)",
        "hsl(200, 30%, 50%)",
        "hsl(200, 30%, 40%)",
        "hsl(200, 30%, 30%)",
        "hsl(200, 30%, 20%)",

        "hsl(225, 30%, 80%)",
        "hsl(225, 30%, 70%)",
        "hsl(225, 30%, 60%)",
        "hsl(225, 30%, 50%)",
        "hsl(225, 30%, 40%)",
        "hsl(225, 30%, 30%)",
        "hsl(225, 30%, 20%)",

        "hsl(180, 30%, 80%)",
        "hsl(180, 30%, 70%)",
        "hsl(180, 30%, 60%)",
        "hsl(180, 30%, 50%)",
        "hsl(180, 30%, 40%)",
        "hsl(180, 30%, 30%)",
        "hsl(180, 30%, 20%)",
      ];

      return colors[this.getColorIndex(score)];
    },
    dotStyle(point) {
      return `left: ${Number(point.score) * 10}%;`;
    },
    isHovering(score, dot_idx) {
      return (
        this.hovering_list[
          `${dot_idx}-${score?.criteria?.id}-${score.score}-${score.weight}-${score?.scorer?.full_name}-${score.report?.id}`
        ] === true
      );
    },
    startHover(score, dot_idx) {
      this.hovering_list[
        `${dot_idx}-${score?.criteria?.id}-${score.score}-${score.weight}-${score?.scorer?.full_name}-${score.report?.id}`
      ] = true;
    },
    endHover(score, dot_idx) {
      this.hovering_list[
        `${dot_idx}-${score?.criteria?.id}-${score.score}-${score.weight}-${score?.scorer?.full_name}-${score.report?.id}`
      ] = false;
    },
    startAverageHover(score) {
      score.hovering = true;
    },
    endAverageHover(score) {
      score.hovering = false;
    },
    getInitials(score) {
      if (this.groupByReport && score.report) {
        return score.report.name.slice(0, 2);
      }
      return score.scorer?.initials;
    },
    getColorIndex(score) {
      if (this.groupByReport && score.report) {
        return String(score.report.color_index);
      }
      if (score.scorer?.id) {
        return score.scorer.color_index;
      }
    },
    isReport(score) {
      // TODO: SS: Not the most efficient way to do this, but my brain is tired.
      score;
      if (this.groupByReport || score?.scorer?.user_average) {
        return true;
      }
      return false;
    },
    scoreCaption(score) {
      // TODO: SS: Not the most efficient way to do this, but my brain is tired.
      // if (this.labelReport) {
      //   return this.report.name;
      // }
      if (!this.groupByReport && score.report) {
        return "<b>" + score.report.name + "</b><br/>" + score.scorer.full_name;
        // scs_copy.scorer.initials = report.name.slice(0, 2)
      }
      return score.scorer?.full_name || "";

      // var names = "";
      // for (var i in this.scores_by_criteria.scores) {
      //   if (this.scores_by_criteria.scores[i].score == score.score) {
      //     names +=
      //       this.scores_by_criteria.scores[i].scorer.full_name + ",<br/> ";
      //   }
      // }

      // if (score.score == this.scores_by_criteria.average_score) {
      //   names = "Average Score,<br/> " + names;
      // }
      // names = names.substring(0, names.length - 7);
      // return names;
      // return `<b>${this.trimNumber(score.score)}</b> - ${names}`;
    },
  },
};
</script>

<style scoped>
.baseline {
  @apply w-full max-h-px border-b-2;
}
.ox-chart {
  bottom: -50%;
}
.dot {
  @apply absolute pt-1;
  top: -12px;
  font-size: 0.6rem;
  vertical-align: middle;
}
.average-area {
  width: 11px;
}
.average-dot {
  border-width: 3px;
  @apply bg-white;
}
.average-line {
  border: 1px solid #f44;
  border-width: 0 2px 0 0;
  width: 0;
  height: 95%;
  left: 8px;
  /*margin-left: 11px;*/
  @apply border-ox-score;
  /*@apply border-medium-grey;*/
}
.label {
  @apply absolute w-auto block text-center;
  transform: translate(-50%, -95%);
  padding-left: 28px;
  z-index: 9999999;
  pointer-events: none;
}
.label .score_container {
  @apply w-full;
}
.label .score_box {
  @apply block bg-ox-score p-0 w-6 h-4 mx-auto text-white font-bold relative text-center;
}
.label .score_number {
  @apply absolute text-center w-full;
  bottom: -6px;
}
.label .caption {
  @apply block rounded bg-base-200 p-2 border whitespace-nowrap;
}
.label.hovering .caption {
}
.label .down-arrow {
  @apply mx-auto;
  margin-top: 0;
  width: 0;
  height: 0;
  border-left: 12px solid transparent;
  border-right: 12px solid transparent;
  border-bottom: 12px solid transparent;
  border-top-width: 12px;
}
.label.average {
  transform: none;
}
.average-area {
  top: 0;
  left: 0;
  width: 100%;
}
.average-point-block {
  width: 12px;
  /*margin-left: -10px;*/
}
.stdev-point-block {
  @apply absolute h-full;
  width: 63%;
  background: #8e24ff11;
}
</style>
