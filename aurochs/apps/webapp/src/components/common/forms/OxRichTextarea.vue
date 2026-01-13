<template>
  <div :data-cy="data_cy">
    <QuillEditor
      ref="oxtextarea"
      v-model:content="text"
      :options="quillOptions"
      :toolbar="quillOptions.toolbarOptions"
      :modules="quillOptions.modules"
      theme="snow"
      content-type="delta"
      @text-change="handleInput"
    />
  </div>
</template>

<script>
import JSON5 from "json5";
import { ref } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import MarkdownShortcuts from "quill-markdown-shortcuts";
import BlotFormatter from "quill-blot-formatter";
import ImageUploader from "quill-image-uploader";

import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "@vueup/vue-quill/dist/vue-quill.bubble.css";
// Font awesome config
// import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
// import { library } from "@fortawesome/fontawesome-svg-core";
// // Skip the tree-shaking that slows down build by deep-importing, and get better errors.
// import { faCircleExclamation } from "@fortawesome/pro-duotone-svg-icons/faCircleExclamation";

// library.add(faCircleExclamation);

export default {
  components: {
    // FontAwesomeIcon,
    QuillEditor,
  },
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    size: {
      type: String,
      default: "sm",
    },
    classes: {
      type: String,
      default: "",
    },
    data_cy: {
      type: String,
      default: "",
    },
    target: {
      type: Object,
      default: () => {},
    },
  },
  emits: ["update:modelValue"],
  setup(props) {
    const errors = ref(null);
    let text = {};
    try {
      text = JSON5.parse(props.modelValue);
    } catch (e) {
      if (props.modelValue) {
        text = { ops: [{ insert: props.modelValue }] };
      } else {
        text = {};
      }
    }
    const id = Math.random().toString(36);
    var toolbarOptions = [
      ["bold", "italic", "underline", "strike"], // toggled buttons

      [{ header: 1 }, { header: 2 }], // custom button values
      [{ list: "ordered" }, { list: "bullet" }],
      [{ align: [] }],
      [{ indent: "-1" }, { indent: "+1" }], // outdent/indent
      ["link", "image", "video", "blockquote", "code-block"],
      // [{ 'direction': 'rtl' }],                         // text direction

      // [{ 'size': ['small', false, 'large', 'huge'] }],  // custom dropdown
      [{ script: "sub" }, { script: "super" }], // superscript/subscript
      [{ header: [1, 2, 3, 4, 5, 6, false] }],

      // [{ 'color': [] }, { 'background': [] }],          // dropdown with defaults from theme
      // [{ 'font': [] }],

      ["clean"], // remove formatting button
    ];
    const modules = [
      {
        name: "markdownShortcuts",
        module: MarkdownShortcuts,
        options: {
          /* options */
        },
      },
      {
        name: "blotFormatter",
        module: BlotFormatter,
        options: {
          /* options */
        },
      },
      {
        name: "imageUploader",
        module: ImageUploader,
        options: {
          upload: function (file) {
            return new Promise((resolve, reject) => {
              let formData = new FormData();
              formData.append("ox_id", props.target.id);
              formData.append("object_type", props.target.__type);
              formData.append("file", file);

              fetch(window.aurochs.data.config.file_path, {
                method: "POST",
                body: formData,
              })
                .then((response) => response.json())
                .then((result) => {
                  resolve(result.url);
                })
                .catch(() => {
                  reject("Error uploading");
                });
            });
          },
        },
      },
    ];

    const quillOptions = {
      scrollingContainer: ".ox-page",
      toolbarOptions: toolbarOptions,
      formats: [
        // "background", // Color
        "bold", // Bold
        // "color", // Color
        "font", // Font
        "code", // Inline Code
        "italic", // Italic
        "link", // Link
        "size", // Size
        "strike", // Strikethrough
        "script", // Superscript/Subscript
        "underline", // Underline

        "blockquote", // Blockquote
        "header", // Header
        "indent", // Indent
        "list", // List
        "align", // Text Alignment
        "direction", // Text Direction
        "code-block", // Code Block

        "formula", // Formula (requires KaTex)
        "image", // Image
        "video", // Video
      ],
      modules: modules,
    };

    return {
      errors,
      text: ref(text),
      id,
      quillOptions,
    };
  },
  computed: {
    sizeClasses() {
      return `textarea-${this.size} text-${this.size}`;
    },
  },
  watch: {
    modelValue(newVal) {
      if (this.text != newVal) {
        this.text = newVal;
        this.$refs.oxtextarea.value = newVal;
        this.$refs.oxtextarea.innerHTML = newVal;
        // this.resize();
      }
    },
  },
  mounted() {
    this.resize();
  },
  methods: {
    resize() {
      // let ele = this.$refs.oxtextarea;
      // console.log(ele)
      // console.log(ele?.editor.$refs)
      // if (ele?.editor) {
      //   ele.editor.style.height = "18px";
      //   ele.editor.style.height = (ele.editor.scrollHeight + 40) + "px";
      // }
    },
    handleInput() {
      // console.log(event)
      // console.log(this.text)
      // console.log(this.text)
      this.$emit("update:modelValue", JSON5.stringify(this.text));
      // this.resize();
    },
  },
};
</script>

<style scoped>
textarea {
  resize: none;
  overflow: hidden;
}
textarea:focus {
  outline: none;
}
.ql-editor,
.ql-container {
  height: auto;
  min-height: 8rem;
}
</style>
