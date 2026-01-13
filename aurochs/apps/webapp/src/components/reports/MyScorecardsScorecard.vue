<template>
  <div ref="scorecard" data-cy="scorecard">
    <div class="card-body" :data-cy="`scorecard-${data_cy_idx}`">
      <div class="card-title">
        <div class="flex flex-row w-full">
          <div class="grow flex cursor-pointer" @click="toggleOpen">
            <!-- 
          <OxScoreBox
            :oxScore="Number(scorecard.ox_score)"
            :has-skipped="scorecard?.has_skipped"
          /> 
          <div class="px-2"></div>
          -->
            <div class="h-12 w-12 mt-2 pt-0.5 mr-3">
              <OxChartIcon
                :chart_id="`activity_icon_${scorecard.framework?.id}`"
                :criteria="scorecard.framework?.criteria"
                :small="false"
                class="h-12 w-12 translate-y-0 translate-x-0"
              />
            </div>
            <!-- <OxAvatar :user="scorecard.scorer" class="align-middle mt-3 mr-2 text-sm" :small="false" /> -->
            <div>
              <div class="ml-2">
                <span class="mr-2 font-bold text-xl">{{ scorecard.scorer.full_name }}</span>
                <!-- - -->
                <span class="font-light text-base text-dark-grey">{{ formatDate(scorecard.modified_at_ms) }}</span>
              </div>
              <router-link
                :to="`/framework/${scorecard.framework?.id}`"
                class="ml-2 mt-2 font-light text-xl align-middle no-underline"
              >
                {{ scorecard.framework?.name }}
              </router-link>
            </div>
          </div>
          <div class="flex place-content-center">
            <div v-if="showAlert" class="alert alert-success shadow-lg -mt-4">
              <div>
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6 mr-2 text-success-content align-middle" />
                <span>Scorecard added.</span>
              </div>
            </div>
          </div>
          <div v-if="!editing" class="flex-none w-4- flex mr-2 hiddenInExport">
            <div role="button" data-cy="toggle-open" class="btn btn-ghost hover:bg-base-100 ml-4" @click="toggleOpen()">
              <div v-if="!open" data-cy="toggle-open-expand">
                <FontAwesomeIcon :icon="['fad', 'chevron-down']" class="h-4 w-4 inline" />
                Expand
              </div>
              <div v-else data-cy="toggle-open-collapse">
                <FontAwesomeIcon :icon="['fad', 'chevron-up']" class="h-4 w-4 inline" />
                Collapse
              </div>
            </div>
          </div>
          <div class="dropdown dropdown-end">
            <DownloadButton
              class="btn btn-ghost btn-border-base-200 mr-2 -ml-2 removedInExport"
              data-cy="download-report"
              type="button"
              role="button"
              title="Download Scorecard"
              tabindex="40"
            />
            <ul
              tabindex="0"
              class="dropdown-content menu p-2 mt-0 shadow-md bg-base-100 rounded-box w-auto whitespace-nowrap text-sm font-normal removedInExport"
            >
              <li>
                <a href="#" class="no-underline" @click.stop.prevent="downloadPDF()">
                  <FontAwesomeIcon :icon="['fad', 'file-pdf']" class="mr-2 w-8 h-8" />
                  Download PDF
                </a>
              </li>
              <li>
                <a
                  href="#"
                  class="no-underline"
                  @click.stop.prevent="
                    queueDownload(
                      $refs.scorecard,
                      `${report.name} - ${scorecard.framework.name} - ${scorecard.scorer.full_name}`
                    )
                  "
                >
                  <FontAwesomeIcon :icon="['fad', 'file-powerpoint']" class="mr-2 w-8 h-8" />
                  Download Image (PNG)
                </a>
              </li>
            </ul>
          </div>

          <div
            v-if="!editing && canScore && scorecard.scorer.id == aurochsData.user.id"
            data-cy="edit-scorecard"
            role="button"
            class="btn btn-outline btn-primary whitespace-nowrap mr-2 hiddenInExport"
            @click.stop.prevent="startEdit()"
          >
            <FontAwesomeIcon :icon="['fad', 'pen']" class="align-middle h-4 w-4 mr-2" />
            Edit
          </div>
          <div
            v-if="!editing && (canManage || scorecard.scorer.id == aurochsData.user.id)"
            role="button"
            class="btn btn-outline btn-error whitespace-nowrap mr-2 hiddenInExport"
            data-cy="delete-scorecard"
            @click.stop.prevent="deleteScorecard()"
          >
            <FontAwesomeIcon :icon="['fad', 'trash-can']" class="align-middle h-4 w-4 mr-2" />
            Delete
          </div>
          <OxScoreBox v-if="!editing" :ox-score="Number(scorecard.ox_score)" :has-skipped="scorecard?.has_skipped" />
        </div>
      </div>
      <div v-if="!editing && !open" class="mt-4" data-cy="view-scores">
        <div class="w-full">
          <div v-for="(score, score_idx) in scorecard.scores" :key="score_idx" class="h-12">
            <div class="font-bold text-sm">{{ score.criteria.name }}</div>
            <div class="full_bar relative">
              <div
                v-if="score.skipped"
                class="absolute z-20 w-full px-4 py-2 pt-0 bg-base-200 text-neutral opacity-75 text-sm"
              >
                Skipped
              </div>
              <div
                class="absolute left-0 h-4 bg-bar opacity-25"
                :style="`width: ${score.criteria.weight * 10}%; background-color: var(--criteria-color-${
                  score_idx + 1
                });`"
              ></div>
              <div
                :class="'absolute left-0 bar h-4 z-10'"
                :style="`width: ${score.score * score.criteria.weight}%; background-color: var(--criteria-color-${
                  score_idx + 1
                });`"
              >
                <div
                  v-if="score.gpt_scored_last"
                  class="absolute bottom-0 right-0 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs"
                  style="font-size: 0.6rem"
                >
                  AI
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!editing && open" class="mt-4" data-cy="view-scores">
        <div class="w-full">
          <div v-for="(score, score_idx) in scorecard.scores" :key="score_idx">
            <div class="font-bold text-sm">{{ score.criteria.name }}</div>
            <div class="full_bar relative">
              <div
                v-if="score.skipped"
                class="absolute z-20 w-full px-4 py-2 pt-0 bg-base-200 text-neutral opacity-75 text-sm"
              >
                Skipped
              </div>
              <div
                class="absolute left-0 h-4 bg-bar opacity-25"
                :style="`width: ${score.criteria.weight * 10}%; background-color: var(--criteria-color-${
                  score_idx + 1
                });`"
              ></div>
              <!--  ${
                  score.gpt_scored_last ? 'bg-ox-score text-ox-score-content' : ''
                }` -->
              <div
                :class="`absolute left-0 bar h-4 z-10`"
                :style="`width: ${score.score * score.criteria.weight}%; background-color: var(--criteria-color-${
                  score_idx + 1
                });`"
              >
                <div
                  v-if="score.gpt_scored_last"
                  class="absolute bottom-0 right-0 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs"
                  style="font-size: 0.6rem"
                >
                  AI
                </div>
              </div>
              <!-- (!score.gpt_scored_last ? `background-color: var(--criteria-color-${score_idx + 1});` : '') -->
            </div>
            <div class="flex w-full my-4 mt-6">
              <div class="grow text-sm mr-12">
                {{ score.comment ? score.comment : "No comments" }}
                <!-- <div v-if="score.gpt_scored_last" class="inline-block w-4 h-4 bg-ox-score text-center text-ox-score-content text-xs " style="font-size: 0.6rem">AI</div> -->
              </div>
              <div class="w-16 max-w-16 flex justify-end -mt-2">
                <div
                  :class="
                    ' w-12 h-12 rounded relative block pt-2 mt-1 font-bold text-2xl text-center text-success-content ' +
                    (score.skipped ? 'bg-base-500 text-medium-grey' : '')
                  "
                  :style="score.skipped ? '' : `background-color: var(--criteria-color-${score_idx + 1});`"
                >
                  {{ score.skipped ? "–" : Math.round(score.score) }}
                  <div
                    v-if="score.gpt_scored_last"
                    class="absolute -bottom-1 -right-1 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs"
                    style="font-size: 0.6rem"
                  >
                    AI
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="editing" class="mt-4" data-cy="edit-scores">
        <div v-for="(score, score_idx) in editingScores" :key="score_idx" :class="'p-6 '">
          <div class="font-bold">{{ score.criteria.name }}</div>
          <div class="text-xs">{{ score.criteria.description }}</div>
          <div
            class="relative cursor-pointer"
            @click="
              if (score.skipped) {
                score.skipped = false;
              }
            "
          >
            <div
              v-if="score.skipped"
              class="absolute inset-x-1/2 w-32 px-4 py-2 pt-1 bg-base-200 border-neutral text-center font-bold opacity-75 text-neutral text-sm cursor-pointer"
            >
              Skipped
            </div>
            <OxSlider
              v-model:score="score.score"
              v-model:oxgptScoredLast="score.gpt_scored_last"
              :min="0"
              :max="10"
              :enable-ox-scoring="true"
              :disabled="score.skipped === true"
            />
          </div>
          <div class="flex w-full justify-between gap-4">
            <div class="grow">
              <OxTextarea
                v-model="score.comment"
                placeholder="Score explanation and comments."
                input-type="textarea"
                :classes="`w-full bg-base-100 text-sm mt-2 border-1`"
              />
            </div>

            <div class="flex gap-4">
              <div
                class="btn btn-sm bd-base-500 text-base-500 mt-2 w-16 text-center btn-base-300 btn-outline"
                @click="toggleSkipped(score)"
              >
                {{ score.skipped ? "Unskip" : "Skip" }}
              </div>
              <div
                class="btn btn-sm bd-base-500 text-base-500 mt-2 btn-base-300 btn-outline"
                @click="
                  score.score = 0;
                  score.comment = '';
                  score.skipped = false;
                "
              >
                Clear
              </div>
              <div
                :class="
                  'w-10 h-10 rounded relative block pt-1 mt-1 font-bold text-2xl text-center text-success-content ' +
                  (score.skipped ? 'bg-base-500 text-medium-grey' : '')
                "
                :style="score.skipped ? '' : `background-color: var(--criteria-color-${score_idx + 1});`"
              >
                {{ score.skipped ? "–" : Math.round(score.score) }}
                <div
                  v-if="score.gpt_scored_last"
                  class="absolute -bottom-1 -right-1 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs"
                  style="font-size: 0.6rem"
                >
                  AI
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="!isDraft" class="flex flex-row justify-end mt-2 mx-5 mb-10">
          <button type="button" role="button" class="btn btn-outline btn-error mr-2 removedInExport" @click="cancel">
            <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-4 w-4 mr-2 align-middle" />
            Cancel
          </button>
          <button
            data-cy="save-scorecard"
            type="button"
            role="button"
            class="btn btn-success removedInExport"
            :disabled="saving"
            :class="saving ? 'saving' : ''"
            @click="saveScorecard"
          >
            <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2 align-middle" />
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, nextTick } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import OxScoreBox from "../common/OxScoreBox.vue";
import OxChartIcon from "../common/icons/OxChartIcon.vue";
import OxSlider from "../common/forms/OxSlider.vue";
import OxTextarea from "../common/forms/OxTextarea.vue";
// import OxAvatar from "../../components/common/OxAvatar.vue";
import { checkCanScore, checkCanManage } from "../../mixins/permissions.js";
import DownloadButton from "../common/DownloadButton.vue";
import downloadArea from "../../mixins/download_area";
import DownloadMixin from "../../mixins/download_file";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faChevronDown } from "@fortawesome/pro-duotone-svg-icons/faChevronDown";
import { faChevronUp } from "@fortawesome/pro-duotone-svg-icons/faChevronUp";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";

library.add(faChevronDown, faChevronUp, faPen, faCheck, faXmark, faTrashCan);

export default {
  components: {
    OxScoreBox,
    OxChartIcon,
    OxSlider,
    OxTextarea,
    FontAwesomeIcon,
    DownloadButton,
    // OxAvatar,
  },
  mixins: [formatDate, downloadArea, DownloadMixin],
  props: {
    scorecard: {
      type: Object,
      default: () => {},
    },
    report: {
      type: Object,
      default: () => {},
    },
    mine: {
      type: Boolean,
      default: () => false,
    },
    dataCy: {
      type: String,
      default: () => "",
    },
    sc_idx: {
      type: String,
      default: () => "",
    },
    data_cy_idx: {
      type: String,
      default: () => "",
    },
    isOpen: {
      type: Boolean,
      default: () => false,
    },
    isDraft: {
      type: Boolean,
      default: () => false,
    },
  },
  setup(props) {
    const aurochsData = useAurochsData();
    const open = ref(props.isOpen || false);
    const saving = ref(false);
    const actions_taken = ref(false);
    let is_new = true;
    if (
      props.scorecard?.modified_at_ms - props.scorecard?.created_at_ms > 10000 ||
      props.scorecard?.scorer?.id != aurochsData.user.id
    ) {
      is_new = false;
    }
    for (let s_index in props.scorecard.scores) {
      if (props.scorecard.scores[s_index].score != null || props.scorecard.scores[s_index].comment != null) {
        is_new = false;
      }
    }
    // this.editing = is_new
    const editing = ref(is_new || props.isDraft);
    const editingScores = ref([]);

    return {
      aurochsData: ref(aurochsData),
      open,
      editing,
      is_new,
      saving,
      actions_taken,
      editingScores,
    };
  },
  computed: {
    showAlert() {
      return this.scorecard.editing && !this.actions_taken;
    },
    canScore() {
      return this.isDraft || checkCanScore(this.report, this.aurochsData.user);
    },
    canManage() {
      return this.isDraft || checkCanManage(this.report, this.aurochsData.user);
    },
    dataHasChanged() {
      for (var i in this.editingScores) {
        var sc = this.editingScores[i];
        if (sc.comment != this.scorecard.scores[i].comment) {
          return true;
        }
        if (Number(sc.score) != Number(this.scorecard.scores[i].score)) {
          return true;
        }
      }
      return false;
    },
  },
  mounted() {
    if (this.editing) {
      this.startEdit();
    }
  },
  methods: {
    toggleOpen() {
      this.open = !this.open;
      this.actions_taken = true;
    },
    startEdit() {
      this.editing = true;
      this.actions_taken = true;
      let newScores = [];
      for (let s_index in this.scorecard.scores) {
        let sc = this.scorecard.scores[s_index];
        sc.skipped = !this.is_new && sc.score === null;
        if (!sc.score) {
          sc.score = 0;
        }
        sc.score = Number(sc.score);
        newScores.push({
          ...sc,
        });
      }
      this.editingScores = newScores;
    },
    async saveScorecard() {
      this.saving = true;
      this.actions_taken = true;
      this.is_new = false;
      var data = {
        id: this.scorecard.id,
        scores: [],
      };

      for (var sc_index in this.editingScores) {
        var scs = this.editingScores[sc_index];
        let score = scs.skipped ? null : scs.score;
        data.scores.push({
          id: scs.id,
          score: score,
          comment: scs.comment,
          gpt_scored_last: scs.gpt_scored_last,
        });
      }
      await this.$sendEvent("update_scorecard", data);
      this.editing = false;
      this.saving = false;
      this.open = true;
    },
    cancel() {
      if (this.dataHasChanged) {
        if (
          window.confirm(
            "Do you want to discard your changes to this scorecard?\n\nPress OK to discard.\nPress Cancel to continue editing."
          )
        ) {
          this.editing = false;
          this.saving = false;
          this.actions_taken = true;
          this.editingScores = [];
        }
      } else {
        this.editing = false;
        this.saving = false;
        this.actions_taken = true;
        this.open = true;
      }
    },
    async deleteScorecard() {
      if (window.confirm("Are you sure you want to delete this scorecard?")) {
        var data = {
          id: this.scorecard.id,
        };
        await this.$sendEvent("delete_scorecard", data);
      }
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
      if (index == this.scorecard.scores.length) {
        s += " rounded-b-md";
      }
      return s;
    },
    roundClass(index) {
      if (index == 0) {
        return "rounded-tl-md";
      }
      if (index >= this.scorecard.scores.length - 1) {
        return "rounded-bl-md";
      }
      return "";
    },
    isSkipped(sc) {
      return sc.skipped;
    },
    toggleSkipped(sc) {
      sc.skipped = !sc.skipped;
      // if (this.isSkipped(sc)) {
      //   sc.score = 5;
      // } else {
      //   sc.score = null;
      // }
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
    async downloadPDF() {
      this.saving = true;
      let data = {
        scorecardId: this.scorecard.id,
      };

      this.downloadFile(
        "/export/scorecard/pdf/" + this.scorecard.id + "/",
        "Ox Scorecard - " +
          this.scorecard.scorer.full_name +
          " - " +
          this.report.name +
          " - " +
          this.scorecard.framework.name,
        ".pdf",
        data
      ).then(() => {
        this.saving = false;
      });
    },
  },
};
</script>
