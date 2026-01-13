<template>
  <div :data-cy="data_cy">
    <label v-if="label" :for="label" class="label"
      ><span class="label-text font-bold" :class="sizeClasses">{{ label }}</span></label
    >
    <textarea
      ref="oxtextarea"
      v-model="text"
      :rows="minRows"
      :name="label"
      class="textarea w-full textarea-bordered leading-snug h-8 focus:outline-none focus-visible:ring focus-visible:ring-primary focus-visible:ring-opacity-25"
      :class="classes"
      :placeholder="placeholder"
      @input="handleInput"
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
      default: "",
    },
    inputType: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    minRows: {
      type: Number,
      default: 4,
    },
    maxHeight: {
      type: Number,
      default: 0,
    },
    size: {
      type: String,
      default: "sm",
    },
    classes: {
      type: String,
      default: "",
    },
    data_cy: {
      type: String,
      default: "",
    },
  },
  emits: ["update:modelValue"],
  setup(props) {
    const errors = ref(null);
    const text = ref(props.modelValue ? String(props.modelValue) : "");
    const id = Math.random().toString(36);
    const quillOptions = {
      scrollingContainer: ".ox-page",
    };

    return {
      errors,
      text,
      id,
      quillOptions,
    };
  },
  computed: {
    sizeClasses() {
      return `textarea-${this.size} text-${this.size}`;
    },
  },
  watch: {
    modelValue(newVal) {
      if (this.text != newVal) {
        this.text = newVal;
        this.$refs.oxtextarea.value = newVal;
        this.$refs.oxtextarea.innerHTML = newVal;
        this.resize();
      }
    },
  },
  mounted() {
    this.resize();
  },
  methods: {
    resize() {
      let ele = this.$refs.oxtextarea;
      ele.style.height = "18px";
      if (this.maxHeight && ele.scrollHeight > this.maxHeight) {
        ele.style.height = this.maxHeight + "px";
        ele.style.overflowY = "auto";
      } else {
        ele.style.height = ele.scrollHeight + "px";
        ele.style.overflowY = "none";
      }
    },
    handleInput(event) {
      this.$emit("update:modelValue", event.target.value);
      this.resize();
    },
  },
};
</script>

<style scoped>
textarea {
  resize: none;
  overflow: hidden;
}
textarea:focus {
  outline: none;
}
textarea::placeholder {
  @apply text-dark-grey;
  opacity: 0.7;
}
.ql-editor,
.ql-container {
  height: auto;
  min-height: 8rem;
}
</style>
