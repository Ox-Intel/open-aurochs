<template>
  <div class="relative z-0">
    <input
      id="search"
      v-model="searchQuery"
      name="search"
      class="input input-bordered w-full"
      :placeholder="placeholder"
      type="search"
      data-cy="searchbar-input"
      @keyup="emitSearch"
    />
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  components: {},
  props: {
    placeholder: {
      type: String,
      default: "Search...",
    },
  },
  emits: ["search"],
  setup() {
    const searchQuery = ref("");
    return {
      searchQuery,
    };
  },
  methods: {
    emitSearch() {
      this.$emit("search", this.searchQuery);
    },
  },
};
</script>
