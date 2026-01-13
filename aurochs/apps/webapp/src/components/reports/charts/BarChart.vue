<template>
  <div class="chart w-full h-full">
    <div class="block relative h-full w-full">
      <div
        :class="greyIfEmpty && isEmpty ? 'bg-medium-grey' : ''"
        class="block absolute left-0 top-0 h-full z-5"
        :style="`width: ${barWidth}%;` + (greyIfEmpty && isEmpty ? '' : `background-color: ${color};`)"
      />
      <div
        class="block absolute left-0 top-0 h-full z-10"
        :style="`width: ${scores_by_criteria.criteria.relative_weight_as_percent_of_max}%; opacity: 0.3; border-right: 1px solid ${color}; background: ${color};`"
      />
    </div>
  </div>
</template>

<script>
export default {
  props: {
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
      type: String,
      default: "0",
    },
    userScoresData: {
      type: Array,
      default: () => [3],
    },
    greyIfEmpty: {
      type: Boolean,
    },
  },
  computed: {
    barWidth() {
      let avg =
        (Number(this.scores_by_criteria.criteria.relative_weight_as_percent_of_max) / 100) *
        10 *
        Number(this.scores_by_criteria.average_score);
      if (avg > 0) {
        return avg;
      }
      return 0.75;
    },
    isEmpty() {
      for (let sc of this.scores_by_criteria.scores) {
        if (sc.score && sc.score != null && (Number(sc.score) > 0 || Number(sc.score) === 0)) return false;
      }
      return true;
    },
  },
  methods: {},
};
</script>
<style scoped></style>
