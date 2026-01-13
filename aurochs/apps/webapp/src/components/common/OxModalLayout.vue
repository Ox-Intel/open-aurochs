<template>
  <TransitionRoot as="template" :show="open">
    <Dialog as="div" class="fixed inset-0 overflow-y-auto" @close="$emit('close')">
      <div class="mt-12 flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <TransitionChild
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <DialogOverlay class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </TransitionChild>

        <TransitionChild
          enter="ease-out duration-300"
          enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          enter-to="opacity-100 translate-y-0 sm:scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 translate-y-0 sm:scale-100"
          leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
        >
          <slot />
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script>
import { TransitionRoot, TransitionChild, DialogOverlay, Dialog } from "@headlessui/vue";

export default {
  components: {
    TransitionRoot,
    TransitionChild,
    DialogOverlay,
    Dialog,
  },
  props: {
    open: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["close"],
  setup() {},
};
</script>
