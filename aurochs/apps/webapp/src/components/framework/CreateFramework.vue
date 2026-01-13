<template>
  <div
    class="relative inline-block align-bottom bg-base-300 px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6"
  >
    <div class="hidden sm:block absolute top-0 right-0 pt-4 pr-4">
      <button
        type="button"
        class="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
        @click="$emit('close')"
      >
        <span class="sr-only">Close</span>
        <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-6 w-6 align-middle fa-swap-opacity" />
      </button>
    </div>
    <!-- Begin Creation -->
    <div class="sm:flex sm:items-start">
      <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left w-full">
        <DialogTitle as="h3" class="text-lg leading-6 font-medium mb-3"> Create a New Framework </DialogTitle>
        <div class="mt-2 w-full">
          <nav aria-label="Create Framework Steps">
            <ol role="list" class="border border-gray-300 divide-y divide-gray-300 md:flex md:divide-y-0">
              <li
                v-for="(step, stepIdx) in steps"
                :key="step.name"
                class="relative md:flex-1 md:flex w-full"
                @click="setStepIdx(stepIdx)"
              >
                <StepperItem :id="step.id" :class="stepClass" :name="step.name" :status="step.status" />
                <template v-if="stepIdx !== steps.length - 1">
                  <!-- Arrow separator for lg screens and up -->
                  <div class="hidden md:block absolute top-0 right-0 h-full w-5" aria-hidden="true">
                    <svg class="h-full w-full" viewBox="0 0 22 80" fill="none" preserveAspectRatio="none">
                      <path
                        d="M0 -2L20 40L0 82"
                        vector-effect="non-scaling-stroke"
                        stroke="currentcolor"
                        stroke-linejoin="round"
                      />
                    </svg>
                  </div>
                </template>
              </li>
            </ol>
          </nav>
        </div>
        <!-- step 1 -->
        <div v-if="stepIdx === 0" class="">
          <OxInput v-model="framework.name" placeholder="Name the framework..." input-type="text" label="Name" />
          <OxTextarea
            v-model="framework.subtitle"
            placeholder="Write a subtitle..."
            input-type="textarea"
            label="Subtitle"
          />
        </div>
        <!-- step 2 -->
        <div v-if="stepIdx === 1" class="">
          <div v-for="criteria in framework.criteria" :key="criteria.id">
            <div class="grid grid-cols-2">
              <div>
                <OxSlider v-model:score="framework.criteria" label="Criteria" :min="0" :max="10" />
              </div>
              <div>graph</div>
            </div>
          </div>
        </div>
        <!-- step 3 -->
        <div v-if="stepIdx === 2" class="">
          <OxInput v-model="framework.name" placeholder="Name the framework..." input-type="text" label="Name" />
          <OxTextarea
            v-model="framework.subtitle"
            placeholder="Write a subtitle..."
            input-type="textarea"
            label="Subtitle"
          />
        </div>
      </div>
    </div>
    <!-- end creation -->
    <div v-if="allStepsComplete" class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
      <button
        type="button"
        class="w-full inline-flex justify-center border border-transparent shadow-sm px-4 py-2 bg-green-600 text-base font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 sm:ml-3 sm:w-auto sm:text-sm"
        @click="save"
      >
        Save New Framework
      </button>
      <button
        type="button"
        class="mt-3 w-full inline-flex justify-center border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 sm:mt-0 sm:w-auto sm:text-sm"
        @click="close"
      >
        Cancel
      </button>
    </div>
  </div>
</template>

<script>
import { DialogTitle } from "@headlessui/vue";
import { ref } from "vue";
import OxInput from "../common/forms/OxInput.vue";
import OxTextarea from "../common/forms/OxTextarea.vue";
import StepperItem from "../common/StepperItem.vue";
import OxSlider from "../common/forms/OxSlider.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";

library.add(faXmark);

export default {
  components: {
    DialogTitle,
    OxInput,
    OxTextarea,
    StepperItem,
    OxSlider,
    FontAwesomeIcon,
  },
  emits: ["close"],
  setup() {
    const steps = [
      { id: "01", name: "Framework Name", status: "complete" },
      { id: "02", name: "Define Criteria", status: "current" },
      { id: "03", name: "Review and Save", status: "regular" },
    ];
    const framework = ref({ criteria: [{}, {}, {}, {}, {}] });
    return {
      steps,
      framework,
    };
  },
  computed: {
    allStepsComplete() {
      return this.steps.reduce((prev, current) => {
        return prev.status === "complete" && current.status === "complete";
      });
    },
  },
  methods: {
    setStepIdx(idx) {
      this.stepIdx = idx;
    },
    resetForm() {},
    close() {
      this.resetForm();
      this.$emit("close");
    },
    stepClass(stepIdx) {
      switch (stepIdx) {
        case 2:
          return "px-6 py-4 flex items-center text-sm font-medium";
        default:
          return "group flex items-center";
      }
    },
    save() {},
  },
};
</script>
