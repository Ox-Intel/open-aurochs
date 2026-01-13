<template>
  <div
    class="relative inline-block align-bottom bg-base-100 px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6"
  >
    <div class="hidden sm:block absolute top-0 right-0 pt-4 pr-4">
      <button type="button" class="focus:outline-none" @click="close">
        <span class="sr-only">Close</span>
        <FontAwesomeIcon :active="active" :icon="['fad', 'xmark']" class="h-6 w-6 align-middle fa-swap-opacity" />
      </button>
    </div>
    <div class="sm:flex sm:items-start">
      <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
        <DialogTitle as="h2" class="text-lg leading-6 font-medium"> {{ createOrEditOrClone }} Framework </DialogTitle>
        <div class="mt-2 w-full">
          <OxInput
            v-model="formData.name"
            data-cy="framework-name"
            placeholder="Enter name..."
            label="Framework Name"
          />
          <OxTextarea v-model="formData.subtitle" placeholder="Enter subtitle..." label="Framework subtitle" />
        </div>
      </div>
    </div>
    <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
      <button data-cy="save-clone" type="button" role="button" class="ml-2 btn btn-success" @click="saveFramework">
        Save
      </button>
      <button data-cy="cancel-clone" type="button" role="button" class="ml-2 btn btn-outline btn-error" @click="close">
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import OxInput from "../common/forms/OxInput.vue";
import OxTextarea from "../common/forms/OxTextarea.vue";
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";

library.add(faXmark);

export default {
  components: {
    OxInput,
    OxTextarea,
    FontAwesomeIcon,
  },
  props: {
    open: {
      type: Boolean,
      default: false,
    },
    framework: {
      type: Object,
      default: () => {},
    },
    isClone: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["save", "close"],
  setup() {
    const formData = ref({});
    return {
      formData,
    };
  },
  computed: {
    createOrEditOrClone() {
      if (this.isClone) {
        return "Duplicate";
      }
      if (this.framework && this.framework.id) {
        return "Edit";
      }
      return "Create";
    },
  },
  watch: {
    framework(newVal) {
      if (newVal) {
        this.formData = { ...this.framework };
      }
    },
  },
  mounted() {
    if (this.framework) {
      this.formData = { ...this.framework };
      if (this.isClone) {
        this.formData.name = "Copy of " + (this.framework.name ? this.framework.name : "framework");
        this.formData.description = this.framework.description ? this.framework.description : "";
      }
    }
  },
  methods: {
    saveFramework() {
      this.$emit("save", this.formData);
    },
    close() {
      this.$emit("close");
    },
  },
};
</script>
