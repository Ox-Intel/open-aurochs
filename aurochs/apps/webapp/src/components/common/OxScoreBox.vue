<template>
  <div
    class="text-ox-score-content place-items-center p-1 w-12 h-12 rounded relative"
    :class="hasSkipped ? 'bg-medium-grey p-1' : 'bg-ox-score p-1 '"
  >
    <OxHorns class="h-8 w-8 mb-1 mt-0.5 mx-auto" />
    <div class="text-xl font-bold text-center -mt-6" data-cy="ox-score" :class="'hasSkipped' ? '' : ''">
      {{ oxScore }}
      <!-- <span class="text-xs -ml-1">%</span> -->

      <div
        v-if="hasSkipped && !inFeed"
        data-cy="star"
        class="star inline-block tooltip tooltip-left cursor-pointer"
        data-tip="At least one criteria was skipped."
      >
        <div class="text-md">*</div>
      </div>
      <div v-if="hasSkipped && inFeed" data-cy="star" class="font-normal text-md inline-block star">*</div>
    </div>
    <!-- <div class="text-2xs uppercase -mt-1">Ox</div> -->
  </div>
</template>

<script>
import OxHorns from "../../components/logo/OxHorns.vue";

export default {
  components: {
    OxHorns,
  },
  props: {
    oxScore: {
      type: Number,
      default: () => 0,
    },
    hasSkipped: {
      type: Boolean,
      default: () => false,
    },
    inFeed: {
      type: Boolean,
      default: () => false,
    },
  },
};
</script>
<style scoped>
.star {
  @apply absolute;
  top: 16px;
  margin-left: -1px;
}
</style>
