<template>
  <div class="px-4 py-8 text-sm">
    <div class="flex">
      <div class="align-bottom flex">
        <span class="block w-28 pt-2 text-medium-grey align-bottom">Owners:</span>
        <router-link :to="`/${object?.__type}/${object?.id}/#permissions`"
          ><a> <OxOwnerBadges :object="object" :medium="false" class="cursor-pointer" /> </a
        ></router-link>
      </div>
    </div>

    <div class="mb-0.5 mt-[0.15rem]">
      <div class="inline-block text-medium-grey">
        <span class="inline-block w-28">Created:</span>
        {{ object?.created_at_ms ? formatDate(object?.created_at_ms) : "" }}
        {{ object?.created_by ? "by " + object?.created_by.full_name : "" }}
      </div>
    </div>

    <div class="">
      <div class="text-medium-grey">
        <span class="inline-block w-28">Last Updated:</span>
        {{ object?.modified_at_ms ? formatDate(object?.modified_at_ms) : "" }}
        {{ object?.modified_by ? "by " + object?.modified_by.full_name : "" }}
      </div>
    </div>
  </div>
</template>

<script>
import formatDate from "../../mixins/format_date";
import OxOwnerBadges from "./OxOwnerBadges.vue";

export default {
  components: {
    OxOwnerBadges,
  },
  mixins: [formatDate],
  props: {
    object: {
      type: Object,
      default: () => {},
    },
  },
  setup() {
    return {};
  },
};
</script>
