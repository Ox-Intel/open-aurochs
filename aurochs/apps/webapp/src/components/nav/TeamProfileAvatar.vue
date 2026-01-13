<template>
  <div class="mr-1" :title="team.name">
    <span
      class="inline-flex items-center px-2 py-0.5 text-xs font-medium bg-slate-100 text-slate-800"
      :title="team.name"
    >
      {{ initials }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    team: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
  computed: {
    initials() {
      let initials = "";
      if (this.team) {
        initials = this.team.name.toUpperCase().slice(0, 2);
      }
      return initials;
    },
  },
};
</script>
