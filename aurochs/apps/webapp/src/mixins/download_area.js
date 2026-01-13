import * as htmlToImage from "html-to-image";

export default {
  methods: {
    async downloadArea(el, name) {
      try {
        if (!name) {
          name = "Ox Export";
        }
        // , width: el.offsetWidth + 0, height: el.offsetHeight + 0, canvasWidth: el.offsetWidth, canvasHeight: el.offsetHeight
        if (Array.isArray(el) != undefined && Array.isArray(el) == true) {
          el = el[0];
        }
        el.classList.add("hideHiddenInExport");
        return htmlToImage.toPng(el).then(function (dataUrl) {
          try {
            // htmlToImage.toPng(el).then(function (dataUrl) {
            var link = el.ownerDocument.createElement("a");
            link.download = `${name}.png`;
            link.href = dataUrl;
            link.click();
          } catch (e) {
            console.error(e);
          }
          el.classList.remove("hideHiddenInExport");
        });
      } catch (e) {
        console.error(e);
        if (Array.isArray(el) != undefined && Array.isArray(el) == true) {
          el = el[0];
        }
        if (el) {
          el.classList.remove("hideHiddenInExport");
        }
        return;
      }
    },
  },
};
