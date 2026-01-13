<template>
  <div class="ox-page overflow-hidden">
    <ox-navbar />
    <!-- <iframe src="https://guide.oxintel.ai/" class="w-full mt-[45px] h-full"></iframe> -->
    <div class="flex w-full">
      <div class="w-80 p-4">
        <div class="w-64 fixed top-16 left-4">
          <div class="font-bold text-2xl p-4">Ox Guide</div>
          <ul class="menu">
            <!-- <h3>Skip ahead to instructions</h3> -->

            <li><a href="#whyuseox">Why use Ox?</a></li>
            <li><a href="#keystufftoknow">Key stuff to know</a></li>
            <li><a href="#usingoxgpt">Using OxGPT</a></li>
            <li><a href="#howoxusesllms">How Ox uses LLMs</a></li>
            <li><a href="#buildingyourfirstframework">Building your first framework</a></li>
            <li><a href="#scoringaframeworkinareport">Scoring a framework in a report</a></li>
            <li><a href="#comparingscorecards">Comparing scorecards</a></li>
            <li><a href="#comparingreportsinastack">Comparing reports in a stack</a></li>
            <li><a href="#exploringframeworkinsights">Exploring framework insights</a></li>

            <!-- <h3>Other helpful info</h3> -->

            <li><a href="#howtousesources">How to use sources</a></li>
            <li><a href="#howtouseyourinbox">How to use your inbox</a></li>
            <li><a href="#behindtheoxapproach">Behind the Ox approach</a></li>
            <li><a href="#understandingnoise">Understanding noise</a></li>
          </ul>
        </div>
      </div>

      <div class="pr-16 pr-8 w-full scroll_container overflow-y-auto">
        <article class="prose relative pt-8 pb-20 mt-20 mx-auto">
          <div id="gettingstartedwithox" class="id_anchor"></div>
          <h1>Getting started with Ox</h1>

          <p>
            Ox is a multi-purpose assessment tool that pairs decision science with AI to help people improve their
            judgments. Here's how to use it.
          </p>
          <!-- 
        <div id="skipaheadtoinstructions" class="id_anchor"></div>
        <h3>Skip ahead to instructions</h3>

        <ul>
        <li><a href="#keystufftoknow">Key stuff to know</a></li>
        <li><a href="#buildingyourfirstframework">Building your first framework</a></li>
        <li><a href="#scoringaframeworkinareport">Scoring a framework in a report</a></li>
        <li><a href="#comparingscorecards">Comparing scorecards</a></li>
        <li><a href="#comparingreportsinastack">Comparing reports in a stack</a></li>
        <li><a href="#exploringframeworkinsights">Exploring framework insights</a></li>
        </ul>

        <div id="otherhelpfulinfo" class="id_anchor"></div>
        <h3>Other helpful info</h3>

        <ul>
        <li><a href="#whyuseox">Why use Ox?</a></li>
        <li><a href="#howtousesources">How to use sources</a></li>
        <li><a href="#howtouseyourinbox">How to use your inbox</a></li>
        <li><a href="#behindtheoxapproach">Behind the Ox approach</a></li>
        <li><a href="#understandingnoise">Understanding noise</a></li>
        </ul>

 -->
          <div id="whyuseox" class="id_anchor"></div>
          <h2>Why use Ox?</h2>

          <p>
            Traditional decision-making processes suffer from inefficiencies, bias, and noise. AI can help improve how
            people make decisions but adoption faces numerous barriers:
          </p>

          <ul>
            <li>
              Making decisions is a complex process that usually take place inside people's heads or in unstructured
              formats.
            </li>
            <li>Subjectivity and disagreement are typical — there is often no clear right answer.</li>
            <li>
              The lack of transparency and inattention to outcomes makes it hard to identify good judgments and learn
              from faulty ones.
            </li>
            <li>
              <span class="highlight">Human judgment is important.</span> People don't want to surrender control over
              decisions to black box AI.
            </li>
          </ul>
          <div class="alert p-4">
            <div class="flex">
              <div class="align-top p-2 mb-4">🐂</div>
              <div>
                <strong
                  >Ox lets individuals and organizations harness AI to strengthen, accelerate, and improve their
                  decision-making without surrendering their judgment or control.</strong
                >
              </div>
            </div>
          </div>

          <ul>
            <li>
              Ox helps simplify complex judgments, making the processes behind them transparent, transferrable, and
              easily trainable.
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

          <div id="keystufftoknow" class="id_anchor"></div>
          <h2>Key stuff to know</h2>

          <ul>
            <li>
              <strong>Ox</strong> is a multi-purpose assessment tool that empowers individuals and teams to make
              high-quality judgments through the use of Ox frameworks.
            </li>
            <li>
              An <strong class="text-ox-score">Ox framework</strong> is a model or formula for making an assessment.
              Frameworks are composed of <strong class="text-ox-score">criteria</strong> — the factors or considerations
              that go into the assessment.

              <ul>
                <li>
                  For example, a framework titled "Job search 2023" might include criteria like "pay," "title," and
                  "opportunities for growth"
                </li>
              </ul>
            </li>
            <li>
              A <strong class="text-report">report</strong> is where you make an assessment, or collect multiple
              assessments, on a specific subject. Reports are composed of
              <strong class="text-report">scorecards</strong> — where users judge the subjects of their assessments by
              scoring their framework criteria from 0-10.

              <ul>
                <li>For example, "XYZ Inc."</li>
              </ul>
            </li>
            <li>
              A <strong class="text-stack">stack</strong> is a group of reports, where you compare assessments of
              different subjects. Stacks show you how reports' scores compare across one or more frameworks.

              <ul>
                <li>For example, "Job opportunities"</li>
              </ul>
            </li>
            <li>
              A <strong class="text-source">source</strong> is an entity used to link reports based on various shared
              characteristics.

              <ul>
                <li>For example, "LinkedIn"</li>
              </ul>
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

          <div id="buildingyourfirstframework" class="id_anchor"></div>
          <h2>Building your first framework</h2>

          <p>
            Think of a framework as your internal formula or mental model for making decisions, assessments, and
            judgments.
          </p>

          <ul>
            <li>Frameworks can be applied to any type of judgment involving evaluation of multiple factors.</li>
            <li>
              You can build your own framework or collaborate with others if you're making a decision with multiple
              stakeholders.
            </li>
            <li>
              Ox users range from intelligence analysts to product managers to investors to people making life
              decisions, such as choosing a new job or apartment.
            </li>
          </ul>

          <p>Unsure where to start? Explore the existing frameworks in your Library for ideas.</p>

          <h3>Step 1: Create a framework using the New dropdown in the top menu.</h3>

          <p>Once you have a judgment in mind, name your framework after it. Examples include:</p>

          <div class="flex">
            <div class="w-1/2">
              <ul>
                <li><p>"Hiring new associate"</p></li>
                <li><p>"Vulnerability risk analysis"</p></li>
                <li><p>"Picking our next vacation"</p></li>
              </ul>
            </div>
            <div class="w-1/2">
              <ul>
                <li><p>"Deciding on my next job"</p></li>
                <li><p>"Quarterly performance review"</p></li>
                <li><p>"Investment diligence"</p></li>
              </ul>
            </div>
          </div>

          <h3>Step 2: Add criteria to your framework.</h3>

          <ul>
            <li>
              Create a criterion that factors into the judgment.

              <ul>
                <li>Examples include: "team fit," "desirable location," "total available market"</li>
                <li>Add an optional description that provides guidance on how to judge it.</li>
                <li>Next, rate the criterion's importance or significance to the overall judgment from 1 to 10.</li>
              </ul>
            </li>
            <li>
              Repeat the above process, creating as many criteria as you want to reflect all the factors and
              considerations that contribute to the judgment. It's entirely up to you how many criteria to include and
              how important you want to rate them.
            </li>
            <li>
              As you continue to add and rate criteria, Ox will automatically calculate their weights, or relative
              importance, to the overall framework, seen in the framework pie chart.
            </li>
          </ul>

          <figure>
            <img :src="image_url('Screenshot 2022-12-08 at 10.53.42 AM.png')" />
            <!-- <figcaption>Screenshot 2022-12-08 at 10.53.42 AM.png</figcaption> -->
          </figure>

          <!-- <div id="step3optional% class="id_anchor"></div> -->
          <h3>Step 3 (Optional): Add other users to your framework.</h3>

          <ul>
            <li>
              If you need other Ox users to weigh in on the framework, go to the Permissions tab to grant them access.

              <ul>
                <li>Anyone added to the report can add comments or questions via the Discussion tab.</li>
                <li><strong>View access</strong> allows users to see the framework but not change anything in it.</li>
                <li>
                  <strong>Edit access</strong> allows users to edit everything in a framework, except for the
                  permissions.
                </li>
                <li>
                  <strong>Admin access</strong> allows users to make any kind of change to a framework, including
                  deleting it and making changes to permissions.
                </li>
              </ul>
            </li>
          </ul>

          <p>Once you've finished adding criteria, your framework is ready to be used in a report.</p>

          <div id="scoringaframeworkinareport" class="id_anchor"></div>
          <h2>Scoring a framework in a report</h2>

          <p>Use a report to evaluate the subject of an assessment or a decision-making option.</p>

          <h3>Step 1: Create a report using the New dropdown in the top menu.</h3>

          <ul>
            <li>
              Reports are focused on and named after the subjects of your assessments.

              <ul>
                <li>Examples include: "Candidate #2," "Vienna," "Stealth-stage startup"</li>
              </ul>
            </li>
            <li>Add any notes or background information you'd like to include in the Notes tab.</li>
          </ul>

          <h3>Step 2: Add a scorecard using your framework.</h3>

          <ul>
            <li>Click +Add Scorecard and select the framework you created to make your assessment.</li>
            <li>
              Using the scoring slider, score each criterion in the framework from 0-10 based on the degree to which the
              subject of the report satisfies it.

              <ul>
                <li>If you're not ready or not able to judge a specific criterion, select Skip.</li>
                <li>Add an optional comment to explain your thinking.</li>
              </ul>
            </li>
            <li>
              Once you've finished and saved your scorecard, you'll see the <strong>Ox score</strong> appear. The Ox
              score captures as a percentage how well the subject of the report satisfies the criteria laid out in the
              framework, weighted according to their relative importance.

              <ul>
                <li>
                  If you skip any of the criteria in the scorecard, your Ox score* will show up in grey with an asterisk
                  flagging it as incomplete.
                </li>
              </ul>
            </li>
          </ul>
          <div class="alert p-4">
            <div class="flex">
              <div class="align-top">
                <FontAwesomeIcon :icon="['fad', 'lightbulb-on']" class="mr-2 w-8 h-8 align-top" />
              </div>
              <div>
                You can always edit your scorecard or add new ones to see how your judgment changes over time, or invite
                others to add their own scorecards with your framework or their own.
              </div>
            </div>
          </div>

          <figure>
            <img :src="image_url('Screenshot 2022-12-12 at 1.59.34 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-12 at 1.59.34 PM.png</figcaption> -->
          </figure>

          <h3><strong>Step 3 (Optional):</strong> Add other users to your report.</h3>

          <ul>
            <li>
              If you need other Ox users to add their own scorecards to the report, go to the Permissions tab to grant
              them access.

              <ul>
                <li>Anyone added to the report can add comments or questions via the Discussion tab.</li>
                <li>
                  <strong>Score-only access</strong> allows users to add their own scorecards but not see other
                  people's.
                </li>
                <li>
                  <strong>View-only access</strong> allows users to see everyone's scorecards but not add their own.
                </li>
                <li>
                  <strong>Edit access</strong> allows users to edit everything in a report, except for the permissions.
                </li>
                <li>
                  <strong>Admin access</strong> allows users to make any kind of change to a report, including deleting
                  it and making changes to permissions.
                </li>
              </ul>
            </li>
          </ul>

          <div id="addanoutcomescore" class="id_anchor"></div>
          <h3>Step 4 (Optional): Add an outcome score.</h3>

          <ul>
            <li>
              If you're later in a position to evaluate the outcome of your assessment, go to the Notes tab and enter an
              Outcome Score to document how well the subject performed against the original assessment.
            </li>
            <li>
              Outcome Score data will help Ox determine the most important criteria for different judgments to help
              reduce bias and improve framework performance.
            </li>
          </ul>

          <div id="comparingscorecards" class="id_anchor"></div>
          <h2>Comparing scorecards</h2>

          <div id="theoverviewtab" class="id_anchor"></div>
          <h3>The Overview tab</h3>

          <ul>
            <li>
              Ox plots users' scores to calculate the average scores for each criterion, producing a weighted average
              bar chart that provides a snapshot of the overall assessment.
            </li>
            <li>
              You can easily compare users' scores and comments by clicking the Comments button, or by clicking the
              scoring plot for individual criteria.

              <ul>
                <li>To see each user's scorecards and comments on their own, head to the Scorecards tab.</li>
              </ul>
            </li>
          </ul>

          <div id="noise" class="id_anchor"></div>
          <h3>Noise</h3>

          <ul>
            <li>
              If there are multiple scorers, Ox identifies the level of criteria noise, or unwanted variability, between
              the judgments.

              <ul>
                <li>Noise may indicate a significant disagreement among scorers or unclear criteria guidance.</li>
                <li>Ox will flag criteria that result in noise and make recommendations for how to reduce it.</li>
                <li>For more on noise, see <a href="#understandingnoise">Understanding noise</a>.</li>
              </ul>
            </li>
          </ul>

          <div id="theaverageoxscore" class="id_anchor"></div>
          <h3>The average Ox score</h3>

          <ul>
            <li>
              At the top of the page, Ox shows the report's average Ox score, based on the average scores and weights
              for all the criteria used in the report.

              <ul>
                <li>
                  If the report has scorecards using multiple frameworks, the average Ox score takes the average of all
                  the frameworks' Ox scores.
                </li>
                <li>
                  If at least one criterion was skipped by all scorers, then the average Ox score* will show up in grey
                  with an asterisk flagging it as incomplete.
                </li>
              </ul>
            </li>
          </ul>

          <figure>
            <img :src="image_url('Screenshot 2022-12-12 at 2.01.28 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-12 at 2.01.28 PM.png</figcaption> -->
          </figure>

          <div id="comparingreportsinastack" class="id_anchor"></div>
          <h2>Comparing reports in a stack</h2>

          <p>
            If your decision involves a comparison of multiple subjects, or you'd just like to see how different reports
            compare across criteria, add the reports to a stack.
          </p>

          <h3>Step 1: Create a stack using the New dropdown in the top menu.</h3>

          <ul>
            <li>
              Name the stack after the decision you're making or the comparison you'd like to see.

              <ul>
                <li>Examples include: "Open engineer role," "Early-stage startups," "Apartment search 2023"</li>
              </ul>
            </li>
            <li>Add any notes or background information you'd like to include in the Notes tab.</li>
          </ul>

          <h3>Step 2: Add the reports you'd like to compare.</h3>

          <ul>
            <li>Click +Add Report and start adding reports to the stack.</li>
          </ul>

          <h3>Step 3: Compare the reports</h3>

          <ul>
            <li>
              In the Overview tab, see how the reports stack up against each other according to their average Ox score.
            </li>
          </ul>

          <figure>
            <img :src="image_url('Screenshot 2022-12-12 at 2.02.17 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-12 at 2.02.17 PM.png</figcaption> -->
          </figure>

          <ul>
            <li>
              In the Frameworks tab, see all the frameworks that were used across the reports, and see how each report
              was scored.

              <ul>
                <li>
                  Ox identifies the average level of noise for criteria across the reports in the stack, accompanied by
                  insights and recommendations.
                </li>
                <li>
                  Toggle to By Report to see the reports' average criteria scores and to By Scorecards to see all the
                  user scores across reports.
                </li>
                <li>Click Comments to compare how users commented on the criteria across different reports.</li>
              </ul>
            </li>
          </ul>

          <figure>
            <img :src="image_url('Screenshot 2022-12-12 at 2.02.28 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-12 at 2.02.28 PM.png</figcaption> -->
          </figure>

          <h3>Step 4 (Optional): Add other users to your stack</h3>

          <ul>
            <li>
              If you'd like to share the stack with other Ox users, go to the Permissions tab to grant them access.

              <ul>
                <li>Anyone added to the stack can add comments or questions via the Discussion tab.</li>
                <li><strong>View access</strong> allows users to see a stack but not change anything in it.</li>
                <li>
                  <strong>Edit access</strong> allows users to edit everything in a stack, except for the permissions.
                </li>
                <li>
                  <strong>Admin access</strong> allows users to make any kind of change to a stack, including deleting
                  it and making changes to permissions.
                </li>
              </ul>
            </li>
          </ul>

          <div id="exploringframeworkinsights" class="id_anchor"></div>
          <h2>Exploring framework insights</h2>

          <p>
            To dive into how you and other users have scored criteria across reports, head to the Explorer tab on the
            Framework page.
          </p>

          <div id="comparecriteriascoringdata" class="id_anchor"></div>
          <h3>Compare criteria scoring data</h3>

          <ul>
            <li>
              Under the Explorer tab, click on different criteria to see all the reports (that you have access to) in
              which the criteria was scored and how.
            </li>
            <li>
              See your average score for each criterion across reports, and explore how it compares to other users'
              scores.
            </li>
            <li>
              Ox identifies the criteria noise levels for each report, as well as their average noise levels across
              reports. Use Ox's suggestions to help refine and improve the framework to reduce consistent noise.
            </li>
          </ul>

          <figure>
            <img :src="image_url('Screenshot 2022-12-12 at 2.09.17 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-12 at 2.09.17 PM.png</figcaption> -->
          </figure>

          <div id="howtousesources" class="id_anchor"></div>
          <h2>How to use sources</h2>

          <p>If you'd like to group reports by source entities, create and add sources to reports.</p>

          <ul>
            <li>
              For example, if you'd like to track the sources of job candidates, "LinkedIn" could be a possible source.
            </li>
          </ul>

          <h3>Step 1: Create a source using the New dropdown in the top menu.</h3>

          <ul>
            <li>Name the source after the entity you'd like to track.</li>
            <li>Add any notes or background information you'd like to include in the Notes tab.</li>
          </ul>

          <h3>Step 2: Linking sources and reports</h3>

          <ul>
            <li>
              On the source page, click +Add Report and select the reports you'd like to associate with the source.
            </li>
            <li>
              To add sources to a report, head to the sources tab on the report page, click +Add Source and select the
              sources you'd like to associate with the report.
            </li>
          </ul>

          <div id="howtouseyourinbox" class="id_anchor"></div>
          <h2>How to use your Inbox</h2>

          <ul>
            <li>
              In the Inbox in your top menu, you'll see notifications for new comments in reports, frameworks, stacks,
              and sources you've created.
            </li>
            <li>
              To get notifications for comments in a piece of content you haven't created, head to the Discussion tab
              and hit +Follow.

              <ul>
                <li>If you no longer want to receive notifications for something, hit Unfollow.</li>
              </ul>
            </li>
            <li>To manage your inbox, mark comments as read or unread, or active or done.</li>
          </ul>

          <div id="behindtheoxapproach" class="id_anchor"></div>
          <h2>Behind the Ox approach</h2>

          <p>
            Ox's structured approach to judgments is one that has been embraced by decision scientists and behavioral
            economists as the best way to combat bias and noise, make more accurate predictions, and integrate
            technology into judgment-making processes.
          </p>

          <div class="flex w-full">
            <div class="p-4">
              <img :src="image_url('noise.jpg')" />
            </div>

            <div class="p-4">
              <img :src="image_url('superforecasting.jpeg')" />
            </div>

            <div class="p-4">
              <img :src="image_url('intel.jpg')" />
            </div>
          </div>

          <p>
            Companies like Google and Atlassian have already adopted structured frameworks for important judgments like
            hiring and performance reviews.
          </p>

          <figure>
            <img :src="image_url('Screenshot 2022-12-08 at 5.34.47 PM.png')" />
            <!-- <figcaption>Screenshot 2022-12-08 at 5.34.47 PM.png</figcaption> -->
          </figure>

          <p>
            Ox is the first solution that empowers users across industries to create shareable frameworks, as well as
            put them into practice. Users' scoring and outcome data then feeds into Ox's AI-driven suggestions, enabling
            continuous improvements of both frameworks and judgments.
          </p>

          <div id="behindourname" class="id_anchor"></div>
          <h3>Behind our name</h3>

          <p>
            In 1907, Francis Galton conducted an experiment where he had attendees at a country fair compete to guess
            the weight of an ox. Galton found that the average of everyone's guesses — approximately 800 of them — was
            closest to the ox's actual weight, and closer than any individual guess, including those from people with
            more familiarity with oxen. This experiment birthed the notion of the wisdom-of-the-crowds effect, but was
            dependent on independent judgments. The more people influenced each other's guesses, the less accurate their
            guesses became, a product of
            <a href="https://www.bbc.com/future/article/20140708-when-crowd-wisdom-goes-wrong" target="_blank"
              >misplaced bias</a
            >.
          </p>

          <p>
            Galton's experiment is the inspiration behind Ox, which seeks to collect data on individual human judgments
            to generate insights based on collective wisdom. Our mission is to leverage these insights to optimize human
            judgment across use cases.
          </p>

          <div id="understandingnoise" class="id_anchor"></div>
          <h2>Understanding noise</h2>

          <div id="whatisnoise" class="id_anchor"></div>
          <h3>What is noise?</h3>

          <p>
            In <em><a href="https://readnoise.com/" target="_blank">Noise: A Flaw in Human Judgment</a></em
            >, authors Daniel Kahneman (a behavioral economist, psychologist, and Nobel prize winner), Olivier Sibony (a
            professor of strategy focused on improving the quality of strategic decision-making), and Cass R. Sunstein
            (a legal scholar and behavioral economist), describe the phenomenon of <strong>noise</strong>, or unwanted
            variability between human judgments.
          </p>

          <p>
            The authors found that noise has detrimental affects across many fields, including medicine, law, economic
            forecasting, strategy, performance reviews, hiring, and intelligence analysis. They explain, "Wherever you
            look at human judgments, you are likely to find noise."
          </p>

          <p>
            Noise, often influenced by cognitive biases or emotional or motivated distortions of thinking, may
            materialize as:
          </p>

          <ul>
            <li>
              <strong>level noise</strong>: two individuals in the same profession making different judgments about the
              same problem despite access to the same information;
            </li>
            <li>
              <strong>pattern noise</strong>: the variance in criteria selection or weighting of factors examined by
              like professionals when making judgments;
            </li>
            <li>
              or <strong>occasion noise</strong>: a single professional exhibiting variance in their judgments based on
              unrelated factors, such as the weather or time of day.
            </li>
          </ul>

          <p>
            All of these types of variability in judgments contribute to system noise, which has wide-ranging
            consequences, such as inconsistent criminal sentencing, inaccurate medical diagnoses, flawed intelligence
            forecasts, and unfair hiring practices. Many industries that suffer from system noise have no ability to
            measure it, and remain ignorant to its deleterious effects and how to address them.
          </p>

          <div id="reducingnoise" class="id_anchor"></div>
          <h3>Reducing noise</h3>

          <p>
            <em>Noise</em>'s authors offer various recommendations for reducing noise for both recurrent judgments and
            singular judgments (those that happen only once), including:
          </p>

          <ul>
            <li>
              <strong>Conduct a noise audit and use a decision observer.</strong> To improve their professional
              judgments, organizations must first document and measure the amount of variability between them. A
              designated decision observer should also observe the assessment-making process and monitor for the
              influence of common biases that may contribute to noise.

              <ul>
                <li>
                  Ox serves as a noise auditing tool that identifies how users differ in their approaches to making
                  judgments and measures the distance between their judgments through the use of simple models, i.e.,
                  <strong class="text-ox-score">Ox frameworks</strong>. By observing this process, Ox is well-placed to
                  make <strong class="text-ox-score">recommendations</strong> on how to limit bias and reduce noise.
                </li>
              </ul>
            </li>
            <li>
              <strong>Structure complex judgments as several independent tasks.</strong> The authors explain that
              breaking down a complex judgment into multiple assessments ensures that each one is evaluated
              independently of the others, limiting the influence of various cognitive biases.

              <ul>
                <li>
                  This is the basis of Ox's <strong>framework-driven approach to making assessments</strong>, which
                  encourages users to identify a set of criteria that act as predictor variables used to predict a
                  target outcome and then assess them individually. According to <em>Noise</em>, the use of simple
                  models like frameworks outperforms case-by-case human judgment as well as more complex models that
                  attempt to capture subtleties in judgment.
                </li>
              </ul>
            </li>
            <li>
              <strong>Aggregate independent judgments from multiple judges.</strong> The authors cite
              <a href="#behindourname">Francis Galton's ox experiment</a>, which found that averaging independent
              judgments of multiple people generally improves accuracy, otherwise known as the wisdom-of-the-crowds
              effect. In the context of noise, the authors found that averaging several independent judgments yields a
              new judgment that is less noisy than the individual judgments.

              <ul>
                <li>
                  Ox takes its name and inspiration from the experiment that discovered the wisdom of the crowds. It is
                  designed to enable users to make independent judgments for the same assessment (using either shared or
                  independent frameworks), collected in the form of
                  <a href="#scoringaframeworkinareport">report scorecards</a>. Ox then automates aggregation of these
                  independent judgments via the <a href="#theaverageoxscore">average Ox score</a>.
                </li>
              </ul>
            </li>
            <li>
              <strong>Leverage AI on top of simple models.</strong> The authors of <em>Noise</em> found that ML can be
              leveraged on top of simple models to identify significant signal in combinations of variables (i.e.,
              criteria) that might otherwise be missed.

              <ul>
                <li>
                  By collecting information on how users across industries identify and score criteria in the course of
                  making their judgments, Ox will be able to make informed recommendations on which combination of
                  criteria demonstrate the highest level of predictability for different users and use cases. In this
                  way, Ox offers critical bridging technology that allows organizations to harness AI to strengthen,
                  accelerate, and improve their judgments without surrendering their expertise or control.
                </li>
              </ul>
            </li>
          </ul>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
import OxNavbar from "../components/nav/OxNavbar.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faLightbulbOn } from "@fortawesome/pro-duotone-svg-icons/faLightbulbOn";

library.add(faLightbulbOn);

export default {
  components: {
    OxNavbar,
    FontAwesomeIcon,
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
