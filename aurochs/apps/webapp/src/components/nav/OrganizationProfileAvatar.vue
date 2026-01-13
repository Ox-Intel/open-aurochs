<template>
  <div class="mr-1" :title="organization.name">
    <span
      class="inline-flex items-center px-2.5 py-0.5 text-sm font-medium bg-sky-100 text-sky-800"
      :title="organization.name"
    >
      {{ initials }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    organization: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
  computed: {
    initials() {
      let initials = "";
      if (this.organization) {
        initials = this.organization.name.toUpperCase().slice(0, 2);
      }
      return initials;
    },
  },
};
</script>
