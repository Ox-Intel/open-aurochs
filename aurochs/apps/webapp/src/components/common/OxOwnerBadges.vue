<template>
  <div class="inline-block">
    <div v-for="(t, team_idx) in objTeams" :key="team_idx" class="inline-block mr-2">
      <div
        class="rounded border opacity-60 text-dark-grey border-opacity-50 border-dark-grey gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
        :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
      >
        <FontAwesomeIcon :icon="['fad', 'users']" class="h-3 w-3 mr-1" />
        <!-- eslint-disable-next-line vue/no-v-html -->
        <span :class="medium ? 'text-sm' : 'text-xs'">
          {{ t.name }}
        </span>
      </div>
    </div>
    <div v-for="(o, org_idx) in objOrganizations" :key="org_idx" class="inline-block mr-2">
      <div
        class="rounded border opacity-60 text-dark-grey border-opacity-50 border-dark-grey gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
        :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
      >
        <FontAwesomeIcon :icon="['fad', 'globe']" class="h-3 w-3 mr-1" />
        <!-- eslint-disable-next-line vue/no-v-html -->
        <span :class="medium ? 'text-sm' : 'text-xs'">
          {{ o.name }}
        </span>
      </div>
    </div>
    <template v-if="showPeople">
      <div v-for="(p, p_idx) in objPeople" :key="p_idx" class="inline-block mr-2">
        <div
          class="rounded border opacity-70 text-dark-grey border-opacity-50 border-dark-grey gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
          :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
        >
          <!-- <FontAwesomeIcon :icon="['fad', 'user']" class="h-3 w-3 mr-1" /> -->
          <OxAvatar :user="p" :tiny="true" class="align-middle pt-2 mr-1" />
          <!-- eslint-disable-next-line vue/no-v-html -->
          <span :class="medium ? 'text-sm' : 'text-xs'">
            {{ p.full_name }}
          </span>
        </div>
      </div>
    </template>
    <div v-if="iAmOnlyAdmin && entirelyPrivate" class="inline-block mr-2">
      <div
        class="rounded border opacity-60 text-dark-grey border-opacity-50 border-dark-grey gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
        :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
      >
        <FontAwesomeIcon :icon="['fad', 'lock']" class="h-3 w-3 mr-1 fa-swap-opacity" />
        <!-- eslint-disable-next-line vue/no-v-html -->
        <span :class="medium ? 'text-sm' : 'text-xs'">Private</span>
      </div>
    </div>
    <div v-if="iAmOnlyAdmin && !entirelyPrivate" class="inline-block mr-2">
      <div
        class="rounded border opacity-70 text-white bg-dark-grey border-opacity-50 border-dark-grey gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
        :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
      >
        <FontAwesomeIcon :icon="['fad', 'user-plus']" class="h-3 w-3 mr-1" />
        <!-- eslint-disable-next-line vue/no-v-html -->
        <span :class="medium ? 'text-sm' : 'text-xs'">Shared</span>
      </div>
    </div>
    <!-- <div v-if="share" class="inline-block mr-2">
      <div
        class="rounded border opacity-70 text-primary border-primary hover:opacity-100 hover:bg-primary hover:text-white gap-1 my-1 select-none overflow-hidden whitespace-nowrap"
        :class="medium ? 'text-md px-1.5 py-1' : 'text-xs px-1 py-0.5 '"
      >
        <FontAwesomeIcon :icon="['fad', 'plus']" class="h-3 w-3 mr-1" />
        <span :class="medium ? 'text-sm' : 'text-xs'">Share</span>
      </div>
    </div> -->
  </div>
</template>

<script>
import * as DOMPurify from "dompurify";
import OxAvatar from "./OxAvatar.vue";
import { useAurochsData } from "../../stores/aurochs";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import { faUser } from "@fortawesome/pro-duotone-svg-icons/faUser";
import { faLock } from "@fortawesome/pro-duotone-svg-icons/faLock";
import { faUserPlus } from "@fortawesome/pro-duotone-svg-icons/faUserPlus";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";

library.add(faGlobe, faUsers, faUser, faLock, faUserPlus, faPlus);

export default {
  components: {
    FontAwesomeIcon,
    OxAvatar,
  },
  props: {
    object: {
      type: Object,
      default: () => {},
    },
    searchText: {
      type: String,
      default: () => "",
    },
    medium: {
      type: Boolean,
      default: () => false,
    },
    share: {
      type: Boolean,
      default: () => false,
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    objOrganizations() {
      // console.log(this.object)
      // return []
      let orgs = [];
      for (let key in this.object?.permissions) {
        if (this.object.permissions[key].slice(3, 4) == "1" && key.slice(0, 1) == "O") {
          orgs.push(this.aurochsData.organizations[key.slice(2)]);
        }
      }
      return orgs;
    },
    objTeams() {
      // console.log(this.object)
      // return []
      let teams = [];
      for (let key in this.object?.permissions) {
        if (this.object.permissions[key].slice(3, 4) == "1" && key.slice(0, 1) == "T") {
          teams.push(this.aurochsData.teams[key.slice(2)]);
        }
      }
      return teams;
    },
    objPeople() {
      // console.log(this.object)
      // return []
      let people = [];
      for (let key in this.object?.permissions) {
        if (this.object.permissions[key].slice(3, 4) == "1" && key.slice(0, 1) == "U") {
          people.push(this.aurochsData.users[key.slice(2)]);
        }
      }
      return people;
    },
    iAmOnlyAdmin() {
      return (
        this.objOrganizations.length == 0 &&
        this.objTeams.length == 0 &&
        this.objPeople.length == 1 &&
        this.objPeople[0].id == this.aurochsData.user.id
      );
    },
    entirelyPrivate() {
      return (
        this.object?.permissions &&
        Object.keys(this?.object?.permissions).length == 1 &&
        Object.keys(this?.object?.permissions)[0] == "U-" + this.aurochsData.user.id
      );
    },
    showPeople() {
      return this.objOrganizations.length == 0 && this.objTeams.length == 0 && !this.iAmOnlyAdmin;
    },
  },
  methods: {
    highlighted(name) {
      if (this.searchText) {
        return DOMPurify.sanitize(name).replace(new RegExp(this.searchText, "gi"), (match) => {
          return '<span class="font-bold">' + match + "</span>";
        });
      }
      return name;
    },
  },
};
</script>
