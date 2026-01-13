<template>
  <div class="flex" data-cy="discussion">
    <div class="w-2/3 mr-8">
      <article class="prose max-w-none comment_block">
        <div v-for="(comment, idx) in target?.comments" :key="idx">
          <CommentCard :comment="comment" :target="target" :add="false" />
        </div>
        <CommentCard :add="true" :target="target" />
      </article>
    </div>
    <div class="w-1/3 mr-8 pt-4">
      <article class="prose max-w-none relative">
        <div
          v-if="!target?.subscribed"
          data-cy="follow"
          class="btn btn-primary absolute right-0 top-0"
          role="button"
          @click="subscribe"
        >
          <FontAwesomeIcon :icon="['fad', 'bell-plus']" class="h-6 w-6 mr-1" />
          Follow
        </div>
        <div
          v-if="target?.subscribed"
          data-cy="unfollow"
          class="btn hover:btn-error btn-primary btn-outline absolute right-0 top-0"
          role="button"
          @click="unsubscribe"
        >
          <FontAwesomeIcon :icon="['fad', 'bell-slash']" class="h-6 w-6 mr-1" />
          Unfollow
        </div>
        <h2 class="pt-2 mt-0">Participants</h2>
        <div v-for="person in allParticipants" :key="person.user.id" class="flex w-full mb-2">
          <OxAvatar :user="person.user" class="mr-2" />
          <div class="grow text-xl align-middle mt-2">
            {{ person.user.full_name }}
          </div>
          <div class="px-2 py-3" :class="person.subscribed ? 'text-neutral' : 'text-base-300'">
            <FontAwesomeIcon :icon="['fad', 'bell']" class="align-middlew-6 h-6" />
          </div>
          <div class="px-2 py-3" :class="person.commented ? 'text-neutral' : 'text-base-300'">
            <FontAwesomeIcon :icon="['fad', 'message']" class="align-middlew-6 h-6" />
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import CommentCard from "./CommentCard.vue";
import OxAvatar from "./OxAvatar.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faMessage } from "@fortawesome/pro-duotone-svg-icons/faMessage";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faBell } from "@fortawesome/pro-duotone-svg-icons/faBell";
import { faBellPlus } from "@fortawesome/pro-duotone-svg-icons/faBellPlus";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faBellSlash } from "@fortawesome/pro-duotone-svg-icons/faBellSlash";

library.add(faMessage, faTrashCan, faBell, faBellPlus, faPen, faBellSlash);

export default {
  components: {
    OxAvatar,
    CommentCard,
    FontAwesomeIcon,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    allParticipants() {
      var people = {};
      for (var i in this.target?.comments) {
        people[`user_${this.target.comments[i].user.id}`] = {
          user: this.target.comments[i].user,
          commented: true,
        };
      }
      for (i in this.target?.subscribers) {
        people[`user_${this.target.subscribers[i].id}`] = people[`user_${this.target.subscribers[i].id}`] || {
          user: this.target.subscribers[i],
          commented: false,
        };
        people[`user_${this.target.subscribers[i].id}`].subscribed = true;
      }
      return people;
    },
  },
  mounted() {
    // this.$pollTimeout = setTimeout(this.pollUpdates, 10000);
  },
  beforeUnmount() {
    // clearTimeout(this.$pollTimeout);
  },
  methods: {
    // async pollUpdates() {
    //   if (this.target?.__type) {
    //     await this.$sendEvent(`get_${this.target.__type}`, { id: this.target.id });
    //   }
    //   this.$pollTimeout = setTimeout(this.pollUpdates, 10000);
    // },
    async subscribe() {
      const data = {
        object_type: this.target.__type,
        id: this.target.id,
      };
      await this.$sendEvent("subscribe", data);
    },
    async unsubscribe() {
      const data = {
        object_type: this.target.__type,
        id: this.target.id,
      };
      await this.$sendEvent("unsubscribe", data);
    },
  },
};
</script>

<style scoped>
.comment_block {
  max-width: 65vw;
}
</style>
