<template>
  <div
    class="flex flex-row place-content-stretch space-x-4 criteria-list-item h-full"
    :class="(bg ? bg : idx ? (idx % 2 ? '' : 'bg-base-200') : 'bg-base-200') + (showImportance ? ' pl-2' : '')"
    :data-cy="`framework-criteria-card-${idx}`"
  >
    <div
      v-if="!showImportance"
      class="flex flex-col items-center justify-center w-5"
      :style="criteriaColor"
      :class="roundClass"
    />
    <div v-if="showImportance" class="flex items-center place-content-center">
      <div
        data-cy="weight"
        class="font-bold leading-none rounded-full text-center"
        :style="`${criteriaColor} padding: ${6 + 2 * Math.round(criteria.weight)}px; margin: ${
          20 - 2 * Math.round(criteria.weight)
        }px; line-height: 0.5em; ${
          criteria.weight >= 10 ? 'padding-right: 20px;padding-left: 20px; margin-right:2px;' : ''
        }; font-size:${criteria.weight / 16 + 0.8}em;`"
      >
        {{ Math.round(Number(criteria.weight)) }}
      </div>
    </div>
    <div class="flex flex-col w-full p-2 place-content-center">
      <div :class="twoLines && thin ? 'h-14 overflow-hidden flex flex-col place-content-center' : ''">
        <span class="text-lg font-bold max-h-14" data-cy="name">{{ criteria.name }}</span>
      </div>
      <p
        v-if="!thin"
        data-cy="description"
        class="block my-0 text-base"
        :class="thin ? ' ellipsis h-6 text-ellipsis overflow-hidden ' : ' text-linebreaks '"
      >
        {{ thin ? criteria.description.slice(0, 42) + "..." : criteria.description }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import chart_colors from "../../mixins/chart_color";
export default {
  props: {
    criteria: {
      type: Object,
      required: true,
    },
    idx: {
      type: Number,
      required: true,
    },
    editing: {
      type: Boolean,
      default: false,
    },
    showImportance: {
      type: Boolean,
      default: true,
    },
    twoLines: {
      type: Boolean,
      default: true,
    },
    thin: {
      type: Boolean,
      default: false,
    },
    bg: {
      type: String,
      default: "",
    },
    roundClass: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    const formData = ref({});
    const editMode = ref(false);
    const criteriaName = ref(props.criteria.name);
    const criteriaDescription = ref(props.criteria.description);
    return {
      formData,
      chart_colors,
      editMode,
      criteriaName,
      criteriaDescription,
    };
  },
  computed: {
    criteriaColor() {
      const color_idx = this.criteria.index;
      return `background-color: ${this.chart_colors[color_idx]}; color:#FFF; `;
    },
  },
};
</script>

<style scoped>
.edit-btn {
  @apply inline-flex items-center px-3 border border-transparent hover:shadow-sm text-sm leading-4 font-medium   focus:outline-none;
}
</style>
