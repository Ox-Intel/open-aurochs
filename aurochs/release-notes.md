Ox Release Notes:

### Release 58: July 7, 2023
This is a transformative release that adds generative AI to Ox, allowing you to much more easily create frameworks, conduct assessments, and make decisions by leveraging the power of large language models.

- OxGPT Beta. We've built a bespoke generative AI system to help you create and score frameworks in reports and stacks in a simple, easy-to-use flow. Click the purple OxGPT button in the top bar to get started! As this feature is still in beta, please contact us with your feedback so we can continue to improve your experience.
- Bugfixes. We've also found and fixed a couple of bugs, including minor issues with deleting reports and adding users to organizations.

### Release 57: February 20, 2023
We’ve updated and improved exports across the app, giving you the ability to get your insights and data out of Ox, and into your work.

- Overhauled Report PDFs.  PDFs have been completely redone for reports, using the new Ox visual language, and a streamlined UI for generation. They should also export much faster, even on very large reports.
- New Stack PDFs.  You can now also export a PDF for your stacks, creating a clean way to share how reports and scorecards compare.
- New CSV exports. We've added CSV export support to reports and stacks, in addition to existing exports for frameworks. We've always wanted to make sure you can get all of your data out of Ox in a format that's useful, and this is a big step toward that goal.
- Improved image exports.  We've completely reworked how image exports work, and expanded them across the Ox platform. Now, on pretty much any page, if you see a visual, you'll also see a download link to export a PNG image of exactly what's on your screen.
- Bugfixes.  We've also found and fixed a couple of bugs, including minor issues with outcome score display and graph sizing on the dashboard.


### Release 56: January 11, 2023
- Real-time sync.  We've re-built Ox's sync engine to give you real-time syncing across your team and all open browsers.  No more refreshing to see the latest - it's always up to date.
- Much, much faster Ox.  Performance has been improved all across Ox, making your saves, edits, comments, and changes all happen in less than a second.
- More intuitive permissions.  We've changed the way permissions work on Stack and Reports to include items within a given stack or report, even if a user doesn't have specific permissions for the included object.  So, when making and sharing a Stack or Report, you no longer have to go through each contained Framework or Report and add each team member to them.
- New Ox Guide.  We've added an Ox guide to the top menu bar, to help you learn how to use Ox in your projects.
- Moved Teams.  With the addition of the Ox Guide, we've moved Teams and Organizations to the user menu in the top right.
- Bugfixes. We've also found and fixed a couple of bugs, including issues related to graphs with skipped scores, and a rare case where complex frameworks would fail to show changes until they were refreshed.

### Release 55: November 24, 2022
- Comments everywhere. We redesigned the overview in reports and stacks to enable you to drill down into comments and easily get a deeper understanding of the context around a given score.
- Skip scores. You can now explicitly skip scoring for individual criteria in all scorecards, marking or resetting the scores as N/A. (Details below.)
- Streamlined Scorecards. We combined the "All Scorecards" and "My Scorecards" tabs in reports, and redesigned how they work to make it simpler and easier to find and understand your scorecards.
- Enhanced dark mode and other quality-of-life improvements. We improved the readability of text and visibility of scroll bars in dark mode. We also made a handful of other design improvements to make Ox's UI clean, consistent, and more visually communicative.
- Bugfixes. There were a few assorted bugs throughout Ox. We've fixed all the ones we know about, including a notable addition that clarifies visibility for reports in which users do not have the necessary permissions to see all scorecards.

#### Details on score skipping:

We've aimed to make skipping simple, while still keeping the Ox score intuitive and valuable. Here's how it works.

When a scorecard contains a skipped score, you'll see its Ox score turn grey, and the score will be flagged with an asterisk. This also bubbles up to reports - if a particular criterion has been skipped in all scorecards, the entire report is flagged with a grey Ox score and an asterisk.

In cases where only some scorecards have skipped a score, the Ox score for a report is calculated using the average of all provided scores.

When calculating the Ox score, we treat any criteria that is unscored (all scorers skipped) as zero.

### Release 54: November 15, 2022

We've made a number of quality-of-life improvements throughout Ox.

