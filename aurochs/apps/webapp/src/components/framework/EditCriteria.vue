<template>
  <div>
    <ul role="list" class="relative z-0">
      <li v-for="(criteria, idx) in criteriaForms.criterias" :key="criteria.id" class="relative px-4 pr-6 py-1">
        <div class="grid grid-cols-2">
          <div class="flex flex-row">
            <div class="w-5 mr-3 h-full" :style="getCriteriaColor(criteria.index)" />
            <div class="flex flex-col w-full">
              <div class="flex flex-row pt-2">
                <label for="criteria" class="sr-only">{{ criteria.name }}</label>
                <input
                  id="name"
                  v-model="criteria.name"
                  :data-cy="`name-edit-${idx}`"
                  type="text"
                  name="name"
                  class="input input-bordered font-bold w-full input-lg px-4 py-2 h-10 rounded-b-none border-b-none outline-0 focus:outline-0 ring-0 focus:ring-0"
                  placeholder="Criteria Name..."
                  autofocus
                />
              </div>
              <OxTextarea
                id="description"
                v-model="criteria.description"
                :data-cy="`description-edit-${idx}`"
                input-type="textarea"
                class="w-full"
                :classes="'rounded-t-none ring-0 focus:ring-0 outline-0 focus:outline-0'"
                :min-rows="2"
                name="description"
                :placeholder="'Criteria description...'"
              />
            </div>
          </div>
          <div class="flex items-center place-content-between ml-2">
            <OxSlider
              :id="`criteria_${criteria.index}`"
              v-model:score="criteria.weight"
              :data-cy="`criteria-weight-${criteria.index}`"
              :index="criteria.index"
              :min="0"
              :max="10"
              @change="updateCriteria"
            />
            <div
              class="font-bold leading-none rounded-full text-center text-white"
              :style="`${getCriteriaColor(criteria.index)} padding: ${6 + 2 * Math.round(criteria.weight)}px; margin: ${
                20 - 2 * Math.round(criteria.weight)
              }px; line-height: 0.5em; ${
                criteria.weight >= 10 ? 'padding-right: 20px;padding-left: 20px; margin-right:2px;' : ''
              }`"
            >
              {{ Math.round(Number(criteria.weight)) }}
            </div>
            <button
              :data-cy="`delete-criteria-${criteria.index}`"
              type="button"
              role="button"
              class="btn btn-circle btn-ghost btn-error hover:btn-error hover:text-error-content ml-4"
              @click="deleteCriteria(idx)"
            >
              <FontAwesomeIcon :icon="['fad', 'trash-can']" class="h-4 w-4 align-middle" />
            </button>
          </div>
        </div>
      </li>
      <li>
        <button class="btn btn-primary m-4" data-cy="new-criteria" @click="addCriteria">
          <FontAwesomeIcon :icon="['fad', 'plus']" class="h-4 w-4 align-middle mr-2" />
          New Criteria
        </button>
      </li>
    </ul>
    <div v-if="!isDraft" class="flex flex-row justify-end mt-2 mx-5 mb-10">
      <button
        type="button"
        role="button"
        data-cy="cancel-criteria"
        class="btn btn-outline btn-base-300 hover:btn-error mr-2"
        @click="cancel"
      >
        <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-4 w-4 align-middle mr-2" />
        Cancel
      </button>
      <button
        type="button"
        role="button"
        data-cy="save-criteria"
        class="btn btn-success"
        :disabled="saving"
        :class="saving ? 'saving' : ''"
        @click="saveCriteria"
      >
        <FontAwesomeIcon v-if="!saving" :icon="['fad', 'check']" class="mr-2 w-4 h-4 align-middle" />
        <FontAwesomeIcon v-if="saving" :icon="['fad', 'rotate']" class="mr-2 w-4 h-4 align-middle fa-spin" />
        {{ saving ? "Saving..." : "Save" }}
      </button>
    </div>
  </div>
</template>

<script>
import chart_colors from "../../mixins/chart_color";
import { reactive, ref } from "vue";
import OxTextarea from "../common/forms/OxTextarea.vue";
import OxSlider from "../common/forms/OxSlider.vue";

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
    OxSlider,
    OxTextarea,
    FontAwesomeIcon,
  },
  props: {
    criteriaList: {
      type: Array,
      required: true,
    },
    saving: {
      type: Boolean,
      default: false,
    },
    isDraft: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["updateCriteria", "saveCriteria", "cancel"],
  setup() {
    const criteriaForms = reactive({ criterias: [] });
    const criteriaCopy = ref([]);
    return {
      criteriaForms,
      criteriaCopy,
      chart_colors,
    };
  },
  mounted() {
    const copy = JSON.parse(JSON.stringify(this.criteriaList));
    this.criteriaCopy = [...copy];
    this.criteriaForms.criterias = [...this.criteriaList];
    if (this.criteriaForms.criterias.length === 0) {
      this.criteriaForms.criterias.push({
        name: "",
        description: "",
        weight: "5",
        index: this.criteriaForms.criterias.length,
      });
    }
    this.updateCriteria();
  },
  methods: {
    updateCriteria() {
      this.$emit("updateCriteria", [...this.criteriaForms.criterias]);
    },
    getCriteriaColor(idx) {
      const color_idx = idx % this.chart_colors.length;
      return `background-color: ${this.chart_colors[color_idx]};`;
    },
    saveCriteria() {
      this.$emit("saveCriteria", { ...this.criteriaForms });
    },
    addCriteria() {
      let lastIndex = 0;
      for (let c of this.criteriaForms.criterias) {
        if ((c.index || c.index === 0) && c.index > lastIndex) {
          lastIndex = c.index;
        }
      }

      this.criteriaForms.criterias.push({
        name: "",
        description: "",
        weight: "5",
        index: lastIndex + 1,
      });
      this.updateCriteria();
    },
    deleteCriteria(idx) {
      this.criteriaForms.criterias.splice(idx, 1);
      // for (let i = idx; i < this.criteriaForms.criterias.length; i++) {
      //   this.criteriaForms.criterias[i].index--;
      // }
      this.updateCriteria();
    },
    cancel() {
      this.criteriaForms = { criterias: [...this.criteriaCopy] };
      this.$emit("cancel", this.criteriaCopy);
    },
    updateFromSource() {
      const copy = JSON.parse(JSON.stringify(this.criteriaList));
      this.criteriaCopy = [...copy];
      this.criteriaForms.criterias = [...this.criteriaList];
      if (this.criteriaForms.criterias.length === 0) {
        this.criteriaForms.criterias.push({
          name: "",
          description: "",
          weight: "5",
          index: this.criteriaForms.criterias.length,
        });
      }
      this.updateCriteria();
    },
  },
};
</script>
<style scoped>
ul[role="list"] {
  list-style: none !important;
  padding-left: 0 !important;
}
</style>
