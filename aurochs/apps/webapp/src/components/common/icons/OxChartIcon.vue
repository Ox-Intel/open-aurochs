<template>
  <!-- <div :style="`transform: scale(${scale}); transform-origin: top`"> -->
  <svg
    height="100%"
    width="100%"
    viewBox="0 0 42 42"
    class="block"
    :style="`width: {scale * 100}%; height: {scale * 100}%`"
  >
    <!-- <circle class="donut-hole" cx="21" cy="21" r="15.91549430918954" fill="transparent"></circle> -->
    <!-- <circle class="donut-ring" cx="21" cy="21" r="15.91549430918954" fill="transparent" stroke="#d2d3d4" stroke-width="8"></circle> -->
    <template v-for="(c, idx) in graphCriteria" :key="idx">
      {{ c.weight }}
      <path
        :d="getArcPath(c)"
        :fill="getCriteriaColor(c.index)"
        @mouseover="hoverCircle(c)"
        @mouseout="hoverOffCircle(c)"
      />
    </template>
    <!-- <circle class="donut-segment" cx="21" cy="21" r="15.91549430918954" fill="transparent" :stroke="getCriteriaColor(c.index)" stroke-width="8" :stroke-dasharray="getStrokeDashArray(c)" :stroke-dashrotation="getStrokeDashrotation(c)" :tooltip="c.name" :title="c.name" @mouseover.stop.prevent="hoverCircle(c)">
          <template v-if="hover">
            <title :id="`segment-${idx}-title`">{{c.name}}</title>
            <desc :id="`segment-${idx}-desc`">{{c.description}}</desc>
          </template>
        </circle> -->
  </svg>
  <!-- </div> -->
</template>

<script>
import { ref, reactive } from "vue";
import chart_colors from "../../../mixins/chart_color";

export default {
  props: {
    criteria: {
      type: Array,
      default: () => [],
    },
    small: {
      type: Boolean,
      default: false,
    },
    score: {
      type: String || Number,
      default: "",
    },
    scale: {
      type: Number,
      default: () => 1.0,
    },
    hover: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    return {
      graphCriteria: reactive(props.criteria),
      hoveredCriteria: ref(null),
    };
  },
  computed: {
    computedCriteria() {
      return this.graphCriteria;
    },
  },
  methods: {
    updateCriteria(newCriteria) {
      let lastIndex = 0;
      for (let c in newCriteria) {
        if (newCriteria[c].index || newCriteria[c].index === 0) {
          if (newCriteria[c].index >= lastIndex) {
            lastIndex = newCriteria[c].index;
          }
        }
      }
      for (let c in newCriteria) {
        if (!newCriteria[c].index && newCriteria[c].index !== 0) {
          lastIndex++;
          newCriteria[c].index = lastIndex;
        }
      }
      this.graphCriteria = reactive(newCriteria);
    },
    getHoveredCriteria() {
      return this.hoveredCriteria;
    },
    getRotatedCoordinates(x, y, rotation, radius, offset) {
      // Need to convert the X and Y to where they'd be rotated x degrees.
      let normalized_rotation = rotation / 100 - 0.25;

      let rotated_y = Math.sin(normalized_rotation * 2 * Math.PI) * radius;
      let rotated_x = Math.cos(normalized_rotation * 2 * Math.PI) * radius;

      rotated_x = rotated_x + offset;
      rotated_y = rotated_y + offset;

      let ret = `${rotated_x} ${rotated_y}`;
      return ret;
    },
    getArcPath(target_criteria) {
      let rotation = 0;
      let totalWeight = 0;
      for (let c of this.graphCriteria) {
        totalWeight += Number(c.weight);
      }
      for (let c of this.graphCriteria) {
        if (c.index == target_criteria.index) {
          break;
        } else {
          if (totalWeight > 0) {
            rotation += (100 * Number(c.weight)) / totalWeight;
          }
        }
      }
      // We're in a 42x42 space.
      let arcDepth = 8;
      let center = 21;
      let outerRadius = center;
      let innerRadius = center - arcDepth;
      let arcAngle = Number((100 * Number(target_criteria.weight)) / totalWeight);
      if (arcAngle == 100) {
        arcAngle = 99.9999;
      }

      // This works by just thinking about each operation on the y-axis, and then "moving" the pointer with the
      // rotation parameter.  Make sure your radius is right, and things should JustWork TM.
      return (
        ` M ${this.getRotatedCoordinates(0, -1 * innerRadius, rotation, innerRadius, center)}` +
        ` L ${this.getRotatedCoordinates(-1 * innerRadius, -1 * outerRadius, rotation, outerRadius, center)}` +
        ` A ${outerRadius}, ${outerRadius}, 0, ${arcAngle > 50 ? 1 : 0}, 1, ${this.getRotatedCoordinates(
          0,
          -1 * outerRadius,
          rotation + arcAngle,
          outerRadius,
          center
        )}` +
        ` L ${this.getRotatedCoordinates(0, -1 * innerRadius, rotation + arcAngle, innerRadius, center)}` +
        ` A ${innerRadius}, ${innerRadius}, 0, ${arcAngle > 50 ? 1 : 0}, 0, ${this.getRotatedCoordinates(
          0,
          -1 * innerRadius,
          rotation,
          innerRadius,
          center
        )}`
      );
    },
    hoverCircle(c) {
      if (this.hover) {
        this.emitter.emit("hovered-criteria", { criteria: c });
      }
    },
    hoverOffCircle() {
      if (this.hover) {
        this.emitter.emit("hovered-criteria", { criteria: null });
      }
    },
    getStrokeDashArray(target_criteria) {
      return (
        String(target_criteria.relative_weight_as_percent) +
        " " +
        String(100 - target_criteria.relative_weight_as_percent)
      );
    },
    getStrokeDashrotation(target_criteria) {
      let baserotation = 25;
      let rotation = 0;
      for (let c of this.graphCriteria) {
        if (c.id == target_criteria.id) {
          break;
        } else {
          rotation += Number(c.relative_weight_as_percent);
        }
      }
      return baserotation - rotation;
    },
    getCriteriaColor(idx) {
      return chart_colors[idx];
    },
  },
};
</script>
