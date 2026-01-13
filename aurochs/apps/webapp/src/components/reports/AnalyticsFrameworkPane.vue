<template>
  <div>
    <div>
      <div
        :ref="`framework-${idx}`"
        class="bg-base-100 border-base-200 border"
        :class="graphOnly ? '' : 'card shadow-xl my-5'"
        :data-cy="`framework-${idx}`"
        :style="graphOnly ? 'scale: 0.45; transform-origin: 0 0; width: 220%' : ''"
      >
        <div :class="graphOnly ? '' : 'card-body'">
          <article class="prose max-w-none">
            <div class="card-title" @click="barClick">
              <div id="framework-icon" class="flex flex-row justify-between items-end my-3 w-full">
                <div class="flex grow align-middle">
                  <OxChartIcon
                    :chart_id="`activity_icon_${frameworkAggregate.framework.id}`"
                    :criteria="frameworkAggregate.framework.criteria"
                    :small="true"
                    :horns="true"
                    class="inline-block h-10 w-10"
                  />
                  <router-link
                    :to="`/framework/${frameworkAggregate.framework.id}`"
                    class="inline-block ml-3 mt-1 no-underline"
                    :class="graphOnly ? ' text-md' : ' text-2xl'"
                  >
                    {{ frameworkAggregate.framework.name }}
                  </router-link>
                </div>
              </div>
              <div v-if="allowGroupByReport" class="form-control hiddenInExport">
                <label class="label cursor-pointer" data-cy="toggleByReportOrScorecard" @click="toggleIndividualScores">
                  <span
                    class="label-text whitespace-nowrap mr-2"
                    :class="showIndividualScorecards ? 'text-base-500' : 'text-primary'"
                    >By Report</span
                  >
                  <div class="rounded-full w-12 h-6 border-medium-grey border relative">
                    <div
                      data-cy="toggle-individual-scores"
                      class="bg-primary rounded-full h-6 w-6 absolute"
                      :class="showIndividualScorecards ? 'right-0' : 'left-0'"
                      style="margin-top: -1px"
                    ></div>
                  </div>
                  <span
                    class="label-text whitespace-nowrap ml-2"
                    :class="showIndividualScorecards ? 'text-primary' : 'text-base-500'"
                    >By Scorecard</span
                  >
                </label>
              </div>

              <div v-if="!graphOnly" class="my-2 flex flex-row items-end">
                <div class="form-control hiddenInExport">
                  <label
                    data-cy="toggle-all-comments"
                    role="button"
                    class="btn btn-ghost hover:bg-base-300"
                    :class="showComments ? 'text-primary' : ''"
                    @click.stop.prevent="toggleComments"
                  >
                    <span class="whitespace-nowrap">
                      <!-- :class="!showComments ? 'text-base-500' : 'text-primary'" -->
                      <FontAwesomeIcon
                        :icon="['fad', 'message-lines']"
                        class="h-4 w-4 inline align-middle opacity-50"
                      />
                      Comments
                    </span>
                    <!-- <div class="rounded-full w-12 h-6 border-medium-grey border relative">
                      <div
                        data-cy="toggle-individual-scores"
                        class="bg-primary rounded-full h-6 w-6 absolute"
                        :class="showComments ? 'right-0' : 'left-0'"
                        style="margin-top: -1px"
                      ></div>
                    </div>-->
                  </label>
                </div>
                <div
                  role="button"
                  class="btn btn-ghost hover:bg-base-300 hiddenInExport"
                  data-cy="toggle-open"
                  @click.stop.prevent="toggleOpen"
                >
                  <div v-if="!open">
                    <FontAwesomeIcon :icon="['fad', 'chevron-down']" class="h-4 w-4 inline align-middle" />
                    Expand
                  </div>
                  <div v-else>
                    <FontAwesomeIcon :icon="['fad', 'chevron-up']" class="h-4 w-4 inline align-middle" />
                    Collapse
                  </div>
                </div>
                <DownloadButton
                  class="btn btn-ghost btn-border-base-200 hiddenInExport"
                  @click="queueDownload($refs[`framework-${idx}`], frameworkAggregate?.framework?.name || null)"
                />
                <template v-if="frameworkAggregate.scorecards && frameworkAggregate.scorecards.length > 0">
                  <div
                    class="ml-4 box rounded border border-base-300 text-medium-grey text-center align-middle px-1 pt-1.5 pb-0 w-14"
                  >
                    <div class="text-xs mb-0">Scores</div>
                    <div class="text-xl font-bold -mt-1 mb-0">
                      {{ frameworkAggregate.scorecards.length }}
                    </div>
                  </div>
                  <OxScoreBox
                    v-if="!hideOxScore"
                    :ox-score="Math.round(Number(frameworkAggregate.average_ox_score))"
                    :has-skipped="aggregateHasSkipped(frameworkAggregate)"
                    data-cy="average-ox-score"
                    class="ml-4"
                  />
                </template>
              </div>
            </div>
            <table v-if="open" class="padding-t-4 border-t-2 border-base-300 w-full mb-4">
              <tr v-if="Object.keys(sortedCriteria).length > 0" class="w-full mb-2 mt-4 font-bold">
                <td class="" :class="hideConfidence ? 'w-4/12' : 'w-3/12'">
                  <div class="grow-0 flex justify-between">
                    <!-- <div>Criteria</div> -->
                    <div>Importance</div>
                  </div>
                </td>
                <td :class="'w-' + graphWidth + '/12'">
                  <div class="text-center">Scores</div>
                </td>

                <td v-if="showNoise" class="w-1/12">
                  <div :class="toggleBar ? '-ml-[1.25rem]' : 'text-center'">Noise</div>
                </td>

                <td v-if="showNoise" class=""></td>
                <td class="w-1/12 place-content-center">
                  <div class="text-center pl-2">Average</div>
                </td>
                <td v-if="!hideConfidence && !showComments" class="whitespace-nowrap">
                  <div class="text-left pl-2">Weighted Average</div>
                </td>
              </tr>
              <tr v-if="Object.keys(sortedCriteria).length == 0">
                <td colspan="99">
                  <div class="card bg-base-200 card-bordered mx-auto max-w-screen-md" data-cy="hidden-scorecards">
                    <div class="card-body w-full">
                      <div class="flex">
                        <div class="w-12 text-center">
                          <FontAwesomeIcon
                            :icon="['fad', 'chart-simple-horizontal']"
                            class="h-12 w-12 text-medium-grey"
                          />
                        </div>
                        <div class="grow text-left px-4 pt-2">
                          <div class="text-xl text-dark-grey">
                            No scores or all scorecards contain only skipped scores.
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </td>
              </tr>
              <template v-for="(sbc, criteria_idx) in sortedCriteria" :key="sbc.criteria.id">
                <tr
                  class="w-full"
                  :data-cy="`criteria-${criteria_idx}`"
                  :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                >
                  <td
                    class="align-middle"
                    :class="
                      (criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200') +
                      ' ' +
                      (hideConfidence ? 'w-4/12 ' : 'w-3/12 ') +
                      roundClass(criteria_idx)
                    "
                  >
                    <div class="flex" :class="showRowComments(sbc) ? 'my-4' : ''">
                      <div class="grow">
                        <CriteriaListItem
                          :criteria="sbc.criteria"
                          :idx="criteria_idx"
                          :thin="true"
                          :two-lines="true"
                          :bg="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                          :round-class="roundClass(criteria_idx)"
                        />
                      </div>
                    </div>
                    <!-- :bg="''" -->
                  </td>
                  <td
                    class=""
                    :class="(criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200') + ' ' + 'w-' + graphWidth + '/12'"
                  >
                    <div class="px-4 mr-4" @click.stop.prevent="toggleRowComments(sbc)">
                      <DotPlot
                        :report="report"
                        :scores_by_criteria="sbc"
                        :idx="criteria_idx"
                        :group-by-report="!showIndividualScorecards && allowGroupByReport"
                        :hide-bar-if-empty="true"
                      />
                    </div>
                  </td>
                  <td v-if="showNoise" class="w-1/12 align-middle whitespace-nowrap text-center px-4">
                    <div
                      class="flex place-content-center place-items-center whitespace-nowrap mb-0 text-base-300"
                      :style="`margin-top: ${noiseTop(sbc)}px;`"
                    >
                      <div class="badge" :class="getNoiseBadgeClass(sbc)" data-cy="noise">
                        <FontAwesomeIcon
                          v-if="sbc.stddev > 2.25"
                          :icon="['fad', 'triangle-exclamation']"
                          class="h-4 w-4 inline align-middle mr-2"
                        />
                        {{ getNoiseText(trimNumber(sbc.stddev)) }}
                      </div>
                      <div
                        v-if="showAverageNoiseWarning && !showIndividualScorecards && sbc.stddev > 2.25"
                        class="ml-2"
                      >
                        <div
                          data-cy="ox-suggestions"
                          class="tooltip z-50 inline-block text-linebreaks text-left mt-1"
                          :data-tip="`This criteria has high average noise across the reports in this stack.\n\nThis generally indicates either significant disagreements among scorers or unclear criteria guidance.`"
                        >
                          <div
                            class="mb-2 bg-ox-score text-ox-score-content rounded-2xl rounded-circle align-middle w-8 h-8 pt-1"
                          >
                            <OxHorns class="block h-6 w-6 mt-2 ml-1" />
                          </div>
                        </div>
                      </div>
                    </div>
                  </td>
                  <td v-if="showNoise">
                    <div v-if="!showAverageNoiseWarning && sbc.stddev > 2.25" class="w-12 ml-2">
                      <div
                        data-cy="ox-suggestions"
                        class="tooltip z-50 inline-block text-linebreaks text-left mt-1"
                        :data-tip="`${sbc.criteria.name} appears to result in noisy judgments${
                          sbc.criteria.weight >= 3 ? ' and has significant importance' : ''
                        }.\n\nTo reduce scoring noise, Ox suggests collecting more information on how users make this judgment${
                          sbc.criteria.weight >= 3
                            ? ' or reducing the importance of this criterion in the framework'
                            : ''
                        }.`"
                      >
                        <div
                          class="mb-2 bg-ox-score text-ox-score-content rounded-2xl rounded-circle align-middle w-8 h-8 pt-1"
                        >
                          <OxHorns class="block h-6 w-6 mt-2 ml-1" />
                        </div>
                      </div>
                    </div>
                    <div
                      v-if="!showAverageNoiseWarning && sbc.stddev < 1.2 && sbc.criteria.weight < 4"
                      class="w-12 ml-2"
                    >
                      <div
                        data-cy="ox-suggestions"
                        class="tooltip z-50 inline-block text-linebreaks text-left mt-1"
                        :data-tip="`${sbc.criteria.name} appears to have a low level of scoring noise, without high importance.\n\nOx recommends reviewing the importance of this criterion in the framework.`"
                      >
                        <div
                          class="mb-2 bg-ox-score text-ox-score-content rounded-2xl rounded-circle align-middle w-8 h-8 pt-1"
                        >
                          <OxHorns class="block h-6 w-6 mt-2 ml-1" />
                        </div>
                      </div>
                    </div>
                  </td>
                  <td class="w-1/12 align-middle text-center">
                    <div
                      class="block text-center text-white text-bold mx-auto align-middle text-l rounded p-3 w-12 h-12"
                      data-cy="average-score"
                      :class="sbcHasValidScores(sbc) ? '' : 'bg-medium-grey'"
                      :style="sbcHasValidScores(sbc) ? `background-color: ${getCriteriaColor(sbc.criteria.index)}` : ''"
                    >
                      {{ trimNumber(sbc.average_score) }}
                    </div>
                  </td>

                  <td v-if="!hideConfidence" class="w-3/12" :class="showComments ? '' : 'bg-base-100'">
                    <BarChart
                      :scores_by_criteria="sbc"
                      :color="getCriteriaColor(sbc.criteria.index)"
                      :idx="sbc.criteria.id"
                      :grey-if-empty="true"
                    />
                  </td>
                </tr>
                <!-- We're not on stacks, or on stacks reports. -->
                <template v-if="!allowGroupByReport">
                  <template v-for="(score, score_idx) in sbc.scores" :key="score_idx">
                    <tr
                      v-if="showRowComments(sbc)"
                      class="table-row w-full"
                      :data-cy="`criteria-comments-${criteria_idx}-${score_idx}`"
                      :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                    >
                      <td :colspan="commentsColspan">
                        <div
                          class="mb-6 flex flex-row min-h-[5rem]"
                          :data-cy="`scorecard-row-${idx}`"
                          :class="
                            (criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200') + (score_idx == 0 ? ' mt-10 ' : ' mt-6 ')
                          "
                        >
                          <div class="basis-1/3">
                            <div class="pl-16 flex">
                              <OxAvatar :user="score.scorer" class="mr-2" :small="false" />
                              <div class="text-base ml-2">
                                <div class="font-bold">{{ score.scorer?.full_name }}</div>
                                <div v-if="score.report && allowGroupByReport" class="font-normal text-base mb-4 mr-2">
                                  {{ score.report.name }}
                                </div>
                                <div v-if="score.modified_at_ms" class="font-light text-sm">
                                  {{ formatDate(score.modified_at_ms) }}
                                </div>
                              </div>
                            </div>
                          </div>
                          <div class="basis-2/3 pr-16 flex">
                            <div class="">
                              <article
                                class="prose max-w-none text-linebreaks relative"
                                data-cy="comment"
                                :class="score.comment ? '' : ' text-base-500'"
                              >
                                {{ score.comment ? score.comment : "No comments." }}
                                <!-- <div v-if="score.gpt_scored_last" class="absolute -bottom-1 -right-1 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs " style="font-size: 0.6rem">AI</div> -->
                              </article>
                            </div>
                          </div>
                        </div>
                      </td>
                      <td colspan="1">
                        <div class="my-3 align-top">
                          <div
                            class="flex place-items-center text-center align-middle w-full"
                            :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                          >
                            <div
                              v-if="score.score === null"
                              class="block text-medium-grey font-normal text-lg text-right h-12"
                              style="border-width: 0 0 0 2px"
                              data-cy="score"
                              :class="score.score > 0 ? 'p-4 pt-2 pl-2' : 'p-4 pt-2 pl-2'"
                            >
                              Skipped
                            </div>
                            <div
                              v-if="score.score !== null"
                              class="block text-white font-bold text-xl text-right h-12"
                              :style="
                                score.score > 0
                                  ? `background-color: var(--criteria-color-${score.criteria.index + 1}); width: ${
                                      score.score * sbc.criteria.weight
                                    }%;`
                                  : `color: var(--criteria-color-${
                                      score.criteria.index + 1
                                    }); border-color: var(--criteria-color-${
                                      score.criteria.index + 1
                                    }); border-width: 0 0 0 2px `
                              "
                              data-cy="score"
                              :class="score.score > 0 ? 'p-4 pt-2 pl-2' : 'p-4 pt-2 pl-2'"
                            >
                              {{ Math.round(score.score) }}
                            </div>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </template>
                </template>
                <!-- We're on stacks. -->
                <template v-if="allowGroupByReport">
                  <template v-for="(scored_report, rep_idx) in scoresGroupedByReport(sbc)" :key="rep_idx">
                    <!-- Report -->
                    <tr
                      v-if="showRowComments(sbc)"
                      class="table-row w-full"
                      :data-cy="`criteria-report-comments-${rep_idx}`"
                      :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                    >
                      <td :colspan="99">
                        <div
                          class="mb-3 flex flex-row relative text-ox-score-content"
                          :data-cy="`report-row-${rep_idx}`"
                          :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                          :style="`background-color: ${userColor(scored_report.report)}`"
                        >
                          <!-- <div
                            class="absolute w-full h-full"
                          ></div> -->
                          <div class="w-full">
                            <div class="pl-16 flex">
                              <!-- <OxAvatar :user="scored_report.report" class="mr-2" :small="false" /> -->
                              <div class="text-ox-score-content ml-2 py-2">
                                <div class="font-bold text-xl py-1">{{ scored_report.report?.name }}</div>
                                <!-- <div v-if="scored_report.report.modified_at_ms" class="font-light text-sm">
                                  {{ formatDate(scored_report.report.modified_at_ms) }}
                                </div> -->
                              </div>
                            </div>
                          </div>
                        </div>
                      </td>
                      <!--                    <td>
                        <div
                          class="block text-center text-white text-bold mx-auto align-middle text-l rounded p-3 w-12 h-12"
                          data-cy="average-score"
                          :class="sbcHasValidScores(sbc) ? '' : 'bg-medium-grey'"
                          :style="sbcHasValidScores(sbc) ? `background-color: ${getCriteriaColor(sbc.criteria.index)}` : ''"
                        >
                          {{ trimNumber(scored_report.average_score) }}
                        </div>
                      </td> -->
                    </tr>

                    <!-- Individual scores -->
                    <template v-for="(score, score_idx) in scored_report.scores" :key="score_idx">
                      <tr
                        v-if="showRowComments(sbc)"
                        class="table-row w-full"
                        :data-cy="`criteria-comments-${criteria_idx}-${score_idx}`"
                        :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                      >
                        <td :colspan="commentsColspan">
                          <div
                            class="my-3 flex flex-row"
                            :data-cy="`scorecard-row-${idx}`"
                            :class="
                              (criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200') +
                              (score_idx == 0 ? ' mt-0 ' : ' mt-2 ') +
                              (score_idx >= scored_report?.scores.length - 1 ? ' mb-8 ' : ' ')
                            "
                          >
                            <div class="basis-1/3">
                              <div class="pl-16 flex">
                                <OxAvatar :user="score.scorer" class="mr-2" :small="false" />
                                <div class="text-base ml-2">
                                  <div class="font-bold">{{ score.scorer?.full_name }}</div>
                                  <div v-if="score.modified_at_ms" class="font-light text-sm">
                                    {{ formatDate(score.modified_at_ms) }}
                                  </div>
                                </div>
                              </div>
                            </div>
                            <div class="basis-2/3 pr-16 flex">
                              <div class="">
                                <article
                                  class="prose max-w-none text-linebreaks relative"
                                  data-cy="comment"
                                  :class="score.comment ? '' : ' text-base-500'"
                                >
                                  {{ score.comment ? score.comment : "No comments." }}
                                  <!-- <div v-if="score.gpt_scored_last" class="absolute -bottom-1 -right-1 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs " style="font-size: 0.6rem">AI</div> -->
                                </article>
                              </div>
                            </div>
                          </div>
                        </td>
                        <td colspan="1">
                          <div
                            class="my-3 align-top w-48"
                            :class="score_idx >= scored_report?.scores.length - 1 ? ' mb-8 ' : ' '"
                          >
                            <div
                              class="flex place-items-center text-center align-middle w-full"
                              :class="criteria_idx % 2 ? 'bg-base-100' : 'bg-base-200'"
                            >
                              <div
                                v-if="score.score === null"
                                class="block text-medium-grey font-normal text-lg text-right h-12"
                                style="border-width: 0 0 0 2px"
                                data-cy="score"
                                :class="score.score > 0 ? 'p-4 pt-2 pl-2' : 'p-4 pt-2 pl-2'"
                              >
                                Skipped
                              </div>
                              <div
                                v-if="score.score !== null"
                                class="block text-white font-bold text-xl text-right h-12"
                                :style="
                                  score.score > 0
                                    ? `background-color: var(--criteria-color-${score.criteria.index + 1}); width: ${
                                        score.score * sbc.criteria.weight
                                      }%;`
                                    : `color: var(--criteria-color-${
                                        score.criteria.index + 1
                                      }); border-color: var(--criteria-color-${
                                        score.criteria.index + 1
                                      }); border-width: 0 0 0 2px `
                                "
                                data-cy="score"
                                :class="score.score > 0 ? 'p-4 pt-2 pl-2' : 'p-4 pt-2 pl-2'"
                              >
                                {{ Math.round(score.score) }}
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    </template>
                  </template>
                </template>
                <!-- <td colspan="1">
                  </td>

                  <td colspan="3">
                    <table class="comments p-4 w-full ">
                      <tr v-for="(score, score_idx) in sbc.scores" :key="score_idx" class="min-h-8 pb-2">
                        <td class="shrink cell-top font-bold text-base whitespace-nowrap">
                          <div class="ml-2 flex">
                            <OxAvatar :user="score.scorer" class="ml-4 mr-2 -mb-2" :small="true" />
                            <div class="">
                              <div>{{ score.scorer?.full_name }}:</div>
                              <div v-if="score.report && allowGroupByReport" class="font-normal text-base mb-4 mr-2">
                                {{ score.report.name }}
                              </div>
                            </div>
                          </div>
                        </td>
                        <td class="cell-top">
                          <div
                            :class="score.comment ? '' : 'text-dark-grey italic'"
                            class="pl-2 mb-2 text-linebreaks leading-tight mt-1 mr-4 text-base"
                          >
                            {{ score.comment || "No comments." }}
                          </div>
                        </td>
                        <td class="shrink w-24 pr-12 cell-top">
                          <div class="mr-10">
                            <div
                              class="block text-center text-white text-sm mx-auto align-middle text-l rounded p-1 pt-1.5 pb-0.5 w-8 h-8 mb-2"
                              data-cy="average-score"
                              :style="`background-color: ${userColor(score.scorer)}`"
                            >
                              {{ trimNumber(score.score) }}
                            </div>
                          </div>
                        </td>
                      </tr> 
                    </table>
                  </td>-->
                <td v-if="!hideConfidence && !showComments" class="bg-base-100"></td>
              </template>
            </table>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import OxChartIcon from "../common/icons/OxChartIcon.vue";
import OxHorns from "../../components/logo/OxHorns.vue";
import OxScoreBox from "../../components/common/OxScoreBox.vue";
import OxAvatar from "../../components/common/OxAvatar.vue";
import DotPlot from "./charts/DotPlot.vue";
import CriteriaListItem from "../framework/CriteriaListItem.vue";
import chart_colors from "../../mixins/chart_color";
import trimNumber from "../../mixins/trim_number";
import { standardDeviation } from "../../mixins/stats.js";
import formatDate from "../../mixins/format_date";
import BarChart from "./charts/BarChart.vue";
import DownloadButton from "../common/DownloadButton.vue";
import downloadArea from "../../mixins/download_area";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faChevronDown } from "@fortawesome/pro-duotone-svg-icons/faChevronDown";
import { faChevronUp } from "@fortawesome/pro-duotone-svg-icons/faChevronUp";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCommentLines } from "@fortawesome/pro-duotone-svg-icons/faCommentLines";
import { faMessageLines } from "@fortawesome/pro-duotone-svg-icons/faMessageLines";

library.add(faChevronDown, faChevronUp, faTriangleExclamation, faCommentLines, faMessageLines, faChartSimpleHorizontal);

export default {
  components: {
    OxChartIcon,
    DotPlot,
    CriteriaListItem,
    BarChart,
    OxHorns,
    FontAwesomeIcon,
    OxScoreBox,
    OxAvatar,
    DownloadButton,
  },
  mixins: [trimNumber, formatDate, downloadArea],
  props: {
    frameworkAggregate: {
      type: Object,
      required: true,
    },
    report: {
      type: Object,
      required: true,
    },
    idx: {
      type: String,
      default: () => {
        "";
      },
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
    startOpen: {
      type: Boolean,
      default: () => true,
    },
    showAverageNoiseWarning: {
      type: Boolean,
      default: () => false,
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
  },
  setup(props) {
    const showIndividualScorecards = ref(false);
    const showComments = ref(false);
    const openCommentRows = ref({});
    const open = ref(props.startOpen);

    return {
      aurochsData: useAurochsData(),
      chart_colors,
      showIndividualScorecards,
      showComments,
      openCommentRows,
      open,
    };
  },
  computed: {
    criterias() {
      return this.frameworkAggregate.framework.criteria;
    },
    graphWidth() {
      let cols = 12;
      if (this.showAverageNoiseWarning) {
        cols = 6;
      }
      if (this.hideConfidence) {
        if (this.hideNoise || this.showIndividualScorecards) {
          cols = 7;
        } else {
          cols = 6;
        }
      } else {
        cols = 4;
      }
      if (this.frameworkAggregate?.scorecards.length <= 1) {
        cols += 1;
      }
      return cols;
    },
    commentsColspan() {
      if (this.hideConfidence && !this.allowGroupByReport) {
        if (this.frameworkAggregate?.scorecards.length > 1) {
          return 4;
        }
        return 2;
      }
      if (this.frameworkAggregate?.scorecards.length <= 1) {
        return 3;
      }
      if (this.allowGroupByReport) {
        if (this.showIndividualScorecards) {
          return 2;
        }
        return 4;
      }
      return 5;
    },
    showNoise() {
      return (
        !this.allowGroupByReport &&
        !this.showIndividualScorecards &&
        this.frameworkAggregate?.scorecards.length > 1 &&
        ((!this.hideNoise && !this.showIndividualScorecards) || this.showAverageNoiseWarning)
      );
    },
    showSuggestions() {
      return (
        this.showAverageNoiseWarning ||
        !this.hideSuggestions ||
        (this.showIndividualScorecards && this.sbc.total_standard_dev > 0)
      );
    },
    sortedCriteria() {
      this.allowGroupByReport;
      if (this.showIndividualScorecards || !this.allowGroupByReport) {
        let criterias = [...this.frameworkAggregate.scores_by_criteria];
        return criterias.sort((a, b) => {
          if (a.criteria.relative_weight_as_percent == b.criteria.relative_weight_as_percent) {
            return a.criteria.index - b.criteria.index;
          }
          return b.criteria.relative_weight_as_percent - a.criteria.relative_weight_as_percent;
        });
      } else {
        // TODO: cleanup and optimize this.  I could't find clean/smart cycles to write this, so it's
        // Written in a very brute-force way.   Future optimization / cleanup work welcome!

        // Get a list of all reports.
        let reports = {};
        for (let sbc of this.frameworkAggregate.scores_by_criteria) {
          // Go through all the scorecards, make sure they're for this framework, and put them into the report list.
          for (let sc of sbc.scores) {
            if (sc.criteria.framework_pk == this.frameworkAggregate.framework.id) {
              if (
                sc.score != "" &&
                sc.score != "null" &&
                sc.score != null &&
                (Number(sc.score) || Number(sc.score) === 0)
              ) {
                if (reports[`rep_${sc.report.id}`] == undefined) {
                  reports[`rep_${sc.report.id}`] = {
                    report: sc.report,
                    criteria: {},
                  };
                }
                if (reports[`rep_${sc.report.id}`].criteria[`crit_${sc.criteria.id}`] == undefined) {
                  reports[`rep_${sc.report.id}`].criteria[`crit_${sc.criteria.id}`] = {
                    criteria: sc.criteria,
                    scoreValues: [],
                    scores: [],
                    total_score: 0,
                    standardDevs: [],
                    total_standard_dev: 0,
                  };
                }
                reports[`rep_${sc.report.id}`].criteria[`crit_${sc.criteria.id}`].total_score += Number(sc.score);
                reports[`rep_${sc.report.id}`].criteria[`crit_${sc.criteria.id}`].scoreValues.push(Number(sc.score));
                reports[`rep_${sc.report.id}`].criteria[`crit_${sc.criteria.id}`].scores.push(sc);
              }
            }
          }
        }

        // Go through the reports, sum up and get averages and stddevs for that report's scores.
        for (let rep_id in reports) {
          let rep = reports[rep_id];
          for (let crit_id in rep.criteria) {
            let crit = rep.criteria[crit_id];
            crit.average_score = 0;
            if (crit.scoreValues.length > 0) {
              crit.average_score = crit.total_score / crit.scoreValues.length;
            }
            crit.stddev = standardDeviation(crit.scoreValues);
            crit.total_standard_dev += crit.stddev;
            crit.standardDevs.push(crit.stddev);
          }
        }

        // Go through the reports and aggregate them into a unified criteria list.
        let return_criteria = {};

        for (let rep_id in reports) {
          let rep = reports[rep_id];
          for (let crit_id in rep.criteria) {
            let crit = rep.criteria[crit_id];
            // Add them to a unified criteria list
            if (return_criteria[`crit_${crit.criteria.id}`] == undefined) {
              return_criteria[`crit_${crit.criteria.id}`] = {
                criteria: crit.criteria,
                scoreValues: [],
                scores: [],
                standardDevs: [],
                total_score: 0,
                total_standard_dev: 0,
              };
            }
            return_criteria[`crit_${crit.criteria.id}`].standardDevs.push(
              crit.total_standard_dev / crit.standardDevs.length
            );
            return_criteria[`crit_${crit.criteria.id}`].total_standard_dev +=
              crit.total_standard_dev / crit.standardDevs.length;

            return_criteria[`crit_${crit.criteria.id}`].scoreValues.push(crit.average_score);
            return_criteria[`crit_${crit.criteria.id}`].total_score += crit.average_score;
            return_criteria[`crit_${crit.criteria.id}`].scores.push({
              criteria: crit.criteria,
              score: crit.average_score,
              weight: Number(crit.criteria.weight),
              report: this.allowGroupByReport ? rep.report : null,
              scorer: {
                full_name: rep.report.name,
                initials: rep.report.name.toUpperCase().slice(0, 2),
              },
            });
          }
        }

        // Go through the return criteria, sum up and get averages and stddevs for that report's scores.
        let return_criteria_list = [];
        for (let c_id in return_criteria) {
          let rc = return_criteria[c_id];
          rc.average_score = 0;
          if (rc.scoreValues.length > 0) {
            rc.average_score = rc.total_score / rc.scoreValues.length;
          }
          if (rc.standardDevs.length > 0) {
            rc.stddev = rc.total_standard_dev / rc.standardDevs.length;
          }

          // Build out the return structure: a list of objects with:
          // average_score
          // criteria, a single of ox criteria
          // scoreValues, a list of the actual scores
          // scores, a list of the ox score objects
          // stddev
          // total_score, the sum of the score.
          return_criteria_list.push(rc);
        }
        return_criteria_list.sort((a, b) => {
          if (a.criteria.relative_weight_as_percent == b.criteria.relative_weight_as_percent) {
            return a.criteria.index - b.criteria.index;
          }
          return b.criteria.relative_weight_as_percent - a.criteria.relative_weight_as_percent;
        });
        return return_criteria_list;
      }
    },
  },
  methods: {
    getCriteriaColor(idx) {
      const color_idx = idx % this.chart_colors.length;
      return this.chart_colors[color_idx];
    },
    getNoiseBadgeClass(obj) {
      if (obj.stddev < 1.2) {
        return "low bg-base-200 border-0 text-neutral";
      } else if (obj.stddev > 2.25) {
        return "high badge-error text-error-content";
      }
      if (obj.stddev || obj.stddev == 0) {
        return "medium bg-base-300 border-0 text-neutral";
      } else {
        return "none hidden";
      }
    },
    getNoiseText(score) {
      if (score < 1.2) {
        return "Low";
      } else if (score > 2.25) {
        return "High";
      }
      if (score) {
        return "Medium";
      } else {
        return "";
      }
    },
    toggleIndividualScores() {
      this.showIndividualScorecards = !this.showIndividualScorecards;
      this.sortedCriteria;
    },
    toggleComments() {
      this.open = true;
      this.showComments = !this.showComments;
      this.openCommentRows = {};
    },
    toggleRowComments(score) {
      if (this.openCommentRows[String(score.criteria.id)]) {
        this.openCommentRows[String(score.criteria.id)] = false;
      } else {
        this.openCommentRows[String(score.criteria.id)] = true;
      }
    },
    showRowComments(score) {
      return this.showComments === true || this.openCommentRows[String(score.criteria.id)] === true;
    },
    barClick() {
      if (this.toggleBar) {
        this.toggleOpen();
      }
    },
    toggleOpen() {
      this.open = !this.open;
    },
    toggle(my_bool) {
      my_bool = !my_bool;
      return my_bool;
    },
    noiseTop(sbc) {
      let score_count = {};
      let scores = sbc.scores || [];
      for (let sc of scores) {
        if (score_count[String(sc.score)] != undefined) {
          score_count[String(sc.score)]++;
        } else {
          score_count[String(sc.score)] = 1;
        }
      }
      let max = 0;
      for (let count of Object.values(score_count)) {
        if (count > max) {
          max = count;
        }
      }
      // 8 x + y = 180px
      // 2 x + y = 35px
      // y = 35 - 2x
      // 8x + 35 - 2x = 180
      // 6x = 145
      // x = 24.1
      // 35 - 2(24.1) = y
      // y = -13.2
      return 0;
      // return max * 24.1 + (max > 1 ? -13.2 : 8);
    },
    userColor(user) {
      let seed = String(user?.id);
      if (!seed && user.full_name) {
        seed = user.full_name;
      }
      if (!seed && user.name) {
        seed = user.name;
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

      return colors[user.color_index];
    },
    rowClass(index) {
      // if (this.editing) {
      //   return "bg-base-100";
      // } else {
      if (index % 2) {
        return "bg-base-100";
      } else {
        return "bg-base-200";
      }
      // }
    },
    scoreRowClass(index) {
      let s = this.rowClass(index);
      if (index == 0) {
        s += " rounded-t-md";
      }
      // if (index == this.scorecard.scores.length) {
      //   s += " rounded-b-md";
      // }
      return s;
    },

    sbcHasValidScores(sbc) {
      for (let sc of sbc.scores) {
        if (sc.score && sc.score != null && (Number(sc.score) > 0 || Number(sc.score) === 0)) return true;
      }
      return false;
    },
    roundClass(index) {
      if (index == 0) {
        return "rounded-tl-md";
      }
      if (index >= this.sortedCriteria.length - 1) {
        return "rounded-bl-md";
      }
      return "";
    },
    scoresGroupedByReport(sbc) {
      let reports = {};
      let scores = {};
      for (let score of sbc.scores) {
        if (score.report) {
          let f_pk = sbc.criteria.framework_pk;

          if (!reports[String(score.report.id)]) {
            reports[String(score.report.id)] = {
              report: score.report,
              average_score: score.score,
              scores: [],
            };
          }

          for (let rep_sc of score.report.scorecards) {
            if (rep_sc.framework.id == f_pk) {
              for (let rep_sc_s of rep_sc.scores) {
                if (rep_sc_s.criteria.id == sbc.criteria.id) {
                  if (!scores[rep_sc_s.id]) {
                    scores[rep_sc_s.id] = true;
                    reports[String(score.report.id)].scores.push(rep_sc_s);
                  }
                }
              }
            }
          }
        }
      }
      let reports_list = [];
      for (let r_id in reports) {
        let rep = reports[r_id];
        rep.scores.sort((a, b) => {
          return a.modified_at_ms - b.modified_at_ms;
        });
        reports_list.push(rep);
      }
      reports_list.sort((a, b) => {
        return a.modified_at_ms - b.modified_at_ms;
      });
      return reports_list;
    },
    aggregateHasSkipped(aggregate) {
      // Go through all criteria, see if any are missing scores.
      for (let c of aggregate.scores_by_criteria) {
        let all_skipped = true;
        for (let s of c.scores) {
          if (s.score != null) {
            all_skipped = false;
          }
        }

        if (all_skipped === true) {
          return true;
        }
      }
      return false;
    },
    async queueDownload(target, name) {
      var wasOpen = this.open;
      this.open = true;
      await nextTick();
      var ctx = this;
      this.downloadArea(target, name).then(function () {
        ctx.open = wasOpen;
      });
    },
    setOpen(val) {
      this.open = val;
    },
    getOpen() {
      return this.open;
    },
  },
};
</script>

<style scoped>
td {
  @apply align-middle;
  border: 0;
  padding: 0;
}
td.cell-top {
  @apply align-top;
}
.criteria-list-item {
  min-height: 4em;
}
table {
  height: 1px;
  border: 0;
  border-spacing: 0;
}
tr {
  border: 0;
  padding: 0;
}
td.grow {
  width: 99%;
}
td.shrink {
  width: 1px;
}
</style>
