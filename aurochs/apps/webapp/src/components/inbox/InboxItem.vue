<template>
  <div class="card m-4 w-full shadow-sm bg-base-200" data-cy="inbox-item">
    <div class="card-body p-4">
      <div class="flex">
        <div class="w-16 pl-4 align-middle">
          <div
            v-if="ii.read"
            data-cy="read-dot"
            class="rounded-full h-6 w-6 mt-4 bg-base-300"
            role="button"
            @click="markUnread(ii)"
          />
          <div
            v-if="!ii.read"
            data-cy="unread-dot"
            class="rounded-full h-6 w-6 mt-4 bg-accent"
            role="button"
            @click="markRead(ii)"
          />
        </div>
        <div class="w-16" role="button">
          <router-link :to="`${ii.target.__type}/${ii.target.id}/#discussion`" @click="markRead(ii)"
            ><a> <OxObjectIcon :target="ii.target" :classes="'h-10 w-10 align-middle p-2'" /> </a
          ></router-link>
        </div>
        <div class="grow" role="button" @click="markRead(ii)">
          <router-link :to="`${ii.target.__type}/${ii.target.id}/#discussion`"
            ><a>
              <div class="font-bold text-lg mb-0" data-cy="name">
                {{ ii.target.name }}
              </div>
              <p class="nowrap my-0">
                <b data-cy="initiator">{{ ii.initiator.full_name }}:</b>
                {{ ii?.comment?.body }}
              </p>
            </a></router-link
          >
        </div>
        <div class="pt-1 pr-4">
          <div
            v-if="!ii.done"
            data-cy="mark-done"
            class="btn btn-rounded btn-primary btn-outline whitespace-nowrap"
            role="button"
            @click="markDone(ii)"
          >
            <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6 mr-2" />
            Mark Done
          </div>
          <div
            v-if="ii.done"
            data-cy="mark-active"
            class="btn btn-rounded btn-primary btn-outline whitespace-nowrap"
            role="button"
            @click="markActive(ii)"
          >
            <FontAwesomeIcon :icon="['fad', 'inbox-in']" class="h-6 w-6 mr-2" />

            Make Active
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import formatDate from "../../mixins/format_date";
import OxObjectIcon from "../common/icons/OxObjectIcon.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faUnlock } from "@fortawesome/pro-duotone-svg-icons/faUnlock";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faFileCsv } from "@fortawesome/pro-duotone-svg-icons/faFileCsv";
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faFilePdf } from "@fortawesome/pro-duotone-svg-icons/faFilePdf";
import { faFilePowerpoint } from "@fortawesome/pro-duotone-svg-icons/faFilePowerpoint";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faRotate } from "@fortawesome/pro-duotone-svg-icons/faRotate";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faDownload } from "@fortawesome/pro-duotone-svg-icons/faDownload";
import { faInboxIn } from "@fortawesome/pro-duotone-svg-icons/faInboxIn";

library.add(
  faUnlock,
  faTrashCan,
  faFileCsv,
  faClone,
  faPen,
  faFileLines,
  faChartSimpleHorizontal,
  faCompass,
  faMessages,
  faFiles,
  faFilePdf,
  faFilePowerpoint,
  faXmark,
  faCheck,
  faRotate,
  faPlus,
  faDownload,
  faInboxIn
);

export default {
  components: {
    FontAwesomeIcon,
    OxObjectIcon,
  },
  mixins: [formatDate],
  props: {
    ii: {
      type: Object,
      default: () => {},
    },
    ii_id: {
      type: String,
      default: () => "",
    },
  },
  setup() {
    return {
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    user() {
      return this.aurochsData.user;
    },
  },
  methods: {
    async markDone(ii) {
      await this.$sendEvent("mark_inbox_item_done", { id: ii.id });
      this.markRead(ii);
    },
    async markActive(ii) {
      await this.$sendEvent("mark_inbox_item_active", { id: ii.id });
    },
    async markRead(ii) {
      await this.$sendEvent("mark_inbox_item_read", { id: ii.id });
    },
    async markUnread(ii) {
      await this.$sendEvent("mark_inbox_item_unread", { id: ii.id });
    },
  },
};
</script>

<style scoped>
article {
  width: 80vw;
}
a {
  text-decoration: none;
}
</style>
