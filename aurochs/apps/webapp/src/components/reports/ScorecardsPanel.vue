<template>
  <div :data-cy="dataCy">
    <ScorecardFeed :report="report" :scorecards-by-framework="scorecardsByFramework" />
    <div
      v-if="Object.keys(scorecardsByFramework).length == 0"
      class="card w-full bg-base-200 card-bordered m-8 max-w-screen-md"
      data-cy="no-scorecards"
    >
      <div class="card-body w-full">
        <div class="flex">
          <div class="w-12 text-center">
            <FontAwesomeIcon :icon="['fad', 'poll-people']" class="h-12 w-12 text-medium-grey" />
          </div>
          <div class="grow text-left px-4 pt-2 flex justify-between">
            <div class="text-xl text-medium-grey">No scorecards yet.</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ScorecardFeed from "./ScorecardFeed.vue";
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faPollPeople } from "@fortawesome/pro-duotone-svg-icons/faPollPeople";

library.add(faPollPeople);
export default {
  components: {
    ScorecardFeed,
    FontAwesomeIcon,
  },
  props: {
    report: {
      type: Object,
      default: () => {},
    },
    scorecardsByFramework: {
      type: Object,
      default: () => {},
    },
    dataCy: {
      type: String,
      default: () => "",
    },
  },
};
</script>
