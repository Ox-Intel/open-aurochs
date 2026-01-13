<template>
  <DefaultLayout> Users </DefaultLayout>
</template>

<script>
import DefaultLayout from "../../layouts/DefaultLayout.vue";
export default {
  components: { DefaultLayout },
  data() {
    return { aurochs: window.aurochs };
  },
};
</script>
