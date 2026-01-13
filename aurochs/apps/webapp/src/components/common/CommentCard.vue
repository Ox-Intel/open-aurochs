<template>
  <div class="card mb-4 w-full" data-cy="comment">
    <div class="card-body">
      <div class="flex">
        <div div class="flex mt-4">
          <OxAvatar :user="comment_obj.user" class="mr-2" />
          <div class="w-36">
            <div class="font-bold -mb-2">
              {{ comment_obj.user.full_name }}
            </div>
            <div>{{ formatDate(comment_obj.modified_at_ms) }}</div>
            <div v-if="comment_obj.edited" class="badge badge-accent">Edited</div>
          </div>
        </div>
        <div class="ml-8 p-4 text-linebreaks bg-base-200 grow max-width-prose break-words relative rounded-lg">
          <div v-if="!editing" data-cy="body">
            {{ comment_obj.body }}
          </div>
          <div v-if="editing">
            <OxTextarea
              v-model="body"
              data_cy="new-comment"
              placeholder="Add your comment..."
              input-type="textarea"
              label=""
              size="lg"
            />
            <div class="flex justify-end">
              <!-- justify-between?  -->
              <button
                v-if="!add"
                data-cy="cancel"
                type="button"
                role="button"
                class="btn btn-outline btn-error mr-2"
                @click="cancel"
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
                @click="saveComment"
              >
                <FontAwesomeIcon
                  v-if="!add && !saving"
                  :icon="['fad', 'check']"
                  class="h-4 w-4 mr-2"
                  aria-hidden="true"
                />
                <FontAwesomeIcon
                  v-if="add && !saving"
                  :icon="['fad', 'plus']"
                  class="h-4 w-4 mr-2"
                  aria-hidden="true"
                />
                {{ saveButtonText }}
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="text-right align-right">
        <div
          v-if="!add && !editing && user.id == comment_obj.user.id"
          data-cy="edit-comment"
          role="button"
          class="btn btn-circle btn-sm text-center btn-primary btn-ghost hover:btn-outline"
          @click="startEditing"
        >
          <FontAwesomeIcon :icon="['fad', 'pen']" class="align-middle h-4 w-4" />
        </div>
        <div
          v-if="!add && !editing && user.id == comment_obj.user.id"
          data-cy="delete-comment"
          role="button"
          class="btn btn-circle btn-sm ml-1 text-center btn-error btn-ghost hover:btn-outline mt-2"
          @click="deleteComment"
        >
          <FontAwesomeIcon :icon="['fad', 'trash-can']" class="align-middle h-4 w-4" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import OxTextarea from "../common/forms/OxTextarea.vue";
import OxAvatar from "../common/OxAvatar.vue";
import { ref } from "vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";

library.add(faTrashCan, faPen, faPlus, faXmark, faCheck, faPlus);

export default {
  components: {
    OxTextarea,
    OxAvatar,
    FontAwesomeIcon,
  },
  mixins: [formatDate],
  props: {
    comment: {
      type: Object,
      default: () => {},
    },
    target: {
      type: Object,
      default: () => {},
    },
    add: {
      type: Boolean,
      default: () => false,
    },
  },
  setup(props) {
    var editing;
    var body_text;

    const saving = ref(false);

    if (props.add) {
      editing = ref(true);
      body_text = ref("");
    } else {
      editing = ref(false);
      body_text = props.comment.body + "";
    }
    return {
      aurochsData: useAurochsData(),
      editing,
      body: ref(body_text),
      saving,
    };
  },
  computed: {
    user() {
      return this.aurochsData.user;
    },
    comment_obj() {
      if (this.add) {
        return {
          user: this.user,
          body: this.body,
          edited: false,
          modified_at_ms: new Date(),
        };
      } else {
        return this.comment;
      }
    },
    saveButtonText() {
      if (this.add) {
        if (this.saving) {
          return "Saving...";
        } else {
          return "Add Comment";
        }
      } else {
        if (this.saving) {
          return "Updating...";
        } else {
          return "Update";
        }
      }
    },
  },
  methods: {
    startEditing() {
      this.editing = true;
    },
    cancel() {
      // this.body = this.comment.body + "";
      this.editing = false;
    },
    async saveComment() {
      this.saving = true;
      if (this.add) {
        const data = {
          object_type: this.target["__type"],
          id: this.target.id,
          body: this.body + "",
        };
        await this.$sendEvent("add_comment", data);
        this.body = "";
      } else {
        const data = {
          id: this.comment.id,
          body: this.body,
        };
        await this.$sendEvent("update_comment", data);
        this.editing = false;
      }
      this.saving = false;
    },
    async deleteComment() {
      if (confirm("Are you sure you want to delete this comment?")) {
        const data = {
          id: this.comment.id,
        };
        await this.$sendEvent("delete_comment", data);
      }
    },
  },
};
</script>
