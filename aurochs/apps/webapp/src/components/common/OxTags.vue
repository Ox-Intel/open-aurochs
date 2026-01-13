<template>
  <div v-click-outside="hideTagMenu">
    <div class="tags" :class="singleLine ? 'overflow-hidden h-6' : ''">
      <div
        v-for="t in collapsedTags"
        :key="t.id"
        class="tag badge badge-md badge-outline bg-base-200 border-base-300 gap-1 mr-2 mb-2 select-none"
        :class="t.deleting ? 'opacity-30' : ''"
        role="button"
        @click="searchForTag(t)"
      >
        <span data-cy="tag-name">{{ t.name }}</span>
        <div
          v-if="canEdit"
          data-cy="delete-tag"
          role="button"
          class="ml-1 text-medium-grey hover:text-error"
          @click.stop.prevent="removeTag(t)"
        >
          <FontAwesomeIcon :icon="['fad', 'circle-x']" class="" />
        </div>
      </div>
      <div
        v-if="canEdit"
        data-cy="add-tag"
        role="button"
        class="badge badge-md badge-primary gap-1 mr-2 select-none"
        @click="openTagMenu"
      >
        <div class="mr-1">
          <FontAwesomeIcon :icon="['fad', 'circle-plus']" class="" />
        </div>
        Add Tag
      </div>
    </div>
    <div v-if="canEdit" class="relative">
      <div
        v-if="addMenuOpen"
        v-click-outside="hideTagMenu"
        class="absolute z-50 bordered border-base-300 bg-base-200 p-4 shadow-xl top-0"
      >
        <input
          v-model="searchText"
          data-cy="tag-search"
          type="text"
          placeholder="Type a tag name"
          class="input input-bordered w-full"
          autofocus
          @keyup.enter="handleEnter"
          @keyup.escape="hideTagMenu"
        />
        <ul class="menu bg-base-200 min-w-max max-w-96 pl-0 max-h-96 overflow-hidden">
          <template v-for="(t, idx) in possibleTags" :key="idx">
            <li
              role="button"
              class="box-rounded rounded-md mb-0 w-full"
              :class="(onlyOneOption ? 'bg-base-300' : '') + (t.adding ? ' opacity-75 disabled' : '')"
              @click="addTag(t)"
            >
              <div class="p-2 align-middle">
                <FontAwesomeIcon v-show="t.adding" :icon="['fad', 'circle-notch']" class="align-middle fa-spin mt-2" />
                {{ t.adding ? "Adding " : "" }} {{ t.name }}
              </div>
            </li>
          </template>
          <li
            v-show="showNewTag"
            role="button"
            class="box-rounded rounded-md mb-0 whitespace-nowrap"
            :class="(noOptions ? 'bg-base-300' : '') + (newTagAdding ? ' opacity-75 disabled' : '')"
            @click="addTag({ name: searchText })"
          >
            <div class="p-2 align-middle">
              <FontAwesomeIcon
                v-show="newTagAdding"
                :icon="['fad', 'circle-notch']"
                class="align-middle fa-spin mt-2"
              />
              <b>{{ newTagAdding ? "Adding" : "Add:" }}</b>
              {{ searchText }}
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faCircleX } from "@fortawesome/pro-duotone-svg-icons/faCircleX";
import { faCirclePlus } from "@fortawesome/pro-duotone-svg-icons/faCirclePlus";
import { faCircleNotch } from "@fortawesome/pro-duotone-svg-icons/faCircleNotch";

library.add(faCircleX, faCirclePlus, faCircleNotch);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
    id: {
      type: String,
      default: () => undefined,
    },
    canEdit: {
      type: Boolean,
    },
    singleLine: {
      type: Boolean,
    },
  },
  setup() {
    const addMenuOpen = ref(false);
    const newTagAdding = ref(false);
    const searchText = ref("");

    return {
      addMenuOpen,
      newTagAdding,
      searchText,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    collapsedTags() {
      let names = {};
      let tags = [];
      for (let t_index in this.target?.tags) {
        if (this.target?.tags[t_index]?.name in names) {
          // Skip this.
        } else {
          names[this.target?.tags[t_index]?.name] = true;
          tags.push(this.target?.tags[t_index]);
        }
      }
      return tags;
    },
    possibleTags() {
      let tag_list = [];
      let tag_list_names = [];
      const lower_search_text = this.searchText.toLowerCase();
      for (let i in this.aurochsData.tags) {
        let tag_name_lower = this.aurochsData.tags[i].name.toLowerCase();
        if (!this.searchText || tag_name_lower.indexOf(lower_search_text) != -1) {
          let found = false;
          for (let j in this.target?.tags) {
            if (this.aurochsData.tags[i].name == this.target?.tags[j].name) {
              found = true;
              break;
            }
          }
          if (!found) {
            for (let name of tag_list_names) {
              if (name == tag_name_lower) {
                found = true;
                break;
              }
            }
          }
          if (!found) {
            tag_list.push(this.aurochsData.tags[i]);
            tag_list_names.push(tag_name_lower);
          }
        }
      }
      return tag_list.sort((a, b) => {
        return b.modified_at_ms - a.modified_at_ms;
      });
    },
    onlyOneOption() {
      return this.possibleTags.length == 1;
    },
    noOptions() {
      return this.possibleTags.length == 0;
    },
    showNewTag() {
      if (!this.searchText) {
        return false;
      }
      let found = false;
      const lower_search_text = this.searchText.toLowerCase();
      for (let i in this.aurochsData.tags) {
        if (this.aurochsData.tags[i].name.toLowerCase() == lower_search_text) {
          found = true;
          break;
        }
      }
      return !found;
    },
  },
  methods: {
    openTagMenu() {
      this.addMenuOpen = true;
    },
    hideTagMenu() {
      this.addMenuOpen = false;
    },
    async handleEnter() {
      if (this.onlyOneOption) {
        await this.addTag(this.possibleTags[0]);
        this.searchText = "";
      } else {
        if (this.noOptions) {
          await this.addTag({ name: this.searchText });
          this.searchText = "";
        }
      }
    },
    async addTag(tag) {
      if (tag.name) {
        tag.adding = true;
      } else {
        this.newTagAdding = true;
      }
      const event_type = `update_${this.target.__type}`;
      var tagList = [];
      for (var i in this.collapsedTags) {
        tagList.push({
          name: this.collapsedTags[i].name,
        });
      }

      tagList.push({
        name: tag.name,
      });

      const data = {
        id: this.target.id,
        tags: tagList,
      };
      await this.$sendEvent(event_type, data);
      if (tag.id) {
        tag.adding = false;
        this.searchText = "";
      } else {
        this.newTagAdding = false;
        this.searchText = "";
      }
    },
    async removeTag(tag) {
      tag.deleting = true;
      const event_type = `update_${this.target.__type}`;
      var tagList = [];
      for (var i in this.collapsedTags) {
        if (this.collapsedTags[i].name != tag.name) {
          tagList.push({
            name: this.collapsedTags[i].name,
          });
        }
      }
      const data = {
        id: this.target.id,
        tags: tagList,
      };
      await this.$sendEvent(event_type, data, this.aurochsData);
    },
    searchForTag(tag) {
      this.emitter.emit("updateSearch", { query: "tag:" + tag.name });
    },
  },
};
</script>
