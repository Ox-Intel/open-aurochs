<template>
  <div v-for="frameworkAggregate in scorecardsByFramework" :key="frameworkAggregate.framework.id">
    <AllScorecardsScorecard :framework-aggregate="frameworkAggregate" />
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import AllScorecardsScorecard from "./AllScorecardsScorecard.vue";
import formatDate from "../../mixins/format_date";
import trimNumber from "../../mixins/trim_number";
import chart_colors from "../../mixins/chart_color";

export default {
  components: {
    AllScorecardsScorecard,
  },
  mixins: [formatDate, trimNumber],
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    scorecardsByFramework: {
      type: Object,
      default: () => {},
    },
  },
  emits: ["createRecord"],
  setup() {
    var showComments = ref(true);

    return {
      showComments,
      chart_colors,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    userId() {
      return this.user.id;
    },
  },
  methods: {
    createRecord() {
      this.$emit("createRecord");
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
.criteria-list-item {
  width: 30vw;
}
.card-body {
  @apply overflow-x-auto;
  max-width: 85vw;
}
.comments {
  width: 400px;
}
.toggle-comments-btn {
  @apply mt-2;
  left: 73vw;
}
th {
  @apply align-top pt-4;
}
.oxScore {
  @apply text-primary-content rounded h-12 w-12 p-3 text-2xl ml-2 pt-1 align-bottom;
}
.oxScore .label {
  @apply uppercase -mt-5 -ml-3;
  font-size: 0.5rem;
}
</style>
