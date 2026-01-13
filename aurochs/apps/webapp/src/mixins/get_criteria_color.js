export default {
  methods: {
    downloadFile(url, filename, extension) {
      let base_url = window.location.origin;
      let anchor = document.createElement("a");
      document.body.appendChild(anchor);
      let headers = new Headers();
      //headers.append("Authorization", `Bearer ${getAuthToken()}`);

      return fetch(base_url + url, { headers })
        .then((response) => response.blob())
        .then((blobby) => {
          let objectUrl = window.URL.createObjectURL(blobby);

          anchor.href = objectUrl;
          anchor.download = filename + extension;
          anchor.click();
          window.URL.revokeObjectURL(objectUrl);
        });
    },
  },
};
