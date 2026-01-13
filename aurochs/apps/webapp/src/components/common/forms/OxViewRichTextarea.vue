<template>
  <div :data-cy="data_cy">
    <QuillEditor
      ref="oxtextarea"
      :content="text"
      theme="bubble"
      :modules="quillOptions.modules"
      :enable="false"
      :read-only="true"
      content-type="delta"
    />
  </div>
</template>

<script>
import JSON5 from "json5";
import { ref } from "vue";
import { QuillEditor } from "@vueup/vue-quill";
import "@vueup/vue-quill/dist/vue-quill.snow.css";
import "@vueup/vue-quill/dist/vue-quill.bubble.css";
import MarkdownShortcuts from "quill-markdown-shortcuts";
import BlotFormatter from "quill-blot-formatter";
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
    content: {
      type: String,
      default: "",
    },
    classes: {
      type: String,
      default: "",
    },
    data_cy: {
      type: String,
      default: "",
    },
  },
  setup(props) {
    const errors = ref(null);
    let text = {};
    try {
      text = JSON5.parse(props.content);
    } catch (e) {
      if (props.content) {
        text = { ops: [{ insert: props.content }] };
      } else {
        text = {};
      }
    }

    const id = Math.random().toString(36);
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
    ];
    const quillOptions = {
      scrollingContainer: ".ox-page",
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
    content(newVal) {
      let parsedNewVal = JSON5.parse(newVal);
      if (this.text != parsedNewVal) {
        this.text = parsedNewVal;
        this.$refs.oxtextarea.setContents(parsedNewVal);
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
      // this.$emit("update:modelValue", this.text);
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
