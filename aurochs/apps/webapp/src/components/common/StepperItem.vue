<template>
  <div v-if="status === 'complete'">
    <span class="px-6 py-4 flex items-center text-sm font-medium">
      <span class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-green-600 group-hover:bg-green-800">
        <FontAwesomeIcon :icon="['fad', 'check']" class="w-6 h-6 text-white" />
      </span>
      <span class="ml-4 text-sm font-medium text-gray-900">{{ name }}</span>
    </span>
  </div>
  <div v-else-if="status === 'current'">
    <span class="px-6 py-4 flex items-center text-sm font-medium">
      <span
        class="flex-shrink-0 w-10 h-10 flex items-center justify-center bg-slate-600 group-hover:bg-slate-800 text-slate-100"
        >{{ id }}</span
      >
      <span class="ml-4 text-sm font-medium text-slate-600 group-hover:text-slate-900">{{ name }}</span>
    </span>
  </div>
  <div v-else>
    <span class="px-6 py-4 flex items-center text-sm font-medium">
      <span
        class="flex-shrink-0 w-10 h-10 flex items-center justify-center border-2 border-gray-300 group-hover:border-gray-400"
      >
        <span class="text-gray-500 group-hover:text-gray-900">{{ id }}</span>
      </span>
      <span class="ml-4 text-sm font-medium text-gray-500 group-hover:text-gray-900">{{ name }}</span>
    </span>
  </div>
</template>

<script>
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";

library.add(faCheck);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    name: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      default: "00",
    },
    status: {
      type: String,
      default: "regular",
    },
  },
  setup() {},
};
</script>
