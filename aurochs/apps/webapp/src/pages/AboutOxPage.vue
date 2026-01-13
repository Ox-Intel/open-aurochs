<template>
  <div class="ox-page overflow-hidden">
    <ox-navbar />
    <div class="flex w-full">
      <div class="w-80 p-4">
        <div class="w-64 fixed top-16 left-4">
          <div class="font-bold text-2xl p-4">Ox Guide</div>
          <ul class="menu">
            <li><a href="#whatsox">What's Ox?</a></li>
            <li><a href="#whyuseox">Why use Ox?</a></li>
            <li><a href="#usingoxgpt">Using OxGPT</a></li>
            <li><a href="#howoxusesllms">How Ox uses LLMs</a></li>
          </ul>
        </div>
      </div>

      <div class="pr-16 pr-8 w-full scroll_container overflow-y-auto">
        <article class="prose relative pt-8 pb-20 mt-10 mx-auto">
          <div id="gettingstartedwithox" class="id_anchor"></div>

          <div id="whatsox" class="id_anchor"></div>
          <h2>What's Ox?</h2>

          <p>
            Ox is a versatile assessment tool that pairs decision science with AI to help people improve their judgments
            and decision-making.
          </p>

          <div id="whyuseox" class="id_anchor"></div>
          <h2>Why use Ox?</h2>
          <p>
            Traditional decision-making processes suffer from inefficiencies, bias, and noise. AI can help improve how
            people make judgments but adoption faces numerous barriers:
          </p>

          <ul>
            <li>
              Making decisions is a complex process that usually takes place inside people's heads or in unstructured
              formats.
            </li>
            <li>Subjectivity and disagreement are typical — there is often no clear right answer.</li>
            <li>
              The lack of transparency and inattention to outcomes makes it hard to identify good judgments and learn
              from faulty ones.
            </li>
            <li>Human judgment is important. People don't want to surrender control over decisions to black box AI.</li>
          </ul>

          <p>
            Ox lets individuals and organizations harness AI to strengthen, accelerate, and improve their
            decision-making without surrendering their judgment or control.
          </p>

          <ul>
            <li>
              Ox helps generate frameworks to simplify complex judgments, making the processes behind them transparent,
              transferrable, and easily trainable.
            </li>
            <li>
              Ox takes the headache out of collaborative decision-making — identifying points of agreement and
              disagreement to remove back-and-forth and streamline the path to a decision.
            </li>
            <li>
              Ox builds confidence in decisions by documenting their contributing factors and limiting the impact of
              bias and noise.
            </li>
            <li>
              Ox proactively identifies opportunities to make better judgments, ensuring your process is progressively
              improving.
            </li>
          </ul>

          <div id="usingoxgpt" class="id_anchor"></div>
          <h2>Using OxGPT</h2>

          <p>
            OxGPT leverages the power of large language models to assist users in creating frameworks and making
            assessments. Here's how it works:
          </p>

          <ul>
            <li>
              <b>Framework creation:</b> Think of frameworks as mental models with different criteria for various
              assessments and decisions. OxGPT helps you build and customize frameworks based on your specific needs and
              use cases. Whether it's hiring, risk assessments, or personal choices, Ox supports a wide range of
              scenarios. To get started, tell Ox about the type of judgment you need assistance with. If you want,
              provide some context, such as your job or important criteria, and specify any considerations Ox should
              exclude. OxGPT will then generate an initial framework which you can modify, add to, or remove criteria
              from according to your own best judgment.
            </li>
            <li>
              <b>Setting weights:</b> Once your framework criteria are in place, determine the importance of each
              criterion on a scale of 1-10. This step allows you to fine-tune the significance of the different factors
              within your framework according to your judgment and priorities.
            </li>
            <li>
              <b>Making assessments:</b> When you're ready to make an assessment, name the subject(s) you want to
              analyze, or have Ox generate some options for you, and provide any additional context for Ox to consider.
              OxGPT employs its language models to generate preliminary scores along with explanatory comments. These
              scores can be adjusted or overridden based on your own knowledge and judgment. OxGPT-generated scores will
              be identified as such, unless you make your own edits.
            </li>
            <li>
              <b>Review and Collaboration:</b> Once you're satisfied with the scores and comments, you can click "Finish
              Scoring" to view an overview of your assessment. To delve deeper into Ox's insights, save your work, or
              collaborate with others, click "Save Framework and Scores" to create a free Ox account.
            </li>
          </ul>
          <div id="howoxusesllms" class="id_anchor"></div>
          <h2>How Ox uses LLMs</h2>

          <p>
            Ox is designed to enhance your decision-making journey by leveraging the power of AI, allowing you to make
            informed assessments while maintaining control over the process. Large language models, like those used by
            Ox, are powerful AI systems that have been trained on vast amounts of text data, enabling them to capture a
            wide range of information and knowledge across various domains.
          </p>
          <p>
            These models have a deep understanding of human language and can analyze complex concepts, reason about
            different scenarios, and provide contextual responses. Their power lies in their ability to generate
            human-like text, provide contextually relevant responses, and assist users in various language-related
            tasks. Ox harnesses these capabilities to enhance the creation of frameworks and support users in making
            assessments, enabling more effective and informed decision-making.
          </p>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import OxNavbar from "../components/nav/OxNavbar.vue";

// Font awesome config
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
  padding-bottom: 12rem;
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
