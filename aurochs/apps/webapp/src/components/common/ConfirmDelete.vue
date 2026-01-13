<!-- This example requires Tailwind CSS v2.0+ -->
<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="relative z-10" @close="close">
      <TransitionChild
        as="template"
        enter="ease-out duration-300"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="ease-in duration-200"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
      </TransitionChild>

      <div class="fixed z-10 inset-0 overflow-y-auto">
        <div class="flex items-end sm:items-center justify-center min-h-full p-4 text-center sm:p-0">
          <TransitionChild
            as="template"
            enter="ease-out duration-300"
            enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enter-to="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leave-from="opacity-100 translate-y-0 sm:scale-100"
            leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <DialogPanel
              class="relative bg-base-100 px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg sm:w-full sm:p-6"
            >
              <div class="hidden sm:block absolute top-0 right-0 pt-4 pr-4">
                <button
                  type="button"
                  class="focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500"
                  @click="close"
                >
                  <span class="sr-only">Close</span>
                  <FontAwesomeIcon :icon="['fad', 'xmark']" class="fa-swap-opacity" />
                </button>
              </div>
              <div class="sm:flex sm:items-start">
                <div
                  class="mx-auto flex-shrink-0 flex items-center justify-center h-12 w-12 bg-red-100 sm:mx-0 sm:h-10 sm:w-10"
                >
                  <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="h-6 w-6 text-red-600" />
                </div>
                <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <DialogTitle as="h3" class="text-lg leading-6 font-medium text-gray-900">
                    Confirm Delete
                  </DialogTitle>
                  <div class="mt-2">
                    <p class="text-sm text-gray-500">
                      {{ message }}
                    </p>
                  </div>
                </div>
              </div>
              <div class="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  class="w-full inline-flex justify-center border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:ml-3 sm:w-auto sm:text-sm"
                  @click="confirm"
                >
                  Delete
                </button>
                <button
                  type="button"
                  class="mt-3 w-full inline-flex justify-center border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-500 sm:mt-0 sm:w-auto sm:text-sm"
                  @click="close"
                >
                  Cancel
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from "@headlessui/vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";

library.add(faXmark, faTriangleExclamation);

export default {
  components: {
    Dialog,
    DialogPanel,
    DialogTitle,
    TransitionChild,
    TransitionRoot,
    FontAwesomeIcon,
  },
  props: {
    open: {
      type: Boolean,
      default: false,
    },
    message: {
      type: String,
      default: "Confirm Delete?",
    },
  },
  emits: ["close", "confirm"],
  methods: {
    close() {
      this.$emit("close");
    },
    confirm() {
      this.$emit("confirm");
    },
  },
};
</script>
