<template>
  <div class="ox-page overflow-hidden">
    <ox-navbar />
    <div class="flex w-full mt-28">
      <div class="w-2/3 mx-auto p-4">
        <div class="card text-center bg-base-200 max-w-screen-md w-screen-md mx-auto">
          <article class="prose relative pt-8 pb-16 mt-10 mx-auto">
            <h1>Organizations and Teams are available for Enterprise customers.</h1>
            <p>
              Interested in how Ox can help your organization make assessments? Join other leading organizations and
              governmental institutions and <a href="mailto:info@oxintel.ai">get in touch</a> with our team to get set
              up with an org account and explore custom integration opportunities.
            </p>

            <a href="mailto:info@oxintel.ai" class="mx-auto btn btn-primary btn-lg mt-8">Contact Ox</a>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import OxNavbar from "../components/nav/OxNavbar.vue";

// // Font awesome config
// import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
// import { library } from "@fortawesome/fontawesome-svg-core";
// // Skip the tree-shaking that slows down build by deep-importing, and get better errors.
// import { faLightbulbOn } from "@fortawesome/pro-duotone-svg-icons/faLightbulbOn";

// library.add(faLightbulbOn);

export default {
  components: {
    OxNavbar,
    // FontAwesomeIcon,
  },
  mounted() {
    document.title = "Ox Guide";
  },
  methods: {
    image_url(file_name) {
      let url =
        window.aurochs.data.config.guide_image_url.substring(
          0,
          window.aurochs.data.config.guide_image_url.indexOf("/intel") + 1
        ) +
        file_name
          .replaceAll(" ", "_")
          .replaceAll("%20", "_")
          .replaceAll("-", "-")
          .replaceAll("-", "-")
          .replaceAll("%E2%80%93", "-");
      return url;
    },
  },
};
</script>
<style scoped>
.id_anchor {
  display: block;
  position: relative;
  top: -4rem;
  visibility: hidden;
}
article {
}
.highlight {
  background: #fff4bd;
}
[data-theme="dark"] .highlight {
  background: #30b89d;
  padding: 0 4px;
  /*  color: #000;*/
}
.scroll_container {
  height: 100vh;
}
</style>
