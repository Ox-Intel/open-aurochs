<template>
  <div v-if="selectedChoice" class="flex place-space-between bg-base-200 border-base-300 rounded-box border-2 p-4">
    <div class="w-12 h-12">
      <OxObjectIcon
        :target="selectedChoice"
        :classes="(selectedChoice.__type == 'framework' ? 'mt-0.5 h-8 w-8' : 'h-8 w-8') + 'mr-2 align-middle'"
      />
    </div>
    <div class="grow align-middle pt-2">
      {{ selectedChoice.name }}
    </div>
    <div role="button" class="mt-2" @click="clearSelectedChoice()">
      <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-6 w-6" />
    </div>
  </div>
  <div v-if="!selectedChoice">
    <input
      v-model="searchText"
      data-cy="searchbox-search"
      class="input input-bordered w-full search-input"
      :placeholder="placeholder"
    />
    <ul
      class="menu bg-base-100 w-full max-h-80 overflow-y-auto overflow-x-hidden mt-2 mr-8 box-rounded rounded-md z-20 p-4 pb-6"
    >
      <template v-for="(opt, idx) in remainingOptions" :key="idx">
        <li role="button" class="box-rounded rounded-md mb-0 w-full mr-8" :data-cy="`searchbox-option-${idx}`">
          <!-- :class="idx === selectedIndex ? 'bg-accent' : ''" -->
          <div class="p-2 align-left flex" @click="selectOption(opt)">
            <div class="w-12">
              <OxObjectIcon :target="opt" :classes="'h-10 w-10'" />
            </div>
            <div>
              {{ opt.name }}
            </div>
          </div>
        </li>
      </template>
    </ul>
  </div>
</template>

<script>
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";

library.add(faXmark);

import OxObjectIcon from "./icons/OxObjectIcon.vue";
import { ref } from "vue";
export default {
  components: {
    OxObjectIcon,
    FontAwesomeIcon,
  },
  props: {
    options: {
      type: Object,
      default: () => {},
    },
    exclude: {
      type: Object,
      default: () => {},
    },
    placeholder: {
      type: String,
      default: () => "Search...",
    },
  },
  emits: ["selectedChoice"],
  setup(props) {
    var lower_options = {};
    const selectedChoice = ref(null);
    const searchText = ref("");

    for (var o_index in props.options) {
      lower_options[o_index] = props.options[o_index].name.toLowerCase();
    }
    return {
      lower_options,
      selectedChoice,
      searchText,
    };
  },
  computed: {
    remainingOptions() {
      var ro = [];
      var excluded = false;
      const lower_search = this.searchText.toLowerCase();
      for (var o_index in this.lower_options) {
        if (this.lower_options[o_index].indexOf(lower_search) != -1 || this.searchText.length < 2) {
          excluded = false;
          for (var e_index in this.exclude) {
            if (
              this.options[o_index].id == this.exclude[e_index].id &&
              this.options[o_index].__type == this.exclude[e_index].__type
            ) {
              excluded = true;
            }
          }
          if (!excluded) {
            ro.push(this.options[o_index]);
          }
        }
      }
      // Sort by most recently modified_by
      ro = ro.sort((a, b) => {
        return b.modified_at_ms - a.modified_at_ms;
      });
      return ro;
    },
  },
  mounted() {
    this.clearSelectedChoice();
    this.emitter.on("clearSearchBox", (e) => {
      if (e.previousSelected == this.selectedChoice) {
        this.clearSelectedChoice();
      }
    });
  },
  methods: {
    selectOption(opt) {
      this.selectedChoice = opt;
      this.$emit("selectedChoice", opt);
    },
    clearSelectedChoice() {
      this.selectedChoice = null;
      this.searchText = "";
      this.$emit("selectedChoice", null);
    },
  },
};
</script>
