<template>
  <div class="flex gap-1" data-cy="stack-badges">
    <div
      v-for="(s, idx) in stacks"
      :key="idx"
      :data-cy="`stack-${slugify(s.name)}`"
      class="cursor-pointer badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 my-1 text-xs select-none overflow-hidden whitespace-nowrap stack-badge"
      @click.stop.prevent="openStack(s)"
    >
      <OxObjectIcon :type="'stack'" :classes="'h-3 w-3 mr-0.5 align-middle'" />
      <span class="align-midle">{{ s.name }}</span>
    </div>
    <label v-if="canAdd" for="add-stack-modal" data-cy="add-to-stack">
      <div
        class="cursor-pointer badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 my-1 text-xs select-none overflow-hidden whitespace-nowrap"
      >
        <FontAwesomeIcon :icon="['fal', 'layer-plus']" class="text-stack h-3 w-3 mr-0.5 align-middle" />
        Add to Stack
      </div>
    </label>
  </div>
  <template v-if="canAdd">
    <input id="add-stack-modal" type="checkbox" class="modal-toggle" />
    <div class="modal" data-cy="add-stack-modal">
      <div class="modal-box relative">
        <div class="relative">
          <label for="add-stack-modal" class="btn btn-sm btn-circle absolute right-0 top-0">
            <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle" />
          </label>
        </div>
        <h3 class="text-2xl font-bold">
          <FontAwesomeIcon :icon="['fad', 'layer-group']" class="mr-2 align-middle text-stack" />
          Add to Stack
        </h3>
        <p class="py-4">To which stack would you like to add this report?</p>
        <OxSearchBox
          :options="aurochsData.stacks"
          :exclude="stacks"
          :placeholder="'Search for a stack...'"
          @selected-choice="setAddStack"
        />
        <div class="flex justify-end">
          <div
            data-cy="add-stack-to-report-from-modal"
            role="button"
            class="mt-4 btn btn-primary"
            :class="{
              'btn-disabled': !newStack || addingStack,
              saving: addingStack,
            }"
            @click="addStack()"
          >
            {{ addingStack ? "Adding..." : "Add to Stack" }}
          </div>
        </div>
      </div>
    </div>
  </template>
</template>

<script>
// import OxAvatar from "./OxAvatar.vue";
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import OxObjectIcon from "./icons/OxObjectIcon.vue";
import OxSearchBox from "./OxSearchBox.vue";
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faLayerGroup } from "@fortawesome/pro-duotone-svg-icons/faLayerGroup";
import { faLayerPlus } from "@fortawesome/pro-duotone-svg-icons/faLayerPlus";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";

library.add(faLayerGroup, faLayerPlus, faXmark);

export default {
  components: {
    FontAwesomeIcon,
    OxObjectIcon,
    OxSearchBox,
    // OxAvatar,
  },
  props: {
    object: {
      type: Object,
      default: () => {},
    },
    canAdd: {
      type: Boolean,
      default: () => false,
    },
  },
  setup() {
    const addingStack = ref(false);
    const newStack = ref(false);

    return {
      aurochsData: useAurochsData(),
      addingStack,
      newStack,
    };
  },
  computed: {
    stacks() {
      let stacks = [];
      for (let j in this.object?.stack_ids) {
        stacks.push(this.aurochsData.stacks[this.object.stack_ids[j]]);
      }
      return stacks;
    },
  },
  methods: {
    openStack(s) {
      this.$router.push(`/stack/${s.id}`);
    },
    setAddStack(stack) {
      this.newStack = stack;
    },
    async addStack() {
      this.addingStack = true;
      var data = {
        report_id: this.object.id,
        stack_id: this.newStack.id,
      };
      await this.$sendEvent("add_report_to_stack", data);
      this.addingStack = false;
      this.newStack = false;
      this.emitter.emit("clearSearchBox", { previousSelected: this.newStack });
      document.getElementById("add-stack-modal").checked = false;
    },
    slugify(name) {
      return name.toLowerCase().replaceAll(" ", "_").replaceAll('"', "'");
    },
    async removeStack(s) {
      if (window.confirm("Are you sure you want remove this report from the stack?")) {
        var data = {
          report_id: this.object.id,
          stack_id: s.id,
        };
        await this.$sendEvent("remove_report_from_stack", data);
      }
      return false;
    },
  },
};
</script>
