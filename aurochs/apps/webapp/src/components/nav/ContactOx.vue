<template>
  <div data-cy="contact-ox">
    <article class="prose max-w-none">
      <div class="relative p-2">
        <label data-cy="close" for="contact-ox-modal" class="btn btn-sm btn-circle absolute right-4 top-4">
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle fa-swap-opacity" />
        </label>
      </div>
      <h1 class="mt-0">
        <FontAwesomeIcon :icon="['fad', 'envelope']" class="mr-2 mb-2 align-middle" />
        Contact Ox
      </h1>
      <p>Hit a bug? Have an idea to make Ox better? Let us know and we'll get right back to you.</p>
      <form class="mt-3" @submit="saveFeedback">
        <OxTextarea v-model="message" placeholder="It would be great if I could..." :min-rows="5" :size="'md'" />
      </form>
      <div class="flex justify-end">
        <a
          class="btn btn-success"
          :href="`mailto:${supportEmail}?subject=Ox Feedback: Ox should...&body=Hi Ox,%0D%0A %0D%0A${message}%0D%0A %0D%0ATechnical Details: %0D%0AUser:%0D%0A${username}`"
        >
          <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
          Send Feedback
        </a>
      </div>
    </article>
  </div>
</template>

<script>
import { ref } from "vue";
import { useAurochsData } from "../../stores/aurochs";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";

import OxTextarea from "../common/forms/OxTextarea.vue";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faEnvelope } from "@fortawesome/pro-duotone-svg-icons/faEnvelope";

library.add(faCheck, faXmark, faEnvelope);

export default {
  components: {
    FontAwesomeIcon,
    OxTextarea,
  },
  setup() {
    const message = ref("");
    const saving = ref(false);
    return {
      message,
      saving,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    user() {
      return this.aurochsData.user;
    },
    supportEmail() {
      return "support@oxintel.ai";
    },
    username() {
      return this.user.username;
    },
  },
};
</script>
