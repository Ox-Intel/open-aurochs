<template>
  <FontAwesomeIcon
    v-if="greyscale && ((target && target.__type && target.__type == 'report') || type == 'report')"
    :icon="['fad', 'file-lines']"
    :class="classes + ' text-medium-grey'"
  />
  <FontAwesomeIcon
    v-if="!greyscale && ((target && target.__type && target.__type == 'report') || type == 'report')"
    :icon="['fad', 'file-lines']"
    :class="classes + ' text-report'"
    style="'--fa-primary-color: var(--report-color); --fa-secondary-color: var(--report-background-color); --fa-secondary-opacity: 0.9; --fa-primary-opacity: 0.9;'"
  />
  <FontAwesomeIcon
    v-if="(target && target.__type && target.__type == 'stack') || type == 'stack'"
    :icon="['fad', 'layer-group']"
    :class="classes + (greyscale ? ' text-medium-grey' : ' text-stack')"
  />
  <FontAwesomeIcon
    v-if="(target && target.__type && target.__type == 'source') || type == 'source'"
    :icon="['fad', 'link-horizontal']"
    :class="classes + (greyscale ? ' text-medium-grey' : ' text-source')"
  />
  <FontAwesomeIcon
    v-if="(target && target.__type && target.__type == 'team') || type == 'team'"
    :icon="['fad', 'globe']"
    class=""
    :class="classes + (greyscale ? ' text-medium-grey' : ' text-medium-grey')"
  />
  <FontAwesomeIcon
    v-if="(target && target.__type && target.__type == 'organization') || type == 'organization'"
    :icon="['fad', 'users']"
    class=""
    :class="classes + (greyscale ? ' text-medium-grey' : ' text-medium-grey')"
  />
  <template v-if="target && target.__type && target.__type == 'framework' && target?.criteria.length > 0">
    <div :class="classes">
      <OxChartIcon
        ref="frameworkIcon"
        :chart_id="`object_icon_${target && target.id ? target.id : ''}`"
        :criteria="target?.criteria"
        :small="small"
        :horns="true"
        class="inline-block"
        :class="classes + (greyscale ? ' text-medium-grey' : ' inline-block')"
        :scale="scale"
        :style="
          tabIcon
            ? (small
                ? 'transform: scale(0.58); transform-origin: 0 0;'
                : 'transform: scale(1); transform-origin: 0 0') + (greyscale ? ' filter: grayscale(100%);' : ' ')
            : ''
        "
      />
    </div>
  </template>
  <template
    v-if="
      (type == 'framework' || (target && target.__type && target.__type == 'framework')) &&
      (!target || target.criteria == undefined || target?.criteria.length == 0)
    "
  >
    <div :class="classes">
      <OxChartIcon
        :chart_id="'blank_framework'"
        :criteria="[
          {
            name: 'Framework',
            weight: 10,
            index: 3,
            relative_weight_as_percent: 60,
            id: 1,
          },
          {
            name: 'Framework',
            weight: 4,
            index: 0,
            relative_weight_as_percent: 20,
            id: 2,
          },
          {
            name: 'Framework',
            weight: 4,
            index: 1,
            relative_weight_as_percent: 20,
            id: 3,
          },
        ]"
        :small="small"
        :horns="true"
        class="inline-block"
        :class="classes + (greyscale ? ' text-medium-grey' : ' inline-block')"
        :scale="scale"
        :style="
          (tabIcon
            ? small
              ? 'transform: scale(0.58); transform-origin: 0 0;'
              : 'transform: scale(1); transform-origin: 0 0'
            : '') + (greyscale ? ' filter: grayscale(100%);' : ' ')
        "
      />
    </div>
  </template>
</template>

<script>
// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faLayerGroup } from "@fortawesome/pro-duotone-svg-icons/faLayerGroup";
import { faLinkHorizontal } from "@fortawesome/pro-duotone-svg-icons/faLinkHorizontal";
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import OxChartIcon from "./OxChartIcon.vue";

library.add(faFileLines, faLinkHorizontal, faLayerGroup, faGlobe, faUsers);

export default {
  components: {
    OxChartIcon,
    FontAwesomeIcon,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
    classes: {
      type: String,
      default: "",
    },
    type: {
      type: String,
      default: "",
    },
    scale: {
      type: Number,
      default: () => 1,
    },
    greyscale: {
      type: Boolean,
      default: () => false,
    },
    small: {
      type: Boolean,
      default: () => true,
    },
    tabIcon: {
      type: Boolean,
      default: () => false,
    },
  },

  methods: {
    updateCriteria(criteria) {
      this.$refs?.frameworkIcon?.updateCriteria(criteria);
    },
  },
};
</script>
