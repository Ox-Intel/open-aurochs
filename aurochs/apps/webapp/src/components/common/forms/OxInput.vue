<template>
  <div :class="{ 'my-5': !noMargin }">
    <div class="mt-1 relative shadow-sm">
      <label :for="label" class="label"
        ><span class="label-text">{{ label }}</span></label
      >
      <input
        :id="id"
        :type="inputType"
        :name="label"
        :value="modelValue"
        class="input input-bordered w-full bg-base-100 bg-base-100 text"
        :aria-describedby="label"
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <p v-if="hint" class="mt-2 text-xs text-gray-500">
        {{ hint }}
      </p>
      <div v-if="errors" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <FontAwesomeIcon :icon="['fad', 'circle-exclamation']" class="h-5 w-5 text-red-500" />
      </div>
      <p id="email-error" class="mt-2 text-sm text-red-600">
        {{ errors }}
      </p>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faCircleExclamation } from "@fortawesome/pro-duotone-svg-icons/faCircleExclamation";

library.add(faCircleExclamation);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    hint: {
      type: String,
      default: "",
    },
    label: {
      type: String,
      required: true,
    },
    id: {
      type: String,
      default: "",
    },
    inputType: {
      type: String,
      default: "text",
    },
    placeholder: {
      type: String,
      default: "",
    },
    noMargin: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue"],
  setup() {
    const errors = ref(null);
    return {
      errors,
    };
  },
};
</script>
