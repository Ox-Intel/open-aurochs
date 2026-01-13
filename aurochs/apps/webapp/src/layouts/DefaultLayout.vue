<template>
  <div class="ox-page">
    <ox-navbar />
    <div class="pb-0 pt-24 p-4 sm:p-10 sm:pt-24 2xl:p-16 2xl:pt-24">
      <slot />
    </div>

    <!-- <ox-footer class="hidden" /> -->
  </div>
</template>

<script>
import OxNavbar from "../components/nav/OxNavbar.vue";
// import OxFooter from "../components/nav/OxFooter.vue";

export default {
  components: { OxNavbar },
};
</script>

<style>
.ox-page {
  @apply bg-base-100 block h-screen overflow-y-auto;
}
</style>
