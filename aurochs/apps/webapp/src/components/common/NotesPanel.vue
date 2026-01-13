<template>
  <article ref="notespanel" class="prose px-4 max-w-screen-lg" :data-show-bottom-buttons="showBottomButtons">
    <div
      v-if="canEditNotes && !notesIsBlank && !editing"
      data-cy="edit-notes"
      role="button"
      class="btn text-center btn-primary align-middle float-right -mr-24"
      @click="startEditing"
    >
      <FontAwesomeIcon :icon="['fad', 'pen']" class="align-middle h-4 w-4 mr-2" />
      Edit Notes
    </div>
    <div
      v-if="!editing"
      class="text-md font-weight-thin prose-p my-6 pr-4 relative"
      :class="notesIsBlank ? '' : 'border-l-2 border-base-500'"
    >
      <div v-if="notesIsBlank">
        <div class="card card-bordered bg-base-200 max-w-screen-md ml-4">
          <div class="card-body w-full">
            <div class="flex">
              <div class="w-12 text-center">
                <FontAwesomeIcon :icon="['fad', 'memo-pad']" class="h-12 w-12 text-base-500" />
              </div>
              <div class="grow text-left px-4 pt-2 flex justify-between">
                <div class="text-xl text-base-500">No notes yet.</div>
                <label
                  v-if="canEditNotes"
                  class="btn btn-primary -mt-2"
                  role="button"
                  data-cy="add-notes"
                  @click="startEditing"
                >
                  <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                  Add Notes
                </label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="!notesIsBlank" data-cy="view-notes">
        <OxViewRichTextarea :content="notes" :classes="'w-full'" :size="'md'" />
      </div>
    </div>

    <div
      v-if="!editing && target?.__type == 'report' && (feedback_comment || feedback_score)"
      class="p-8 bg-base-200 my-8 rounded"
    >
      <h2 class="mt-0">Report Outcome</h2>
      <div class="">
        <p class="whitespace-nowrap">
          <b>Outcome Score: {{ feedback_score != null ? Math.round(feedback_score) + "%" : "Not set." }}</b>
        </p>
        <div class="font-bold mt-4">Outcome Comments</div>
        <OxViewRichTextarea :content="feedback_comment" :classes="'w-full'" :size="'md'" />
      </div>
    </div>

    <div v-if="editing" class="w-full border-l-1 border-base-500" data-cy="editing-notes">
      <OxRichTextarea
        v-model="notes"
        :target="target"
        placeholder=""
        input-type="textarea"
        :classes="'w-full'"
        :size="'md'"
      />

      <div v-if="target?.__type == 'report'" class="p-8 bg-base-200 my-8 rounded">
        <h2 class="mt-0">Report Outcome</h2>
        <div class="">
          <div class="font-bold">Outcome Score (0-100)</div>
          <div class="flex w-96">
            <OxSlider :id="'outcome_score'" v-model:score="feedback_score" :min="0" :max="100" />
            <div class="ml-4 font-bold whitespace-nowrap">
              {{ feedback_score != null ? feedback_score : "Not set." }}
            </div>
            <div class="btn btn-outline btn-sm ml-16" @click="clearFeedbackScore()">Clear</div>
          </div>
          <div class="font-bold mt-4">Outcome Comments</div>
          <OxRichTextarea v-model="feedback_comment" :target="target" :classes="'w-full'" :size="'md'" />
        </div>
      </div>
      <div v-if="showBottomButtons" class="flex justify-end mt-4">
        <!-- justify-between?  -->
        <button
          data-cy="cancel"
          type="button"
          role="button"
          class="btn btn-outline btn-error mr-2"
          @click="stopEditing"
        >
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-4 w-4" />
          Cancel
        </button>
        <button
          data-cy="save-comment"
          type="button"
          role="button"
          class="btn btn-success"
          :class="saving ? 'saving' : ''"
          :disabled="saving"
          @click="saveObject"
        >
          <FontAwesomeIcon v-if="!saving" :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
          Save Notes
        </button>
      </div>
    </div>
  </article>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import OxSlider from "../common/forms/OxSlider.vue";
