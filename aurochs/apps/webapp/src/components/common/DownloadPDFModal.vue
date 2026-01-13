<template>
  <input id="download-modal" type="checkbox" class="modal-toggle" />
  <div class="modal">
    <div class="modal-box max-w-screen-sm p-10">
      <div class="relative">
        <label for="download-modal" class="btn btn-sm btn-circle text-base-100 absolute right-0 top-0">
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle" />
        </label>
      </div>
      <h3 class="text-2xl font-bold">
        <FontAwesomeIcon :icon="['fad', 'file-arrow-down']" class="mr-2 w-8 h-8 align-middle" />
        Export PDF
      </h3>
      <p class="py-4">Use the fields below to customize the PDF to your preferred format. (optional)</p>
      <div class="mt-4 form-control w-full">
        <label class="label font-bold">
          <span class="label-text">Title</span>
        </label>
        <input v-model="title" type="text" placeholder="" class="input input-bordered w-full" />
      </div>
      <div class="mt-4 form-control w-full">
        <label class="label font-bold">
          <span class="label-text">Organization Name</span>
        </label>
        <input v-model="orgName" type="text" placeholder="" class="input input-bordered w-full" />
      </div>
      <div class="mt-4 form-control w-full">
        <label class="label font-bold">
          <span class="label-text">Organization Logo</span>
        </label>
        <input type="file" placeholder="" class="input w-full" @input="orgLogo = $event.target.files[0]" />
      </div>
      <div class="mt-4 form-control w-full">
        <label class="label font-bold">
          <span class="label-text">Distribution/Classification Text</span>
        </label>
        <input v-model="distributionText" type="text" placeholder="" class="input input-bordered w-full" />
      </div>
      <!--       <div class="mt-4 form-control w-full">
        <label class="label font-bold">
          <span class="label-text">Theme</span>
        </label>
        <div class="btn-group">
          <button class="btn" :class="theme == 'standard' ? 'btn-active' : 'btn-outline'" @click="setTheme('standard')">
            Standard
          </button>
          <button class="btn" :class="theme == 'light' ? 'btn-active' : 'btn-outline'" @click="setTheme('light')">
            Light
          </button>
        </div>
      </div>
 -->
      <div class="flex flex-row justify-end mx-5 mt-6">
        <button type="button" role="button" class="btn btn-outline btn-base-300 hover:btn-error mr-2" @click="cancel">
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2 w-4 h-4 align-middle" />
          Cancel
        </button>
        <button type="button" role="button" class="btn btn-success" :disabled="saving" @click="downloadPDF">
          <FontAwesomeIcon v-if="!saving" :icon="['fad', 'arrow-down']" class="mr-2 w-4 h-4 align-middle" />
          <FontAwesomeIcon v-if="saving" :icon="['fad', 'rotate']" class="mr-2 w-4 h-4 align-middle fa-spin" />
          {{ saving ? "Exporting..." : "Export" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import { ref } from "vue";
import DownloadMixin from "../../mixins/download_file";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faFileArrowDown } from "@fortawesome/pro-duotone-svg-icons/faFileArrowDown";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faArrowDown } from "@fortawesome/pro-duotone-svg-icons/faArrowDown";
import { faRotate } from "@fortawesome/pro-duotone-svg-icons/faRotate";

library.add(faFileArrowDown, faXmark, faCheck, faArrowDown, faRotate);

export default {
  components: {
    FontAwesomeIcon,
  },
  mixins: [DownloadMixin],
  props: {
    target: {
      type: Object,
      default: () => {},
    },
    isOpen: {
      type: Boolean,
      default: () => false,
    },
    downloadType: {
      type: String,
      default: () => "Report",
    },
  },
  emits: ["close"],
  setup(props) {
    const saving = ref(false);
    const title = ref("");
    const orgName = ref("");
    const orgLogo = ref("");
    const previousId = ref(props.target.id);
    const distributionText = ref("");
    const theme = ref("standard");

    return {
      saving,
      aurochsData: useAurochsData(),
      title,
      orgName,
      orgLogo,
      distributionText,
      theme,
      previousId,
    };
  },
  computed: {},
  watch: {
    target(newVal) {
      if (newVal.id != this.previousId) {
        this.previousId = this.target.id;
        this.title = "";
        this.orgName = "";
        this.orgLogo = "";
        this.distributionText = "";
      }
    },
  },
  mounted() {
    this.title = "";
    this.orgName = "";
    this.orgLogo = "";
    this.distributionText = "";
    this.emitter.on("export_event", this.handleExportEvent);
  },
  methods: {
    base64toBlob(b64Data, contentType = "", sliceSize = 512) {
      const byteCharacters = atob(b64Data);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        const slice = byteCharacters.slice(offset, offset + sliceSize);

        const byteNumbers = new Array(slice.length);
        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      const blob = new Blob(byteArrays, { type: contentType });
      return blob;
    },
    handleExportEvent(data) {
      if (this.saving && data.data.event_type == "export-pdf") {
        let anchor = document.createElement("a");
        document.body.appendChild(anchor);
        let blob = this.base64toBlob(data.data.blob, "application/pdf");
        let objectUrl = window.URL.createObjectURL(blob);
        anchor.href = objectUrl;
        anchor.download = data.data.filename;
        anchor.click();
        window.URL.revokeObjectURL(objectUrl);
        this.saving = false;
      }
    },
    async downloadPDF() {
      this.saving = true;
      let data = {
        targetId: this.target.id,
        title: this.title,
        orgName: this.orgName,
        distributionText: this.distributionText,
        orgLogo: this.orgLogo,
        pageTheme: this.theme,
      };

      this.downloadFileAsync(
        `/export/${this.downloadType.toLowerCase()}/pdf/` + this.target.id + "/",
        `Ox ${this.downloadType} - ` + this.target.name,
        ".pdf",
        data
      ).then(() => {
        // this.saving = false;
      });
    },
    setTheme(t) {
      this.theme = t;
    },
    cancel() {
      this.$emit("close", true);
    },
  },
};
</script>
