<template>
  <div class="" data-cy="release-notes">
    <div class="relative">
      <label data-cy="close" for="release-notes-modal" class="btn btn-sm btn-circle fixed right-12 top-8">
        <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle text-base-100 fa-swap-opacity" />
      </label>
    </div>
    <h3 class="text-4xl font-bold">
      <FontAwesomeIcon :icon="['fad', 'rocket-launch']" class="mr-2 mb-2 align-middle text-ox-score" />
      Release Notes
    </h3>
    <article class="prose max-w-none">
      <p class="mt-4">
        We regularly release new versions of Ox to make it better, more useful, and fix any outstanding bugs. Below are
        the most recent improvements.
      </p>

      <h2>Release 58: July 7, 2023</h2>
      <p>
        This is a transformative release that adds generative AI to Ox, allowing you to much more easily create
        frameworks, conduct assessments, and make decisions by leveraging the power of large language models.
      </p>

      <ul>
        <li>
          <b>OxGPT Beta.</b> We've built a bespoke generative AI system to help you create and score frameworks in
          reports and stacks in a simple, easy-to-use flow. Click the purple OxGPT button in the top bar to get started!
          As this feature is still in beta, please contact us with your feedback so we can continue to improve your
          experience.
        </li>
        <li>
          <b>Bugfixes.</b> We've also found and fixed a couple of bugs, including minor issues with deleting reports and
          adding users to organizations.
        </li>
      </ul>

      <h2>Release 57: February 20, 2023</h2>
      <p>
        We’ve updated and improved exports across the app, giving you the ability to get your insights and data out of
        Ox, and into your work.
      </p>

      <ul>
        <li>
          <b>Overhauled Report PDFs.</b> PDFs have been completely redone for reports, using the new Ox visual language,
          and a streamlined UI for generation. They should also export much faster, even on very large reports.
        </li>
        <li>
          <b>New Stack PDFs.</b> You can now also export a PDF for your stacks, creating a clean way to share how
          reports and scorecards compare.
        </li>
        <li>
          <b>New CSV exports.</b> We've added CSV export support to reports and stacks, in addition to existing exports
          for frameworks. We've always wanted to make sure you can get all of your data out of Ox in a format that's
          useful, and this is a big step toward that goal.
        </li>
        <li>
          <b>Improved image exports.</b> We've completely reworked how image exports work, and expanded them across the
          Ox platform. Now, on pretty much any page, if you see a visual, you'll also see a download link to export a
          PNG image of exactly what's on your screen.
        </li>
        <li>
          <b>Bugfixes.</b> We've also found and fixed a couple of bugs, including minor issues with outcome score
          display and graph sizing on the dashboard.
        </li>
      </ul>

      <h2>Release 56: January 11, 2023</h2>
      <ul>
        <li>
          <b>Real-time sync.</b> We've re-built Ox's sync engine to give you real-time syncing across your team and all
          open browsers. No more refreshing to see the latest - it's always up to date.
        </li>
        <li>
          <b>Much, much faster Ox.</b> Performance has been improved all across Ox, making your saves, edits, comments,
          and changes all happen in less than a second.
        </li>
        <li>
          <b>More intuitive permissions.</b> We've changed the way permissions work on Stack and Reports to include
          items within a given stack or report, even if a user doesn't have specific permissions for the included
          object. So, when making and sharing a Stack or Report, you no longer have to go through each contained
          Framework or Report and add each team member to them.
        </li>
        <li>
          <b>New Ox Guide.</b> We've added an Ox guide to the top menu bar, to help you learn how to use Ox in your
          projects.
        </li>
        <li>
          <b>Moved Teams.</b> With the addition of the Ox Guide, we've moved Teams and Organizations to the user menu in
          the top right.
        </li>
        <li>
          <b>Bugfixes.</b> We've also found and fixed a couple of bugs, including issues related to graphs with skipped
          scores, and a rare case where complex frameworks would fail to show changes until they were refreshed.
        </li>
      </ul>

      <h2>Release 55: November 24, 2022</h2>
      <ul>
        <li>
          <b>Comments everywhere.</b> We redesigned the overview in reports and stacks to enable you to drill down into
          comments and easily get a deeper understanding of the context around a given score.
        </li>
        <li>
          <b>Skip scores.</b> You can now explicitly skip scoring for individual criteria in all scorecards, marking or
          resetting the scores as N/A. (Details below.)
        </li>
        <li>
          <b>Streamlined Scorecards.</b> We combined the "All Scorecards" and "My Scorecards" tabs in reports, and
          redesigned how they work to make it simpler and easier to find and understand your scorecards.
        </li>
        <li>
          <b>Enhanced dark mode and other quality-of-life improvements.</b> We improved the readability of text and
          visibility of scroll bars in dark mode. We also made a handful of other design improvements to make Ox's UI
          clean, consistent, and more visually communicative.
        </li>
        <li>
          <b>Bugfixes.</b> There were a few assorted bugs throughout Ox. We've fixed all the ones we know about,
          including a notable addition that clarifies visibility for reports in which users do not have the necessary
          permissions to see all scorecards.
        </li>
      </ul>

      <h4>Details on score skipping:</h4>
      <p>
        We've aimed to make skipping simple, while still keeping the Ox score intuitive and valuable. Here's how it
        works.
      </p>
      <p>
        When a scorecard contains a skipped score, you'll see its Ox score turn grey, and the score will be flagged with
        an asterisk. This also bubbles up to reports - if a particular criterion has been skipped in
        <b>all</b> scorecards, the entire report is flagged with a grey Ox score and an asterisk.
      </p>

      <p>
        In cases where only <b>some</b> scorecards have skipped a score, the Ox score for a report is calculated using
        the average of all provided scores.
      </p>
      <p>When calculating the Ox score, we treat any criteria that is unscored (all scorers skipped) as zero.</p>
      <h2>Release 54: November 15, 2022</h2>

      <p>This release is all about meaningful quality-of-life improvements across Ox.</p>
      <ul>
        <li>
          <b>User avatars.</b> User avatars are unique, and all across Ox, including in Report, Stack, and Framework
          graphs.
        </li>
        <li>
          <b>Notes tab.</b> All Frameworks, Reports, Stacks, and Sources now include a Notes tab, where you can leave
          notes and documentation for your work, including images and hyperlinks.
        </li>
        <li>
          <b>Subtitles.</b> All objects now have a consistent title and subtitle, to help you easily identify and
          clarify their purpose. We've moved existing description content to the notes field.
        </li>
        <li>
          <b>Permissions tab.</b> We moved permissions to its own tab to make it easier to see and edit all of an
          object's viewers, editors, and administrators. We've also added the object's owners to the bottom of each
          page, and linked those to permissions.
        </li>
        <li>
          <b>Improved search.</b> Search is faster and more powerful, allowing you to use multiple terms, and search for
          items in stacks.
        </li>
        <li>
          <b>Quick-linked Stacks.</b> Stack badges on reports help you quickly navigate back to their associated Stacks,
          or add a report to a stack.
        </li>
        <li>
          <b>Even more quality-of-life improvements.</b> Adding frameworks or tags now shows your most recently used
          ones first. Owners and change dates are listed at the bottom of all object pages. Reports are now identified
          in scoring graphs in both Framework and Stacks.
        </li>
        <li>
          <b>Bugfixes.</b> There were a few assorted bugs throughout Ox. We've found and fixed all the ones we know
          about.
        </li>
      </ul>

      <h2>Release 53: November 1, 2022</h2>

      <p>Stacks are here! We've added a new core feature to Ox: Stacks.</p>
      <ul>
        <li>
          <b>Stacks.</b> You can now group a set of reports together, compare their Ox Scores, and dig into the
          scorecards, frameworks, and trends. Ideal for comparing between several assessments (hiring, vendors,
          software, or any zero-sum choice), stacks make it easy to understand a decision, stakeholder perspectives, and
          the points that need more consensus.
        </li>
        <li>
          <b>Simplified Library.</b> With the addition of Stacks, we've also simplified the library into two panes: one
          for your things and one for things you share with your teams, orgs, and other Ox users.
        </li>
        <li>
          <b>New Dashboard.</b> We've also reworked the dashboard entirely to surface your most recent Frameworks,
          Reports, and Stacks, and helping you easily get back to what you're actively working on, or start something
          new.
        </li>
        <li>
          <b>New Graphs.</b> We've added a new view to our scoring graph to allow you to visually see all scores stacked
          together. This makes it much simpler to understand trends and patterns of scoring. We've simplified the
          average display, giving you a single line at the average of all scores.
        </li>
        <li>
          <b>Improved UI.</b> Ox has been simplified, clarified, and improved throughout. From things like the
          overhauled framework explorer, to a new dark/light/auto mode toggle, to small spacing and alignment fixes
          throughout, we've streamlined Ox to make it a place you'll be even happier to spend time.
        </li>
        <li>
          <b>Follow by default, clearer ownership.</b> When you create a new item, Ox now defaults you to following the
          conversation. We've also surfaced the owners for a particular item, so you know who can share and
          administrate.
        </li>
        <li>
          <b>Bugfixes.</b> There were a few assorted bugs throughout Ox. We've found and fixed all the ones we know
          about.
        </li>
      </ul>

      <h2>Release 52: October 2022</h2>

      <p>This release focuses on small improvements, as we work toward the next big Ox release.</p>
      <ul>
        <li>
          <b>Score-only permissions for reports.</b> You can now limit users to score-only permission for a report to
          facilitate independent, blind scoring for a given report.
        </li>
        <li>
          <b>Ox suggestions across reports.</b> We now display Ox suggstions in the framework explorer across all
          reports, to help you understand how best to improve criteria, and your processes around scoring.
        </li>
        <li>
          <b>Simplified reports.</b> We've combined the analytic question and description fields, to make creating and
          sharing reports more intuitive.
        </li>
        <li>
          <b>Track clone parents.</b> We're now tracking the parent of all cloned frameworks, to help surface
          relationships down the road.
        </li>
        <li><b>Bugfixes.</b> We've found and fixed a small number of bugs within Ox.</li>
      </ul>
      <h2>Release 51: September 2022</h2>

      <p>This release focuses on making Ox faster, stronger, and more reliable.</p>
      <ul>
        <li>
          <b>Speed.</b> Significant improvements in page load speed and navigation. You should now see Ox load in less
          than a second, and switching between pages should be instant.
        </li>
        <li>
          <b>Defaults new criteria to 5.</b> We noticed that knowing what value to set for a criteria's importance was
          tripping up a numbers of users, so we now default new criteria to the same weight - 5/10. You can still set
          the importance as you see fit.
        </li>
        <li>
          <b>Bugfixes.</b> We added significant automated testing to Ox, and in the process found a fixed a number of
          small bugs thoughout the app.
        </li>
      </ul>

      <h2>Ox 2.0 - Release 50: August 2022</h2>

      <p>Welcome to the new Ox!</p>

      <p>
        We've built a new and improved UI that cleans up the entire interface and adds new visualizations, tabs, and
        features throughout. In particular, the new report and scorecards make it much easier for you to visualize,
        compare, and improve your judgments. There are also a host of brand new features, including:
      </p>

      <b>New Features:</b>
      <ul>
        <li>
          <b>New Report Visualizations.</b> Ox reports now include new tabs and visualizations that compare user scores
          and comments, identify low/medium/high levels of scoring noise (variance between user scores), and show
          weighted confidence for criteria.
        </li>

        <li>
          <b>Ox Smart Suggestions.</b> Under the Overview tab in reports, Ox flags criteria with low, medium, and high
          noise, and provides suggestions for how to reduce noise.
        </li>

        <li>
          <b>New Scorecards.</b> All-new tools for creating and editing scorecards that lets you easily manage your
          scorecards, and compare scores and comments across users in a report.
        </li>

        <li>
          <b>Explorer.</b> On framework pages, you can now use the Explorer tab to compare how you and other users have
          scored individual criteria across different reports. You can also see Ox Smart Suggestions, criteria noise,
          and suggestions for how to reduce it.
        </li>

        <li>
          <b>Team and Organization Management.</b> You can now create and manage teams, approve administrators, and add
          new users to your Ox org from the Teams page.
        </li>

        <li>
          <b>Permissions.</b> Permissions have been overhauled to make sharing easier and more granular. You can now
          customize permissions for each framework, source, and report, granting specific users and teams read, write,
          and administrative access.
        </li>

        <li>
          <b>Global Search.</b> Ox now has global search in the top bar, where you can search for Ox content by name or
          tag, and navigate to results from a dropdown list. Keyboard shortcuts are included, so you can switch between
          pages without ever reaching for the mouse.
        </li>

        <li><b>Dark Mode.</b> You can now choose between a light mode and a dark mode for Ox's interface.</li>

        <li>
          <b>Discussion Participants.</b> Under the Discussion tab of sources, reports, and frameworks, you can now see
          who is in the conversation, with a list of all user who have commented or are following the discussion.
        </li>

        <li>
          <b>Source Keyword Search.</b> When adding sources to a report, you can now more easily find the sources you‘re
          looking for with a keyword search bar.
        </li>
      </ul>

      <h2>Release 49: June 16, 2022</h2>

      <b>New Features:</b>
      <ul>
        <li><b>Discussion:</b> A new discussion section has been added to frameworks, reports, and sources.</li>
        <li>
          <b>Follow:</b> Users can follow (subscribe) to discussions in frameworks, reports, and sources in order to
          receive notifications for new comments.
        </li>
        <li>
          <b>Inbox:</b> Ox now has a built-in inbox, where users are notified of any new comments in followed
          discussions. Users can mark things as Read/Unread or as Done to archive them in a separate folder.
        </li>
        <li>
          <b>Tags:</b> Users can now tag any framework, source, or report with one or more tags, and click to find
          everything that shares a specific tag. Tags are also searchable in the Activity section of the Dashboard.
        </li>
        <li>
          <b>Customizable PDF Exports:</b> For report PDF exports, users can now change the organization name, logo,
          color theme, and add distribution guidance or classification level.
        </li>
        <li>
          <b>Bugfixes:</b> Speed and reliability have been improved throughout Ox, in addition to fixes for a few rare
          bugs.
        </li>
      </ul>

      <h2>Release 48: May 1, 2022</h2>

      <b>New Features:</b>
      <ul>
        <li>
          Next-generation application backend, to enable rapid buildout of new features, more robust permissioning, and
          ML and AI support.
        </li>
        <li>Much faster application load times.</li>
        <li>Allows multiple scorecards to be added to and removed from a report.</li>
        <li>Allows multiple sources to be added to and removed from a report.</li>
        <li>Allows unlimited text into any field. (No more 255 character limit.)</li>
        <li>Streamlined framework add and removes from a report.</li>
        <li>Moves organization, team and user management features to a dedicated administration console.</li>
      </ul>

      <b>Bugfixes:</b>
      <ul>
        <li>Ensures consistent display and scaling of criteria importance (formerly "weight").</li>
      </ul>

      <h2>Release 47: April 7, 2022</h2>

      <b>New Features:</b>
      <ul>
        <li>
          Reworked Framework view and edit page to make framework creation and modification much easier, more visual and
          more intuitive.
        </li>
        <li>Clone Framework feature, to allow users to easily clone existing frameworks.</li>
        <li>
          Adds CSV export for framework. The current implementation is keyed around having each row be self-contained
          for ease of machine import. Please provide feedback on format changes that would ease data interchange!
        </li>
        <li>Changes criteria importance to a 1-10 scale, normalizes previous criteria by dividing by 10.</li>
        <li>Adds the ability to remove a framework from a report.</li>
        <li>Adds confirmation dialogs for destructive actions (delete, destructive edits.)</li>
        <li>Reduces the UI functionality for superusers to only team and user management.</li>
      </ul>

      <b>Bugfixes:</b>
      <ul>
        <li>Fixes an incorrect average for a user's criteria score on the dashboard.</li>
        <li>Fixes the password complexity check to allow much more complex passwords with more special characters.</li>
        <li>Fixes PDF generation for very large PDFs.</li>
        <li>Fixes a bug where login expiration gave a blank screen instead of returning the user to the login page.</li>
        <li>Fixes a bug where team data was not saved if a team lead was missing.</li>
        <li>Fixes related bugs with missing teams in source and framework.</li>
        <li>Fixes a save bug for new sources in brand-new organizations.</li>
        <li>Ensures that scorecard comment field auto-expands to fit the user's text.</li>
      </ul>
    </article>
  </div>
</template>

<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";

import { faRocketLaunch } from "@fortawesome/pro-duotone-svg-icons/faRocketLaunch";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";

library.add(faRocketLaunch, faXmark);

export default {
  components: {
    FontAwesomeIcon,
  },
  setup() {},
};
</script>
