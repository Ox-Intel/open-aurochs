<template>
  <div class="p-3 w-full relative" :class="activity?.__type == 'report' && oxScore ? 'min-h-[6rem]' : 'min-h-[4.5rem]'">
    <div v-if="oxScore && activity.__type == 'report'" class="block mr-2 float-right text-center align-middle">
      <OxScoreBox :ox-score="oxScore" :has-skipped="hasSkipped" :in-feed="true" />
    </div>
    <div class="flex space-x-3">
      <div class="flex-shrink-0">
        <OxObjectIcon :target="record" :classes="'h-10 w-10'" />
      </div>
      <div class="min-w-0 flex-grow mb-4">
        <p class="text-large font-medium" data-cy="item-name">
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span v-html="highlighted(record.name)" />
        </p>
        <div
          v-for="(t, tag_idx) in tags"
          :key="tag_idx"
          class="inline-block mr-1"
          @click.stop.prevent="searchForTag(t)"
        >
          <div
            class="badge badge-sm badge-outline bg-base-300 border-base-300 hover:border-dark-grey gap-1 my-1 text-xs select-none overflow-hidden whitespace-nowrap"
          >
            <!-- eslint-disable-next-line vue/no-v-html -->
            <span v-html="highlighted(t.name)" />
          </div>
        </div>

        <div v-if="activity.__type == 'report' && stacks.length > 0">
          <div
            v-for="(s, idx) in stacks"
            :key="idx"
            class="badge badge-md badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 my-1 text-xs select-none overflow-hidden whitespace-nowrap"
          >
            <router-link :to="`/stack/${s.id}`"
              ><a>
                <OxObjectIcon :type="'stack'" :classes="'h-3 w-3 mr-0.5 align-middle'" />
                {{ s.name }}
              </a></router-link
            >
          </div>
        </div>
      </div>
    </div>
    <div class="absolute w-full bottom-0 left-0 flex place-items-center mt-2 justify-between pr-4">
      <!-- <p class="text-xs text-base-500 mt-1">
          {{ byline }}
        </p> -->
      <!-- <p class="text-xs text-base-500">
          {{ createdAt }}
        </p> -->
      <div class="ml-16">
        <OxOwnerBadges :object="activity" :search-text="searchText" />
      </div>
      <div class="text-xs text-base-500">
        {{ updatedAt }}
      </div>
    </div>
  </div>
</template>

<script>
import * as DOMPurify from "dompurify";
import OxObjectIcon from "./icons/OxObjectIcon.vue";
import OxScoreBox from "./OxScoreBox.vue";
import OxOwnerBadges from "./OxOwnerBadges.vue";
import { useAurochsData } from "../../stores/aurochs";

import formatDate from "../../mixins/format_date";

export default {
  components: {
    OxScoreBox,
    OxObjectIcon,
    OxOwnerBadges,
  },
  mixins: [formatDate],
  props: {
    activity: {
      type: Object,
      required: true,
      default: () => {},
    },
    tag: {
      type: String,
      default: () => "",
    },
    searchText: {
      type: String,
      default: () => "",
    },
    private_only: {
      type: Boolean,
      default: () => false,
    },
  },
  emits: ["set-featured"],
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    teams() {
      return this.aurochsData.teams;
    },
    organizations() {
      return this.aurochsData.organizations;
    },
    record() {
      return this.activity;
    },
    stacks() {
      if (this.activity.__type == "report" && this.activity.stack_ids?.length > 0) {
        let stacks = [];
        for (let s_id of this.activity.stack_ids) {
          stacks.push(this.aurochsData.stacks[s_id]);
        }
        return stacks;
      }
      return [];
    },
    tags() {
      if (this.activity.tags?.length > 0) {
        let tags = [];
        for (let tag of this.activity.tags) {
          tags.push(tag);
        }
        return tags;
      }
      return [];
    },
    // orgs() {
    //   return this.activity.permissions.administer?.organizations;
    // },
    // obj_teams() {
    //   return this.activity.permissions.administer?.teams;
    // },
    createdUser() {
      let user = this.record.created_by ? this.record.created_by : null;
      let name = null;
      if (user) {
        name = user.first_name + " " + user.last_name;
      }
      return name;
    },
    byline() {
      let byline = "";
      if (this.record.createdUser) {
        byline += "By " + this.record.createdUser;
      }
      return byline;
    },
    createdAt() {
      return "Created on " + this.formatDate(this.record.created_at_ms);
    },
    updatedAt() {
      return "Updated on " + this.formatDate(this.record.modified_at_ms);
    },
    oxScore() {
      let score;
      if (this.activity.record) {
        score = Number(this.activity.record.ox_score);
      } else {
        score = Number(this.activity.ox_score);
      }
      return score;
    },
    hasSkipped() {
      let skip;
      if (this.activity.record) {
        skip = this.activity.record.has_skipped;
      } else {
        skip = this.activity.has_skipped;
      }
      return skip;
    },
  },
  methods: {
    setFeatured(record) {
      this.$emit("set-featured", record);
    },
    highlighted(name) {
      if (this.searchText) {
        return DOMPurify.sanitize(name).replace(new RegExp(this.searchText, "gi"), (match) => {
          return '<span class="font-bold">' + match + "</span>";
        });
      }
      return name;
    },
    searchForTag(tag) {
      this.emitter.emit("updateSearch", { query: "tag:" + tag.name });
    },
  },
};
</script>
