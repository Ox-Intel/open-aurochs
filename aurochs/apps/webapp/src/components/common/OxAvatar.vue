<template>
  <!-- -->
  <div class="relative inline-block mask mask-circle" :class="sizeClasses">
    <div class="absolute top-0 left-0">
      <div class="h-10 w-10 absolute top-0 left-0" :style="`background-color: ${bgColor}`"></div>
      <div class="relative w-full h-full place-content-center place-items-center">
        <div
          class="z-50 text-white shadow-inner text-center"
          :class="
            tiny
              ? 'w-4 h-4 text-[0.6rem] pt-[0.045rem] font-bold opacity-[85%]'
              : small
              ? 'w-6 h-6 text-xs pt-[0.21rem] font-bold opacity-[85%]'
              : 'w-10 h-10 text-xl pt-1.5 font-light opacity-90'
          "
        >
          {{ user?.full_name.slice(0, 1) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      default: () => {},
    },
    tiny: {
      type: Boolean,
      default: () => false,
    },
    small: {
      type: Boolean,
      default: () => false,
    },
  },
  computed: {
    avatarColors() {
      // return [
      //   "hsl(251,32.7%,41.4%)",
      //   "hsl(207,55.6%,38.8%)",
      //   "hsl(191,95.3%,33.7%)",
      //   "hsl(172,86.5%,37.6%)",
      //   "hsl(158,81.7%,47.3%)",
      //   "hsl(113,65.9%,67.8%)",
      //   "hsl(82,72.4%,65.9%)",
      //   "hsl(58,82.3%,64.5%)",
      //   "hsl(43,84.9%,63.5%)",
      //   "hsl(30,86.5%,62.4%)",
      // ]
      // return ["#2d728f","#3b8ea5","#f5ee9e","#f49e4c","#ab3428"]
      // return ["#92A1C6", "#146A7C", "#F0AB3D", "#C271B4", "#C20D90"]
      // return ["#92A1C6", "#146A7C", "#F0AB3D", "#C271B4", "#0d97c2", "#C20D90"];
      return ["#395a50", "#432430", "#853c43", "#f25c5e", "#0d97c2"];
      // return ["#323031","#3d3b3c","#7f7979","#c1bdb3","#5f5b6b"]
      // return [  "hsl(251,32.7%,41.4%)","hsl(158,81.7%,47.3%)","hsl(58,82.3%,64.5%)",]
    },
    darkMode() {
      return !localStorage.getItem("theme");
    },
    sizeClasses() {
      if (this.small) {
        return "w-6 h-6 p-1";
      }
      if (this.tiny) {
        return "w-4 h-4 p-0.5";
      }
      return "w-10 h-10 p-2";
    },
    avatarSize() {
      if (this.small) {
        return 24;
      }
      if (this.tiny) {
        return 16;
      }
      return 48;
    },
    bgColor() {
      // let seed = this.user?.id;
      // if (!seed) {
      //   seed = this.user.full_name;
      // }
      let colors = [
        "hsl(200, 30%, 80%)",
        "hsl(200, 30%, 70%)",
        "hsl(200, 30%, 60%)",
        "hsl(200, 30%, 50%)",
        "hsl(200, 30%, 40%)",
        "hsl(200, 30%, 30%)",
        "hsl(200, 30%, 20%)",

        "hsl(225, 30%, 80%)",
        "hsl(225, 30%, 70%)",
        "hsl(225, 30%, 60%)",
        "hsl(225, 30%, 50%)",
        "hsl(225, 30%, 40%)",
        "hsl(225, 30%, 30%)",
        "hsl(225, 30%, 20%)",

        "hsl(180, 30%, 80%)",
        "hsl(180, 30%, 70%)",
        "hsl(180, 30%, 60%)",
        "hsl(180, 30%, 50%)",
        "hsl(180, 30%, 40%)",
        "hsl(180, 30%, 30%)",
        "hsl(180, 30%, 20%)",
      ];

      return colors[this.user.color_index];
    },
  },
};
</script>
