export default {
  methods: {
    formatDate(time) {
      const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const date = new Date(time);

      return `${months[date.getUTCMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
    },
  },
};