- User avatars.  User avatars are unique, and all across Ox, including in Report, Stack, and Framework graphs.
- Notes tab.  All Frameworks, Reports, Stacks, and Sources now include a Notes tab, where you can leave notes and documentation for your work, including images and hyperlinks.
- Subtitles.  All objects now have a consistent title and subtitle, to help you easily identify and clarify their purpose. We've moved existing description content to the notes field.
- Permissions tab.  We moved permissions to its own tab to make it easier to see and edit all of an object's viewers, editors, and administrators. We've also added the object's owners to the bottom of each page, and linked those to permissions.
- Improved search.  Search is faster and more powerful, allowing you to use multiple terms, and search for items in stacks.
- Quick-linked Stacks.  Stack badges on reports help you quickly navigate back to their associated Stacks, or add a report to a stack.
- Even more quality-of-life improvements.  Adding frameworks or tags now shows your most recently used ones first. Owners and change dates are listed at the bottom of all object pages. Reports are now identified in scoring graphs in both Framework and Stacks.
- Bugfixes.  There were a few assorted bugs throughout Ox. We've found and fixed all the ones we know about.


### Release 53: November 1, 2022

Stacks are here! We've added a new core feature to Ox: Stacks.

- Stacks. You can now group a set of reports together, compare their Ox Scores, and dig into the scorecards, frameworks, and trends. Ideal for comparing between several assessments (hiring, vendors, software, or any zero-sum choice), stacks make it easy to understand a decision, stakeholder perspectives, and the points that need more consensus.
- Simplified Library. With the addition of Stacks, we've also simplified the library into two panes: one for your things and one for things you share with your teams, orgs, and other Ox users.
- New Dashboard. We've also reworked the dashboard entirely to surface your most recent Frameworks, Reports, and Stacks, and helping you easily get back to what you're actively working on, or start something new.
- New Graphs. We've added a new view to our scoring graph to allow you to visually see all scores stacked together. This makes it much simpler to understand trends and patterns of scoring. We've simplified the average display, giving you a single line at the average of all scores.
- Improved UI. Ox has been simplified, clarified, and improved throughout. From things like the overhauled framework explorer, to a new dark/light/auto mode toggle, to small spacing and alignment fixes throughout, we've streamlined Ox to make it a place you'll be even happier to spend time.
- Bugfixes. There were a few assorted bugs throughout Ox. We've found and fixed all the ones we know about.


### Release 52: October 1, 2022

- Score-only permissions for reports. You can now limit users to score-only permission for a report to facilitate independent, blind scoring for a given report.
- Ox suggestions across reports We now display Ox suggstions in the framework explorer across all reports, to help you understand how best to improve criteria, and your processes around scoring. 
- Simplified reports.  We've combined the analytic question and description fields, to make creating and sharing reports more intuitive.
- Track clone parents.  We're now tracking the parent of all cloned frameworks, to help surface relationships down the road.
- Bugfixes. We've found and fixed a small number of bugs within Ox.


### Release 51: September 1, 2022

This release focuses on making Ox faster, stronger, and more reliable.

- Speed. Significant improvements in page load speed and navigation.  You should now see see Ox in less than a second, and switching between pages should be instant.
- Defaults new criteria to 5.  We noticed that knowing what value to set for a criteria's importance was tripping up a numbers of users, so we now default new criteria to the same weight - 5/10.  You can still set the importance as you see fit.
- Bugfixes.  We added significant automated testing to Ox, and in the process found a fixed a number of small bugs thoughout the app.


### Release 50: July 31, 2022

**Welcome to the new Ox!**

We've built a new and improved UI that cleans up the entire interface and adds new visualizations, tabs, and features throughout. In particular, the new report and scorecards make it much easier for you to visualize, compare, and improve your judgments. There are also a host of brand new features, including:

