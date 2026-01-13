<template>
  <div class="pb-6 sm:pb-16">
    <div class="relative max-w-lg mx-auto px-4 sm:px-6 lg:px-8">
      <dl class="p-4 text-base">
        <div class="grid grid-cols-2 px-2">
          <div class="">Average Ox Score</div>
          <div class="ox-stat">{{ avgOxScore }}%<span v-if="has_skipped" class="-mr-6"> *</span></div>
        </div>
        <div class="grid grid-cols-2 bg-base-200 px-2 my-1">
          <div class="">Average Outcome Score</div>
          <div class="ox-stat">
            {{ avgFeedbackScore }}
          </div>
        </div>
        <div class="grid grid-cols-2 px-2">
          <div class="">Highest Scoring Criterion</div>
          <div class="ox-stat">
            {{ highestCriterion }}
          </div>
        </div>
        <div class="grid grid-cols-2 bg-base-200 px-2 my-1">
          <div class="">Lowest Scoring Criterion</div>
          <div class="ox-stat">
            {{ lowestCriterion }}
          </div>
        </div>
        <div class="grid grid-cols-2 px-2">
          <div class="">Number of Reports</div>
          <div class="ox-stat">
            {{ reportsUsed }}
          </div>
        </div>
        <div class="grid grid-cols-2 bg-base-200 px-2 my-1">
          <div class="">Number of Users</div>
          <div class="ox-stat">
            {{ numUsers }}
          </div>
        </div>
      </dl>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    framework: {
      type: Object,
      required: true,
    },
  },
  computed: {
    avgOxScore() {
      if (this.framework) {
        return this.framework.ox_score;
      }
      return "";
    },
    has_skipped() {
      if (this.framework) {
        return this.framework.has_skipped;
      }
      return "";
    },
    reportsUsed() {
      if (this.framework) {
        return this.framework.number_of_reports;
      }
      return "";
    },
    numUsers() {
      if (this.framework) {
        return this.framework.number_of_users;
      }
      return "";
    },
    highestCriterion() {
      if (this.framework && this.framework.highest_scoring_criterion) {
        return this.framework.highest_scoring_criterion.name;
      }
      return "";
    },
    lowestCriterion() {
      if (this.framework && this.framework.lowest_scoring_criterion) {
        return this.framework.lowest_scoring_criterion.name;
      }
      return "";
    },
    avgFeedbackScore() {
      return this.framework.average_feedback_score && !isNaN(this.framework.average_feedback_score)
        ? Math.round(this.framework.average_feedback_score) + "%"
        : "N/A";
    },
  },
};
</script>

<style scoped>
.ox-stat {
  @apply text-right font-bold;
}
</style>
