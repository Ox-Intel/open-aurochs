export default {
  methods: {
    downloadFile(url, filename, extension, data) {
      let base_url = window.location.origin;
      let anchor = document.createElement("a");
      document.body.appendChild(anchor);
      var fetch_data = {};
      fetch_data.headers = new Headers();
      if (data) {
        var form_data = new FormData();
        for (var k in data) {
          form_data.append(k, data[k]);
        }
        fetch_data.body = form_data;
        fetch_data.method = "POST";
        fetch_data.headers["Content-Type"] = "application/json";
      }

      return fetch(base_url + url, fetch_data)
        .then((response) => response.blob())
        .then((blobby) => {
          let objectUrl = window.URL.createObjectURL(blobby);

          anchor.href = objectUrl;
          anchor.download = filename + extension;
          anchor.click();
          window.URL.revokeObjectURL(objectUrl);
        });
    },
    downloadFileAsync(url, filename, extension, data) {
      let base_url = window.location.origin;
      let anchor = document.createElement("a");
      document.body.appendChild(anchor);
      var fetch_data = {};
      fetch_data.headers = new Headers();
      if (data) {
        var form_data = new FormData();
        for (var k in data) {
          form_data.append(k, data[k]);
        }
        fetch_data.body = form_data;
        fetch_data.method = "POST";
        fetch_data.headers["Content-Type"] = "application/json";
      }

      return fetch(base_url + url, fetch_data);
    },
  },
};
