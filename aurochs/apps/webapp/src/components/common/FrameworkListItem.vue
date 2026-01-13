<template>
  <div class="relative" data-cy="framework-list-item" @click="setFeatured(record)">
    <div class="flex flex-row">
      <div class="mr-3 align-middle">
        <OxChartIcon :criteria="record.criteria" :chart_id="`framework_icon_${record.id}`" :small="true" />
      </div>
      <div class="max-h-24 overflow-hidden align-middle">
        <h3 class="">
          <span class="absolute inset-0" aria-hidden="true" />
          {{ record.name }}
        </h3>
      </div>
    </div>
  </div>
</template>
<script>
import OxChartIcon from "./icons/OxChartIcon.vue";
export default {
  components: {
    OxChartIcon,
  },
  props: {
    record: {
      type: Object,
      required: true,
    },
    chart_id: {
      type: Number,
      required: true,
    },
  },
  emits: ["set-featured"],
  methods: {
    setFeatured(record) {
      this.$emit("set-featured", record);
    },
  },
};
</script>
