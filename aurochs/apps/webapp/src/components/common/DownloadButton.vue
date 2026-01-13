<template>
  <div class="">
    <FontAwesomeIcon :icon="['fad', 'download']" />
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faDownload } from "@fortawesome/pro-duotone-svg-icons/faDownload";

library.add(faDownload);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  methods: {},
};
</script>

<style scoped>
.comment_block {
  max-width: 65vw;
}
</style>
