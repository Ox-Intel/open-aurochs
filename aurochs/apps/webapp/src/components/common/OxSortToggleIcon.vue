<template>
  <button role="button" type="button" class="ox-sort-button" @click="emitToggle">
    <FontAwesomeIcon v-if="sortAsc" :icon="['fad', 'arrow-up-short-wide']" class="h-4 w-4 inline" data-cy="up-arrow" />
    <FontAwesomeIcon
      v-if="!sortAsc"
      :icon="['fad', 'arrow-down-short-wide']"
      class="h-4 w-4 inline"
      data-cy="down-arrow"
    />
  </button>
</template>

<script>
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faArrowDownShortWide } from "@fortawesome/pro-duotone-svg-icons/faArrowDownShortWide";
import { faArrowUpShortWide } from "@fortawesome/pro-duotone-svg-icons/faArrowUpShortWide";

library.add(faArrowDownShortWide, faArrowUpShortWide);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    sortAsc: {
      type: Boolean,
    },
  },
  emits: ["toggle"],
  methods: {
    emitToggle() {
      this.$emit("toggle");
    },
  },
};
</script>

<style scoped>
.ox-sort-button {
  @apply btn rounded px-4 py-2 inline-flex items-center input input-bordered text-base-content border-base-300 hover:bg-base-200 hover:text-base-content;
}
</style>
