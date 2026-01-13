export default {
  methods: {
    trimNumber(num) {
      if (!num && num !== 0) {
        return "N/A";
      }
      if (num % 1 === 0) {
        return Math.round(num);
      }
      return Number(num).toFixed(1);
    },
  },
};
