<template>
  <DefaultLayout class="">
    <main class="flex flex-row h-full max-h-screen">
      <article class="prose max-w-none">
        <div class="mx-auto mt-2">
          <h1>Inbox</h1>
          <p class="mt-0">
            Track comments on frameworks, reports, sources, and stacks you follow, and mark them done when complete.
          </p>
          <div class="mx-auto mt-2 pb-8">
            <TabGroup :default-index="0">
              <TabList class="tabs w-full ml-6">
                <Tab
                  v-for="tab in tabs"
                  v-slot="{ selected }"
                  :key="tab.name"
                  :data-cy="`tab-${tab.hash}`"
                  as="template"
                >
                  <div class="tab tab-bordered tab-lg focus:outline-none" :class="selected ? 'tab-active' : ''">
                    <FontAwesomeIcon :icon="tab.icon" class="mr-2" />

                    <span>{{ tab.name }}</span>
                  </div>
                </Tab>
              </TabList>
              <TabPanels class="mt-8">
                <TabPanel>
                  <template v-for="(ii, idx) in inboxitems" :key="idx">
                    <InboxItem v-if="!ii.done" :ii="ii" />
                  </template>
                </TabPanel>
                <TabPanel>
                  <template v-for="(ii, idx) in inboxitems" :key="idx">
                    <InboxItem v-if="ii.done" :ii="ii" />
                  </template>
                </TabPanel>
              </TabPanels>
            </TabGroup>
          </div>
        </div>
      </article>
    </main>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useAurochsData } from "../stores/aurochs";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import InboxItem from "../components/inbox/InboxItem.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faBoxArchive } from "@fortawesome/pro-duotone-svg-icons/faBoxArchive";
import { faInbox } from "@fortawesome/pro-duotone-svg-icons/faInbox";

library.add(faBoxArchive, faInbox);

export default {
  components: {
    DefaultLayout,
    InboxItem,
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    FontAwesomeIcon,
  },
  setup() {
    const tabs = [
      { name: "Active", hash: "active", icon: ["fad", "inbox"] },
      { name: "Done", hash: "done", icon: ["fad", "box-archive"] },
    ];
    document.title = "Inbox";
    return {
      aurochsData: useAurochsData(),
      tabs,
    };
  },
  computed: {
    inboxitems() {
      return Object.values(this.aurochsData.inboxitems).sort(function (a, b) {
        if (b.read != a.read) {
          return a.read - b.read;
        }
        return a.comment.modified_at_ms - b.comment.modified_at_ms;
      });
    },
  },
};
</script>

<style scoped>
article {
  width: 80vw;
}
</style>