import OxRichTextarea from "../common/forms/OxRichTextarea.vue";
import OxViewRichTextarea from "../common/forms/OxViewRichTextarea.vue";
import { checkCanEdit, checkCanManage } from "../../mixins/permissions.js";
// import OxAvatar from "./OxAvatar.vue";
import { ref } from "vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faMessage } from "@fortawesome/pro-duotone-svg-icons/faMessage";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faBell } from "@fortawesome/pro-duotone-svg-icons/faBell";
import { faBellPlus } from "@fortawesome/pro-duotone-svg-icons/faBellPlus";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faBellSlash } from "@fortawesome/pro-duotone-svg-icons/faBellSlash";

library.add(faMessage, faTrashCan, faBell, faBellPlus, faPen, faBellSlash);

export default {
  components: {
    FontAwesomeIcon,
    OxSlider,
    OxRichTextarea,
    OxViewRichTextarea,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
  },
  setup(props) {
    const editing = ref(false);
    const saving = ref(false);
    const notes = ref(props.target?.notes);
    const feedback_comment = ref(props.target?.feedback_comment);
    const feedback_score = ref(props.target?.feedback_score);
    return {
      aurochsData: useAurochsData(),
      editing,
      saving,
      notes,
      feedback_comment,
      feedback_score,
    };
  },
  computed: {
    notesIsBlank() {
      return !this.notes || this.notes == "{ops:[{insert:'\\n'}]}" || this.notes == { ops: [{ insert: "\\n" }] };
    },
    showBottomButtons() {
      // if (this.$refs?.notespanel) {
      // console.log(this)
      // console.log(this.$refs);
      // console.log(this.$refs?.notespanel);
      // console.log(this.$refs?.notespanel?.scrollHeight);
      this.$refs;
      this.$refs?.notespanel;
      this.$refs?.notespanel?.scrollHeight;
      // console.log(window.innerHeight)
      // return this.$refs?.notespanel?.scrollHeight > window.innerHeight - 200;
      // }
      return true;
    },
    canEditNotes() {
      return checkCanEdit(this.target, this.aurochsData.user) || checkCanManage(this.target, this.aurochsData.user);
    },
  },
  watch: {
    target: {
      deep: true,
      handler: function (newVal) {
        if (newVal) {
          this.notes = newVal.notes;
          this.feedback_comment = newVal.feedback_comment;
          this.feedback_score = newVal.feedback_score;
        }
      },
    },
  },
  mounted() {
    // this.$pollTimeout = setTimeout(this.pollUpdates, 10000);

    // this.notes = this.target?.notes;

    if (this.target?.__type == "report") {
      this.feedback_score = this.target?.feedback_score;
      this.feedback_comment = this.target?.feedback_comment;
    }
  },
  beforeUnmount() {
    // clearTimeout(this.$pollTimeout);
  },
  methods: {
    async saveObject() {
      this.saving = true;
      let data = {
        id: this.target.id,
        notes: this.notes,
      };
      if (this.target.__type == "report") {
        data["feedback_score"] = this.feedback_score;

        if (this.feedback_comment == "{ops:[{insert:'\\n'}]}") {
          data["feedback_comment"] = null;
        } else {
          data["feedback_comment"] = this.feedback_comment;
        }
      }
      await this.$sendEvent(`update_${this.target.__type}`, data);
      this.saving = false;
      this.stopEditing();
    },
    startEditing() {
      this.editing = true;
    },
    stopEditing() {
      this.editing = false;
    },
    clearFeedbackScore() {
      this.feedback_score = null;
    },
  },
};
</script>

<style scoped>
.comment_block {
  max-width: 65vw;
}

.ql-toolbar.ql-snow {
  @apply rounded-t-md shadow-sm;
}

.ql-container.ql-snow {
  @apply rounded-b-md;
}
</style>