- New Report Visualizations. Ox reports now include new tabs and visualizations that compare user scores and comments, identify low/medium/high levels of scoring noise (variance between user scores), and show weighted confidence for criteria.
- Ox Smart Suggestions. Under the Overview tab in reports, Ox flags criteria with low, medium, and high noise, and provides suggestions for how to reduce noise.
- New Scorecards.  All-new tools for creating and editing scorecards that lets you easily manage your scorecards, and compare scores and comments across users in a report.
- Explorer. On framework pages, you can now use the Explorer tab to compare how you and other users have scored individual criteria across different reports. You can also see Ox Smart Suggestions, criteria noise, and suggestions for how to reduce it.
- Team and Organization Management. You can now create and manage teams, approve administrators, and add new users to your Ox org from the Teams page.
- Permissions.  Permissions have been overhauled to make sharing easier and more granular. You can now customize permissions for each framework, source, and report, granting specific users and teams read, write, and administrative access.
- Global Search. Ox now has global search in the top bar, where you can search for Ox content by name or tag, and navigate to results from a dropdown list.  Keyboard shortcuts are included, so you can switch between pages without ever reaching for the mouse.
- Dark Mode. You can now choose between a light mode and a dark mode for Ox's interface.
- Discussion Participants. Under the Discussion tab of sources, reports, and frameworks, you can now see who is in the conversation, with a list of all user who have commented or are following the discussion.
- Source Keyword Search. When adding sources to a report, you can now more easily find the sources you‘re looking for with a keyword search bar.

### Release 49: June 16, 2022

#### New Features:

- Discussion: A new discussion section has been added to frameworks, reports, and sources.
- Follow: Users can follow (subscribe) to discussions in frameworks, reports, and sources in order to receive
  notifications for new comments.
- Inbox: Ox now has a built-in inbox, where users are notified of any new comments in followed discussions. Users can
  mark things as Read/Unread or as Done to archive them in a separate folder.
- Tags: Users can now tag any framework, source, or report with one or more tags, and click to find everything that
  shares a specific tag. Tags are also searchable in the Activity section of the Dashboard.
- Customizable PDF Exports: For report PDF exports, users can now change the organization name, logo, color theme, and
  add distribution guidance or classification level.
- Bugfixes: Speed and reliability have been improved throughout Ox, in addition to fixes for a few rare bugs.

### Release 48: May 1, 2022

#### New Features:

- Next-generation application backend, to enable rapid buildout of new features, more robust permissioning, and ML and
  AI support.
- Much faster application load times.
- Allows multiple scorecards to be added to and removed from a report.
- Allows multiple sources to be added to and removed from a report.
- Allows unlimited text into any field. (No more 255 character limit.)
- Streamlined framework add and removes from a report.
- Moves organization, team and user management features to a dedicated administration console.

#### Bugfixes:

- Ensures consistent display and scaling of criteria importance (formerly "weight").

### Release 47: April 7, 2022

#### New Features:

- Reworked Framework view and edit page to make framework creation and modification much easier, more visual and more
  intuitive.
- Clone Framework feature, to allow users to easily clone existing frameworks.
- Adds CSV export for framework. The current implementation is keyed around having each row be self-contained for ease
  of machine import. Please provide feedback on format changes that would ease data interchange!
- Changes criteria importance to a 1-10 scale, normalizes previous criteria by dividing by 10.
- Adds the ability to remove a framework from a report.
- Adds confirmation dialogs for destructive actions (delete, destructive edits.)
- Reduces the UI functionality for superusers to only team and user management.

#### Bugfixes:

- Fixes an incorrect average for a user's criteria score on the dashboard.
- Fixes the password complexity check to allow much more complex passwords with more special characters.
- Fixes PDF generation for very large PDFs.
- Fixes a bug where login expiration gave a blank screen instead of returning the user to the login page.
- Fixes a bug where team data was not saved if a team lead was missing.
- Fixes related bugs with missing teams in source and framework.
- Fixes a save bug for new sources in brand-new organizations.
- Ensures that scorecard comment field auto-expands to fit the user's text.


### Ox Intel Application Upgrade Instructions

These instructions provide the set of commands needed to upgrade to v1.50 of the Ox Intel application.

The update process is performed by running an automated script that performs the necessary tasks. The script will
perform the following tasks:

* Export and backup the existing application database
* Migrate the existing application data to the updated structure
* Load new docker images with the updated software version
* Launch and load the new docker images and perform system configuration

To perform the upgrade, you will need to copy the update files to the server (AWS instance) where the Ox Intel
application is running. To do this point a browser at the url and confirm the login page loads.

Next, you will need to expand the archive by running the following command:

```commandline
tar -xvf <NAME OF UPDATE>
```

When this process is complete, a directory will be created with the same name as the update file. To see this run the
following command:

```commandline
ls
```

Now change directories into that directory:

```commandline
cd <NAME OF DIRECTORY>
```

Next, we will run the upgrade script. To do this run the following command:

```commandline
 sudo ./upgrade-to-aurochs.sh
```

To verify the update navigate to the application url and login.

