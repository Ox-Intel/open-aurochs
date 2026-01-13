<template>
  <DefaultLayout>
    <main class="" data-cy="library">
      <div class="flex flex-row overflow-hidden gap-12">
        <LibraryFeed title="My Library" :private_only="true" data-cy="my-library-list" class="basis-1/2" />
        <LibraryFeed title="Shared Library" :private_only="false" data-cy="shared-library-list" class="basis-1/2" />
      </div>
    </main>
  </DefaultLayout>
</template>

<script>
import "regenerator-runtime/runtime";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import LibraryFeed from "../components/library/LibraryFeed.vue";
import { ref } from "vue";
import { useAurochsData } from "../stores/aurochs";

export default {
  components: {
    DefaultLayout,
    LibraryFeed,
  },
  setup() {
    const showCreateModal = ref(false);
    document.title = "Ox Library";

    return {
      aurochsData: useAurochsData(),
      showCreateModal,
    };
  },
  methods: {},
};
</script>

<style scoped>
html {
  @apply h-full;
}

body {
  @apply h-full;
}
</style>
