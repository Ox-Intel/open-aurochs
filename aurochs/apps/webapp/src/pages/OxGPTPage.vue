<template>
  <DefaultLayout>
    <main class="" data-cy="oxgpt">
      <div class="prose m-auto w-full">
        <!-- <img class="w-48 mx-auto mb-0" :src="image_url('common/img/oxgpt_white.png')" /> -->
        <!-- <img class="w-48 mx-auto mb-0" :src="image_url('common/img/oxgpt_vertical_purple.png')" /> -->
        <!-- <img class="w-72 mx-auto mb-0" :src="image_url('common/img/oxgpt_horizontal_white.png')" /> -->
        <img
          v-if="!darkMode()"
          class="w-40 mx-auto mb-0"
          :src="image_url('common/img/oxgpt_vertical_black_beta.png')"
        />
        <img v-if="darkMode()" class="w-40 mx-auto mb-0" :src="image_url('common/img/oxgpt_vertical_white_beta.png')" />
        <!-- <img class="w-72 mx-auto mb-0" v-if="!darkMode()" :src="image_url('common/img/oxgpt_horizontal_large_black.png')" /> -->
        <!-- <img class="w-72 mx-auto mb-0" v-if="darkMode()" :src="image_url('common/img/oxgpt_horizontal_large_white.png')" /> -->
        <div data-cy="generate-criteria">
          <div class="text-center">
            <div class="mb-2 mt-8 font-bold">Ox, build a framework to help me:</div>
            <OxTextarea
              v-model="topic"
              autofocus="true"
              class="max-w-screen-md mx-auto"
              placeholder="Anything you can think of – hire a new product manager, assess vulnerability risks, evaluate investment opportunities, conduct performance evaluations, do due diligence on potential acquisitions, choose where to stay on vacation, select a new security provider..."
              input-type="textarea"
            />
            <!-- label="Framework topic or question" -->
            <div class="mb-2 mt-12 font-bold">
              Share any context or guidance you'd like Ox to consider (recommended):
            </div>
            <OxTextarea
              v-model="topic_context"
              class="max-w-screen-md mx-auto"
              placeholder="Add any additional context that you feel is very important, explaining it as you would to an expert in the topic.

Context could include things like your job or sector, criteria that you care more about, your risk tolerance, your long-term outlook, how thorough the due dlligence process needs to be, etc."
              input-type="textarea"
            />

            <div v-if="!generatingFramework" class="btn btn-primary" @click="generateFramework">
              <div v-if="generatedFramework.criteria && generatedFramework.criteria?.length > 0">
                <FontAwesomeIcon :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 align-middle" />
              </div>
              {{
                generatedFramework.criteria && generatedFramework.criteria?.length > 0
                  ? "Regenerate Framework"
                  : "Generate Framework"
              }}
              <div
                v-if="!generatedFramework || !generatedFramework.criteria || generatedFramework.criteria?.length == 0"
              >
                <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
              </div>
            </div>
            <div v-if="generatingFramework">
              <div v-if="generatingFramework" class="btn btn-ghost" disabled>Generating Framework...</div>
              <div class="dot-container mb-8">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
              </div>
            </div>
            <div v-if="generatingFrameworkError" class="mt-4">
              {{ generatingFrameworkError }}
            </div>
          </div>
          <div v-if="generatedFramework && generatedFramework.name" ref="seeGeneratedCriteria" class="framework pt-16">
            <!-- <h1 class=""> -->
            <!-- {{ generatedFramework.name }} -->
            <div class="flex">
              <div class="max-w-screen-md w-16 h-16 mr-4">
                <OxChartIcon
                  :criteria="generatedFramework.criteria"
                  :chart_id="`generated_framework`"
                  :small="true"
                  class="w-16 h-16"
                />
              </div>
              <div>
                <input
                  v-model="generatedFramework.name"
                  data-cy="input-framework-name"
                  placeholder="Framework Title"
                  autofocus
                  type="text"
                  class="w-auto max-w-100 p-0 text-3xl text-neutral font-bold font-extra-bold border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-base-200 focus:base-200 text-neutral mt-0.5"
                  :style="`width: ${
                    3 + (generatedFramework?.name?.length || 0) * 0.8
                  }ch; max-width: 100%; min-width: 250px;`"
                />
                <!-- </h1> -->
                <p class="pr-32 mt-0">
                  <input
                    v-model="generatedFramework.description"
                    data-cy="input-framework-name"
                    placeholder="Framework Title"
                    autofocus
                    type="text"
                    class="w-auto max-w-100 p-0 border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-base-200 focus:base-200 text-neutral mt-0.5"
                    :style="`width: ${
                      3 + (generatedFramework?.description?.length || 0) * 0.8
                    }ch; max-width: 100%; min-width: 250px;`"
                  />
                </p>
              </div>
            </div>
            <div v-for="(c, idx) in generatedFramework.criteria" :key="idx" class="flex -mr-32">
              <div
                :class="
                  'unscored-criteria border-2 rounded-lg block relative mb-6 w-10/12 py-4 bg-base-200 ' +
                  (isHighlightedForRemoval(idx) ? ' opacity-25' : '')
                "
                :style="`border-color: var(--criteria-color-${idx + 1});`"
              >
                <div
                  :style="`background-color: var(--criteria-color-${idx + 1});`"
                  class="w-6 h-full absolute left-0 top-0"
                ></div>
                <div class="ml-10 block">
                  <div class="flex w-full">
                    <div :class="finishedCriteriaSelection ? 'w-6/12' : ''">
                      <div>
                        <input
                          v-model="c.name"
                          data-cy="input-criteria-name"
                          placeholder="Criteria Title"
                          autofocus
                          type="text"
                          class="w-auto max-w-100 font-bold text-lg p-0 font-extra-bold border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-200 base-400 focus:base-400 text-neutral mt-0.5"
                          :style="`width: ${3 + (c?.name?.length || 0) * 0.8}ch; max-width: 100%; min-width: 250px;`"
                        />
                      </div>
                      <input
                        v-model="c.description"
                        data-cy="input-criteria-subtitle"
                        type="text"
                        placeholder="Criteria description..."
                        class="w-auto max-w-100 font-light p-0 border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-200 base-400 focus:base-400 text-neutral"
                        :style="`width: ${
                          3 + (c?.description?.length || 0) * 0.7
                        }ch; max-width: 100%; min-width: 250px;`"
                      />
                    </div>
                    <div v-if="finishedCriteriaSelection" class="w-6/12">
                      <div class="flex w-full pr-8 ml-2 gap-4">
                        <div class="grow pt-4">
                          <OxSlider v-model:score="c.weight" :min="0" :max="10" />
                        </div>
                        <div
                          class="w-auto font-bold leading-none rounded-full text-center text-white"
                          :style="`${getCriteriaColor(idx)} padding: ${6 + 2 * Math.round(c.weight)}px; margin: ${
                            20 - 2 * Math.round(c.weight)
                          }px; line-height: 0.5em; ${
                            c.weight >= 10 ? 'padding-right: 20px;padding-left: 20px; margin-right:2px;' : ''
                          }`"
                        >
                          {{ Math.round(Number(c.weight)) }}
                        </div>
                      </div>
                    </div>
                  </div>
                  <!-- <p>{{c.weight}}</p> -->
                </div>
              </div>
              <div class="w-1/12 text-center middle pl-4 pt-6">
                <div
                  class="btn btn-outline btn-error w-10 h-8 pt-0 text-lg"
                  @click="removeCriteria(idx)"
                  @mouseover="potentialRemoveCriteria(idx)"
                  @mouseout="clearPotentialRemoveCriteria(idx)"
                >
                  <FontAwesomeIcon :icon="['fad', 'minus']" class="h-5 w-5 align-middle" />
                </div>
              </div>
            </div>
            <div class="flex flex-row w-full justify-between w-11/12">
              <div class="flex">
                <div class="btn btn-primary btn-outline mr-4" @click="addBlankCriteria()">
                  <FontAwesomeIcon :icon="['fad', 'plus']" class="h-4 w-4 mr-2 align-middle" />
                  Add New Criteria
                </div>
                <div v-if="!generatingMoreCriteria" class="btn btn-primary btn-outline" @click="generateMoreCriteria">
                  <FontAwesomeIcon :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 align-middle" />
                  Generate More Criteria
                </div>
                <div v-if="generatingMoreCriteria" class="btn btn-outline btn-disabled" @click="generateMoreCriteria">
                  <FontAwesomeIcon :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 fa-spin align-middle" />
                  Generating More Criteria...
                </div>
              </div>
              <div v-if="generatingMoreCriteria">
                <div class="dot-container">
                  <div class="dot"></div>
                  <div class="dot"></div>
                  <div class="dot"></div>
                </div>
              </div>
              <div v-if="!finishedCriteriaSelection" class="btn btn-primary" @click="finishCriteriaSelection">
                Continue to weights
                <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
              </div>
              <div v-if="finishedCriteriaSelection" class="btn btn-primary" @click="finishCriteriaWeight">
                Start using my framework
                <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
              </div>
            </div>
          </div>
        </div>

        <div
          v-if="finishedCriteriaSelection && finishedCriteriaWeight"
          ref="nameSubjects"
          class="center w-full"
          data-cy="weight-criteria"
        >
          <div class="text-center max-w-screen-lg mx-auto">
            <div class="text-2xl mt-20 mb-0">
              Name the subjects of your analysis. <span v-if="subjectsErrorShowing" class="text-error">*</span>
            </div>
            <div class="relative w-full text-center max-w-screen-md mx-auto">
              <div class="mb-2 mt-8 font-bold">
                <!-- Name the subject(s) of your analysis.<br /> -->
                Separate each subject with new line.
                <!-- Both URLs and text descriptions are allowed. -->
              </div>
              <div
                :class="`btn btn-primary btn-sm absolute right-0 top-0 ${
                  generatingSubjects ? ' disabled btn-disabled' : ''
                }`"
                @click="generateSubjects"
              >
                <span v-if="!generatingSubjects">Suggest Subjects</span>
                <span v-if="generatingSubjects">
                  <FontAwesomeIcon :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 fa-spin align-middle" />
                  Generating...</span
                >
              </div>
            </div>
            <div v-if="subjectsErrorShowing" ref="subjectsErrorShowing" class="text-error my-4 text-center">
              Please enter one or more subjects to analyze.
            </div>
            <OxTextarea
              v-model="subjects"
              placeholder="John Y. Smith
CVE-2020-3433
Stealth Startup, Inc.
Vienna
Sony A7SIII
Apple"
              input-type="textarea"
              :classes="'max-w-screen-md'"
            />

            <!--             <div class="mb-2 mt-8 font-bold">
              Share any context or guidance you'd like Ox to consider when conducting the analysis:
            </div>

            <OxTextarea
              v-model="scoring_context"
              placeholder="Share any context around the assessment or details on what you want Ox to look for, in plain English. "
              input-type="textarea"
            />
 -->
            <div class="mb-2 mt-12 font-bold">Select the sources of information you'd like Ox to review:</div>
            <div class="mb-16 mt-4">
              <div class="btn-group">
                <button
                  :class="
                    'btn ' +
                    (sourceGeneralKnowledge
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceGeneralKnowledge = !sourceGeneralKnowledge"
                >
                  <FontAwesomeIcon
                    v-if="sourceGeneralKnowledge"
                    :icon="['fad', 'check']"
                    class="h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  <FontAwesomeIcon
                    v-if="!sourceGeneralKnowledge"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  General Knowledge
                </button>
                <button
                  :class="
                    'btn ' +
                    (sourceSearch
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceSearch = !sourceSearch"
                >
                  <FontAwesomeIcon
                    v-if="sourceSearch"
                    :icon="['fad', 'check']"
                    class="h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  <FontAwesomeIcon
                    v-if="!sourceSearch"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  Internet Search
                </button>
                <button
                  :class="
                    'btn ' +
                    (sourceNews
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceNews = !sourceNews"
                >
                  <FontAwesomeIcon v-if="sourceNews" :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
                  <FontAwesomeIcon
                    v-if="!sourceNews"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  Recent News
                </button>
                <button
                  :class="
                    'btn ' +
                    (sourceCustom
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceCustom = !sourceCustom"
                >
                  <FontAwesomeIcon
                    v-if="sourceCustom"
                    :icon="['fad', 'check']"
                    class="h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  <FontAwesomeIcon
                    v-if="!sourceCustom"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  Custom URLs
                </button>
                <button
                  :class="
                    'btn ' +
                    (sourceCustomText
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceCustomText = !sourceCustomText"
                >
                  <FontAwesomeIcon
                    v-if="sourceCustomText"
                    :icon="['fad', 'check']"
                    class="h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  <FontAwesomeIcon
                    v-if="!sourceCustomText"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  Custom Text
                </button>
                <button
                  :class="
                    'btn ' +
                    (sourceCustomDocs
                      ? 'bg-ox-score border-ox-score text-ox-score-content  hover:brightness-90 hover:border-ox-score'
                      : 'btn-outline hover:bg-ox-score btn-medium-grey border-medium-grey')
                  "
                  @click="sourceCustomDocs = !sourceCustomDocs"
                >
                  <FontAwesomeIcon
                    v-if="sourceCustomDocs"
                    :icon="['fad', 'check']"
                    class="h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  <FontAwesomeIcon
                    v-if="!sourceCustomDocs"
                    :icon="['fad', 'check']"
                    class="text-medium-grey h-4 w-4 mr-2"
                    aria-hidden="true"
                  />
                  PDFs or Word Docs
                </button>
              </div>
              <OxTextarea
                v-if="sourceCustom"
                v-model="sourceUrls"
                class="max-w-screen-md w-8/12 mt-4 mx-auto"
                :max-height="120"
                placeholder="Add any URLs that you'd like Ox to use, separated by line breaks.

Ox will research using these URLs as well as similar sources it finds online."
                input-type="textarea"
              />
              <OxTextarea
                v-if="sourceCustomText"
                v-model="sourceText"
                class="max-w-screen-md w-8/12 mt-4 mx-auto"
                :max-height="120"
                placeholder="Type or paste any text you'd like Ox to use in conducting the analysis.

This can be large reports, narrative descriptions, or lists of ideas."
                input-type="textarea"
              />
              <div
                v-if="sourceCustomDocs"
                :class="
                  'max-w-screen-md w-8/12 mt-8 mx-auto rounded-md shadow-inner p-8 text-neutral ' +
                  (draggingOver ? 'bg-base-300 border-base-200 dragging' : 'bg-base-200')
                "
              >
                <FileUpload
                  name="demo[]"
                  :custom-upload="true"
                  :multiple="true"
                  :unstyled="true"
                  :show-upload-button="true"
                  :show-cancel-button="false"
                  :auto="true"
                  :mode="'advanced'"
                  :class="''"
                  :style="''"
                  @uploader="handleFileUpload($event)"
                  @select="onSelectedFiles"
                >
                  <template #buttonbar="{}"></template>
                  <template #content="{}">
                    <div class="text-neutral" @dragover="handleDragOver" @dragleave="handleDragLeave">
                      <div>
                        <div class="flex text-center text-2xl gap-8 w-full mb-8 justify-center">
                          <FontAwesomeIcon :icon="['fad', 'file-pdf']" class="h-12 w-12" />
                          <FontAwesomeIcon :icon="['fad', 'file-doc']" class="h-12 w-12" />
                        </div>

                        Drag and drop any PDF, Word, or text documents you want to use.
                        <br />
                        <br />
                        Ox will only use the files within this analysis, and will not retain them after this page is
                        refreshed.
                        <div class="w-full text-center justify-center mt-4">
                          <div class="btn btn-outline" @click="openFileChooser">
                            Choose <template v-if="files && Object.keys(files).length > 0"> More </template> Files
                          </div>
                        </div>
                      </div>
                      <div v-if="Object.keys(files).length > 0">
                        <div class="flex flex-wrap p-0 sm:p-5 mt-8 gap-4">
                          <div
                            v-for="file of files"
                            :key="file.name + file.type + file.size"
                            class="flex justify-between w-full"
                          >
                            <div class="flex gap-6">
                              <div v-if="file.complete" class="mx-auto badge badge-success mt-3 w-20">Analyzed</div>
                              <div v-if="!file.complete" class="mx-auto badge badge-warning mt-3 w-20">Analyzing..</div>
                              <div class="text-left w-6">
                                <FontAwesomeIcon
                                  v-if="file.type == 'pdf'"
                                  :icon="['fad', 'file-pdf']"
                                  class="mt-2 h-8 w-8"
                                />
                                <FontAwesomeIcon
                                  v-if="file.type == 'doc'"
                                  :icon="['fad', 'file-doc']"
                                  class="mt-2 h-8 w-8"
                                />
                                <FontAwesomeIcon
                                  v-if="file.type == 'other'"
                                  :icon="['fad', 'file-lines']"
                                  class="mt-2 h-8 w-8 -ml-1"
                                />
                                <FontAwesomeIcon v-if="!file.type" :icon="['fad', 'file']" class="mt-2 h-8 w-8 -ml-1" />
                              </div>
                              <div class="text-left">
                                <span class="font-semibold mb-0 leading-5">{{ file.name }}</span>
                                <div class="-mt-1">
                                  {{ formatSize(file.size)
                                  }}<span v-if="file.complete"> | {{ formatNumber(file.num_words) }} words</span>
                                </div>
                              </div>
                            </div>
                            <div class="text-right">
                              <div class="cursor-pointer opacity-75" @click="removeFile(file.name + file.size)">
                                <FontAwesomeIcon :icon="['fad', 'x']" class="mt-2 h-4 w-4" />
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                </FileUpload>
              </div>
            </div>

            <div v-if="!scoringSubjects && !handAnalyzeSet" class="btn btn-primary" @click="scoreSubjects">
              Analyze using Ox AI
              <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
            </div>
            <div v-if="!scoringSubjects && handAnalyzeSet" class="btn btn-primary" @click="scoreSubjects">
              Analyze Manually
              <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
            </div>
            <div v-if="scoringSubjects" class="btn btn-disabled" @click="scoreSubjects">Analyzing using Ox AI...</div>
            <div v-if="scoringSubjects">
              <div class="dot-container mb-8">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
              </div>
            </div>
            <div v-if="scoringSubjectsError" class="mt-4">
              {{ scoringSubjectsError }}
            </div>
            <div v-if="statusUpdatesSorted" class="mt-2 mb-20 text-left max-w-screen-md mx-auto">
              <div v-for="(message, idx) in statusUpdatesSorted" :key="idx">
                <div :class="'flex ' + (message.inset ? 'pl-6' : '')">
                  <FontAwesomeIcon v-if="message.complete" :icon="['fad', 'check']" class="h-4 w-4 mr-2 mt-1 pt-0.5" />
                  <FontAwesomeIcon
                    v-if="!message.complete"
                    :icon="['fas', 'spinner-third']"
                    class="h-4 w-4 mr-2 mt-1 pt-0.5 fa-spin opacity-50"
                  />
                  <div v-html="message.message"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div ref="bottom" class="w-full">
        <div
          v-if="
            generatedFramework &&
            finishedCriteriaSelection &&
            finishedCriteriaWeight &&
            !scoringSubjects &&
            errorScoringSubjects
          "
          ref="errorScoringSubjects"
          class="mt-4"
        >
          <div class="alert alert-warning alert-outline my-4 mx-auto max-w-screen-md p-6">
            <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="h-10 w-10 mr-2" />
            <div class="flex-wrap">
              <p>
                Hm. We seem to have hit an error scoring. As OxGPT is still in beta, sometimes this happens due to
                system fluctuations.
              </p>
              <p>Please try again and let us know if you see a consistent issue!</p>
            </div>
            <a href="mailto:support@oxintel.ai" class="btn mr-4">Contact Ox</a>
          </div>
        </div>
        <div
          v-if="
            generatedFramework &&
            finishedCriteriaSelection &&
            finishedCriteriaWeight &&
            subjectsScoredByOx &&
            !scoringSubjects &&
            !errorScoringSubjects
          "
          ref="scorecardScoringEle"
        >
          <div class="text-center">
            <h1 class="text-2xl mt-20 mb-0">Review Scorecards</h1>
            <div class="mb-2 mt-8 font-bold">
              OxGPT has taken a first pass at scoring each of your subjects. Review and adjust the scores as you see
              fit.
            </div>
          </div>
          <!-- :selected-index="Number(selectedTab)" @change="changeTab" -->
          <TabGroup>
            <TabList class="tabs w-full mt-20">
              <Tab v-for="sc in scorecards" v-slot="{ selected }" :key="sc.name" as="template">
                <div
                  :data-cy="`tab-${sc.index}`"
                  class="tab tab-bordered tab-lg focus:outline-none"
                  :class="selected ? 'tab-active' : ''"
                >
                  <!-- <FontAwesomeIcon :icon="sc.icon" :class="sc.class" class="mr-2 align-middle" /> -->
                  <span>{{ sc.name }}</span>
                </div>
              </Tab>
            </TabList>
            <TabPanels class="mt-8 justify-center">
              <TabPanel v-for="sc in scorecards" :key="sc.index" as="template">
                <div class="card w-full bg-base-200 card-bordered mt-4 mx-auto max-w-screen-xl">
                  <div class="card-body w-full">
                    <div class="text-2xl font-extra-bold text-center">{{ sc.name }}</div>

                    <div class="flex">
                      <div class="h-8 w-8 mr-4">
                        <OxChartIcon
                          :criteria="generatedFramework.criteria"
                          :chart_id="`generated_framework`"
                          :small="true"
                        />
                      </div>
                      <div class="font-bold font-2xl">
                        {{ generatedFramework.name }}
                      </div>
                    </div>
                    <div class="w-full">
                      <div v-for="(score, score_idx) in sc.scores" :key="score_idx">
                        <div class="font-bold">{{ score.criteria.name }}</div>
                        <div
                          class="relative cursor-pointer"
                          @click="
                            if (score.skipped) {
                              score.skipped = false;
                            }
                          "
                        >
                          <div
                            v-if="score.skipped"
                            class="absolute inset-x-1/2 w-32 px-4 py-2 pt-1 bg-base-200 border-neutral text-center font-bold opacity-75 text-neutral text-sm cursor-pointer"
                          >
                            Skipped
                          </div>
                          <OxSlider
                            v-model:score="score.score"
                            v-model:oxgptScoredLast="score.gpt_scored_last"
                            :min="0"
                            :max="10"
                            :enable-ox-scoring="true"
                            :disabled="score.skipped === true"
                          />
                        </div>
                        <div class="flex w-full justify-between">
                          <div class="grow">
                            <OxTextarea
                              v-model="score.comment"
                              placeholder="Score explanation and comments."
                              input-type="textarea"
                              :classes="`w-full bg-base-200 text-sm mt-2 border-0`"
                            />
                          </div>

                          <div class="flex gap-4">
                            <div
                              class="btn btn-sm bd-base-500 text-base-500 mt-2 w-16 text-center btn-base-300 btn-outline"
                              @click="score.skipped = !score.skipped"
                            >
                              {{ score.skipped ? "Unskip" : "Skip" }}
                            </div>
                            <div
                              class="btn btn-sm bd-base-500 text-base-500 mt-2 btn-base-300 btn-outline"
                              @click="
                                score.score = 0;
                                score.comment = '';
                                score.skipped = false;
                              "
                            >
                              Clear
                            </div>
                            <div
                              :class="
                                'w-10 h-10 rounded block pt-1 mt-1 font-bold text-2xl text-center text-success-content ' +
                                (score.skipped ? 'bg-base-500 text-medium-grey' : '')
                              "
                              :style="score.skipped ? '' : `background-color: var(--criteria-color-${score_idx + 1});`"
                            >
                              {{ score.skipped ? "–" : score.score }}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </TabPanel>
            </TabPanels>
          </TabGroup>
          <div v-if="urlsUsed && urlsUsed.length > 0" class="max-w-screen-md mx-auto mt-12">
            <div class="text-lg font-bold">Source URLs referenced:</div>
            <ul>
              <li v-for="url in urlsUsed" :key="url">
                <a :href="url" target="_blank" class="underline text-primary text-sm">{{ strippedUrl(url) }}</a>
              </li>
            </ul>
          </div>
          <div class="text-center w-full mt-12 mb-12">
            <div v-if="!scoringSubjects" class="btn btn-primary" @click="finalizeAnalysis">
              Finish Scoring and View Results
              <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
            </div>
          </div>
        </div>

        <div v-if="finishedCriteriaSelection && subjectsScoredByUser" ref="finalizedScoresRef">
          <div v-if="scorecards.length == 1">
            <!-- Single scorecard. -->
            <div v-for="(sc, sc_idx) in scorecards" :key="sc_idx">
              <div class="card w-full bg-base-200 card-bordered mt-4 mx-auto max-w-screen-xl">
                <div class="card-body w-full relative">
                  <div class="absolute right-0 mr-8">
                    <OxScoreBox :ox-score="oxScore(sc)" :has-skipped="hasSkipped(sc)" />
                  </div>
                  <div class="text-2xl font-extra-bold text-center">{{ sc.name }}</div>
                  <div class="flex">
                    <div class="h-8 w-8 mr-4">
                      <OxChartIcon
                        :criteria="generatedFramework.criteria"
                        :chart_id="`generated_framework`"
                        :small="true"
                      />
                    </div>
                    <div class="font-bold font-2xl">
                      {{ generatedFramework.name }}
                    </div>
                  </div>
                  <div class="w-full">
                    <div v-for="(score, score_idx) in sc.scores" :key="score_idx" class="h-12">
                      <div class="font-bold text-sm">{{ score.criteria.name }}</div>
                      <div class="full_bar relative">
                        <div
                          v-if="score.skipped"
                          class="absolute z-20 w-full px-4 py-2 pt-0 bg-base-200 text-neutral opacity-75 text-sm"
                        >
                          Skipped
                        </div>
                        <div
                          class="absolute left-0 h-4 bg-bar opacity-25"
                          :style="`width: ${score.criteria.weight * 10}%; background-color: var(--criteria-color-${
                            score_idx + 1
                          });`"
                        ></div>
                        <div
                          class="absolute left-0 bar h-4 z-10"
                          :style="`width: ${
                            score.score * score.criteria.weight
                          }%; background-color: var(--criteria-color-${score_idx + 1});`"
                        >
                          <div
                            v-if="score.gpt_scored_last"
                            class="absolute bottom-0 right-0 w-4 h-4 text-center bg-ox-score text-ox-score-content text-xs"
                            style="font-size: 0.6rem"
                          >
                            AI
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div v-if="scorecards.length > 1">
            <!-- Stack -->
            <div class="card w-full bg-base-200 card-bordered mt-4 mx-auto max-w-screen-xl">
              <div class="card-body w-full relative">
                <div class="flex text-center mb-8">
                  <div class="h-8 w-8 mr-4">
                    <OxChartIcon
                      :criteria="generatedFramework.criteria"
                      :chart_id="`generated_framework`"
                      :small="true"
                    />
                  </div>
                  <div class="font-bold text-2xl">
                    {{ generatedFramework.name }}
                  </div>
                </div>
                <div v-for="(sc, sc_idx) in sortedScorecards" :key="sc_idx">
                  <p>
                    <b>{{ sc.name }}</b>
                  </p>
                  <div
                    :style="`width: ${oxScore(sc)}%;`"
                    class="rounded-sm text-ox-score-content p-3 py-1 mt-1 mb-2 text-md font-bold inline-block"
                    :class="hasSkipped(sc) ? 'bg-medium-grey' : 'bg-ox-score'"
                    data-cy="ox-bar"
                  >
                    <span v-if="oxScore(sc) > 6"
                      >{{ oxScore(sc) }}<span class="text-sm">%</span>
                      <div
                        v-if="hasSkipped(sc)"
                        class="star inline-block tooltip tooltip-right cursor-pointer"
                        data-tip="At least one criteria was skipped by all scorers."
                      >
                        <div class="text-md">*</div>
                      </div></span
                    >
                    <span v-if="oxScore(sc) <= 6">&nbsp;</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div
            v-if="finishedCriteriaSelection && subjectsScoredByUser && !creatingUser"
            class="text-center w-full mt-12 mb-40"
          >
            <div
              :class="'btn  ' + (saving ? 'disabled btn-disabled' : 'btn-primary')"
              @click="
                saving = true;
                saveFrameworkAndScores();
              "
            >
              {{ saving ? "Saving..." : "Save Framework and Scores" }}
              <FontAwesomeIcon v-if="!saving" :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
            </div>
          </div>
          <div v-if="creatingUser && !showLogIn" class="mx-auto max-w-screen-sm mt-8 text-center p-8 bg-base-150">
            <div class="text-2xl font-bold mb-2">Create Account</div>
            <div class="text-md">Looks like you don't have an Ox account yet!</div>
            <div class="text-md mb-2">Let's make one so you can save your results - it's free.</div>
            <div v-if="creationErrorMessage" class="text-error">{{ creationErrorMessage }}</div>

            <div class="max-w-sm mx-auto">
              <div class="w-full relative mb-2">
                <div v-if="validNewUserFirstName" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserFirstName"
                  type="text"
                  placeholder="First Name"
                  class="input input-bordered w-full px-4"
                />
              </div>
              <div class="w-full relative mb-2">
                <div v-if="validNewUserLastName" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserLastName"
                  type="text"
                  placeholder="Last Name"
                  class="input input-bordered w-full px-4"
                />
              </div>
              <div class="w-full relative mb-2">
                <div v-if="validNewUserEmail" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserEmail"
                  type="text"
                  placeholder="Email"
                  class="input input-bordered w-full px-4"
                />
              </div>
              <div class="w-full relative mb-4">
                <div v-if="validNewUserPassword" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserPassword"
                  type="password"
                  placeholder="Password"
                  class="input input-bordered w-full px-4"
                />
              </div>
              <div
                :class="'btn  ' + (!newUserFormIsValid || saving ? 'disabled btn-disabled' : 'btn-primary')"
                @click="
                  saving = true;
                  createAccountAndSave();
                "
              >
                <FontAwesomeIcon v-if="saving" :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 fa-spin align-middle" />
                {{ saving ? "Creating Account and Saving..." : "Create Account and Save Results" }}
                <FontAwesomeIcon v-if="!saving" :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
              </div>
            </div>
            <div class="mx-auto mt-4 mb-2 text-primary cursor-pointer" @click="showLogIn = true">
              Have an account? <span class="underline">Log in instead.</span>
            </div>
          </div>
          <div v-if="creatingUser && showLogIn" class="mx-auto max-w-screen-sm mt-8 text-center p-8 bg-base-150">
            <div class="text-2xl font-bold mb-2">Log in</div>
            <div class="text-md">Have an Ox account? Log in to save your results.</div>
            <div v-if="creationErrorMessage" class="text-error">{{ creationErrorMessage }}</div>

            <div class="max-w-sm mx-auto">
              <div class="w-full relative mb-2">
                <div v-if="validNewUserEmail" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserEmail"
                  type="text"
                  placeholder="Email"
                  class="input input-bordered w-full px-4"
                />
              </div>
              <div class="w-full relative mb-4">
                <div v-if="validNewUserPassword" class="-left-8 mt-1 top-2 text-success absolute z-20">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="align-middle h-6 w-6" />
                </div>
                <input
                  v-model="newUserPassword"
                  type="password"
                  placeholder="Password"
                  class="input input-bordered w-full px-4"
                />
              </div>
            </div>
            <div
              :class="'btn  ' + (!loginFormIsValid || saving ? 'disabled btn-disabled' : 'btn-primary')"
              @click="
                saving = true;
                logInAndSave();
              "
            >
              <FontAwesomeIcon v-if="saving" :icon="['fad', 'repeat']" class="h-4 w-4 mr-2 fa-spin align-middle" />
              {{ saving ? "Logging in and Saving..." : "Log In and Save Results" }}
              <FontAwesomeIcon v-if="!saving" :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
            </div>
            <div class="underline mx-auto mt-4 text-primary cursor-pointer" @click="showLogIn = false">
              Sign up instead.
            </div>
          </div>
          <div
            v-if="
              generatedFramework &&
              finishedCriteriaSelection &&
              finishedCriteriaWeight &&
              subjectsScoredByOx &&
              (newUserFormIsValid || loginFormIsValid) &&
              !scoringSubjects &&
              !saving &&
              errorSaving
            "
            ref="errorSaving"
            class="mt-4"
          >
            <div class="alert alert-warning alert-outline my-4 mx-auto max-w-screen-md">
              <p>
                <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="h-10 w-10 mr-2" />
                Hm. We seem to have hit an saving this framework. Apologies! As OxGPT is still in beta, sometimes this
                happens due to system fluctuations. <br />Please try again and let us know if you see a consistent
                issue!
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </DefaultLayout>
</template>

<script>
import "regenerator-runtime/runtime";
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { ref } from "vue";
import FileUpload from "primevue/fileupload";
import { useAurochsData } from "../stores/aurochs";
import OxTextarea from "../components/common/forms/OxTextarea.vue";
import OxChartIcon from "../components/common/icons/OxChartIcon.vue";
import OxScoreBox from "../components/common/OxScoreBox.vue";
import OxSlider from "../components/common/forms/OxSlider.vue";
import chart_colors from "../mixins/chart_color";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faMinus } from "@fortawesome/pro-duotone-svg-icons/faMinus";
import { faLayerPlus } from "@fortawesome/pro-duotone-svg-icons/faLayerPlus";
import { faRepeat } from "@fortawesome/pro-duotone-svg-icons/faRepeat";
import { faAngleRight } from "@fortawesome/pro-duotone-svg-icons/faAngleRight";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";
import { faSpinnerThird } from "@fortawesome/pro-solid-svg-icons/faSpinnerThird";
import { faFileDoc } from "@fortawesome/pro-duotone-svg-icons/faFileDoc";
import { faFilePdf } from "@fortawesome/pro-duotone-svg-icons/faFilePdf";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faFile } from "@fortawesome/pro-duotone-svg-icons/faFile";
import { faX } from "@fortawesome/pro-duotone-svg-icons/faX";
// import { faFileWord } from "@fortawesome/pro-duotone-svg-icons/faFileWord";
// import { faFileExcel } from "@fortawesome/pro-duotone-svg-icons/faFileExcel";

library.add(
  faMinus,
  faLayerPlus,
  faCheck,
  faRepeat,
  faAngleRight,
  faTriangleExclamation,
  faSpinnerThird,
  faFileDoc,
  faFilePdf,
  faFileLines,
  faFile,
  faX
);

export default {
  components: {
    DefaultLayout,
    OxTextarea,
    OxChartIcon,
    OxSlider,
    OxScoreBox,
    FontAwesomeIcon,
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    FileUpload,
  },
  setup() {
    const showCreateModal = ref(false);
    const generatingFramework = ref(false);
    const generatingMoreCriteria = ref(false);
    const saving = ref(false);
    const scoringSubjects = ref(false);
    const generatingSubjects = ref(false);
    const subjectsError = ref(false);
    const finishedCriteriaSelection = ref(false);
    const finishedCriteriaWeight = ref(false);
    const subjectsScoredByOx = ref(false);
    const subjectsScoredByUser = ref(false);
    const errorScoringSubjects = ref(false);
    const errorSaving = ref(false);
    const creatingUser = ref(false);
    const createdUser = ref(false);
    const sourceGeneralKnowledge = ref(true);
    const sourceSearch = ref(false);
    const sourceNews = ref(false);
    const sourceCustom = ref(false);
    const sourceCustomText = ref(false);
    const sourceCustomDocs = ref(false);
    const draggingOver = ref(false);
    const showLogIn = ref(false);
    const sourceUrls = ref("");
    const sourceText = ref("");
    const gptInstanceGUID = ref(Date.now().toString(36) + Math.random().toString(36).substring(2));

    const generatedFramework = ref({});
    const highlightedCriteriaForRemoval = ref({});
    const urlsUsed = ref([]);
    const topic = ref("");
    const topic_context = ref("");
    const scoring_context = ref("");
    const subjects = ref("");
    const newUserFirstName = ref("");
    const newUserLastName = ref("");
    const newUserEmail = ref("");
    const newUserPassword = ref("");
    const newUserOxId = ref("");
    const creationErrorMessage = ref("");
    const generatingFrameworkError = ref("");
    const generatingSubjectsError = ref("");
    const scoringSubjectsError = ref("");
    const analyzingStatusMessage = ref([]);
    const scorecards = ref({});
    const selectedTab = ref(0);
    document.title = "OxGPT Framework Generator";

    const totalSize = ref(0);
    const totalSizePercent = ref(0);
    const files = ref({});
    const uploadedFiles = ref({});

    return {
      aurochsData: useAurochsData(),
      showCreateModal,
      generatingFramework,
      generatingMoreCriteria,
      subjectsError,
      saving,
      finishedCriteriaSelection,
      finishedCriteriaWeight,
      scoringSubjects,
      generatingSubjects,
      subjectsScoredByOx,
      subjectsScoredByUser,
      errorScoringSubjects,
      errorSaving,
      creatingUser,
      createdUser,
      sourceGeneralKnowledge,
      sourceSearch,
      sourceNews,
      sourceCustom,
      sourceCustomText,
      sourceCustomDocs,
      showLogIn,
      sourceUrls,
      sourceText,
      generatedFramework,
      highlightedCriteriaForRemoval,
      urlsUsed,
      topic,
      topic_context,
      scoring_context,
      subjects,
      newUserFirstName,
      newUserLastName,
      newUserEmail,
      newUserPassword,
      newUserOxId,
      creationErrorMessage,
      generatingFrameworkError,
      generatingSubjectsError,
      scoringSubjectsError,
      analyzingStatusMessage,
      scorecards,
      chart_colors,
      selectedTab,
      totalSize,
      totalSizePercent,
      files,
      uploadedFiles,
      draggingOver,
      gptInstanceGUID,
    };
  },
  computed: {
    report() {
      return { id: 1, framework: this.generatedFramework };
    },
    sortedScorecards() {
      let sc = this.scorecards.slice();
      sc.sort((a, b) => this.oxScore(b) - this.oxScore(a));
      return sc;
    },
    newUserFormIsValid() {
      return (
        this.validNewUserFirstName && this.validNewUserLastName && this.validNewUserEmail && this.validNewUserPassword
      );
    },
    loginFormIsValid() {
      return this.validNewUserEmail && this.validNewUserPassword;
    },
    validNewUserFirstName() {
      return this.newUserFirstName.length > 0;
    },
    validNewUserLastName() {
      return this.newUserLastName.length > 0;
    },
    validNewUserEmail() {
      return (
        this.newUserEmail.length > 0 && this.newUserEmail.indexOf("@") != -1 && this.newUserEmail.indexOf(".") != -1
      );
    },
    validNewUserPassword() {
      return this.newUserPassword.length > 0;
    },
    handAnalyzeSet() {
      return (
        !this.sourceGeneralKnowledge && !this.sourceSearch && !this.sourceNews && !this.sourceCustom && !this.sourceText
      );
    },
    subjectsErrorShowing() {
      return this.subjectsError && this.subjects == "";
    },
    statusUpdatesSorted() {
      // console.log("statusUpdatesSorted")
      let messages = [...this.analyzingStatusMessage];
      let deduplicated_messages = {};

      // Handle race conditions.
      for (let m of messages) {
        // console.log([m.sentAt, m.complete, m.message])
        if (m.message in deduplicated_messages) {
          if (m.complete) {
            deduplicated_messages[m.message].complete = true;
          } else {
            deduplicated_messages[m.message].sentAt = m.sentAt;
          }
        } else {
          deduplicated_messages[m.message] = m;
        }
      }
      // console.log(messages)
      // console.log(deduplicated_messages)
      let ret_messages = [];
      for (let i in deduplicated_messages) {
        ret_messages.push(deduplicated_messages[i]);
      }
      ret_messages.sort((a, b) => {
        return a.sentAt - b.sentAt;
      });

      return ret_messages;
    },
  },
  mounted() {
    this.emitter.on("oxgpt_event", this.handleOxGPTEvent);
  },
  methods: {
    async generateFramework() {
      this.finishedCriteriaSelection = false;
      this.generatedFramework = {};
      this.generatingFramework = true;
      this.generatingFrameworkError = "";
      this.scorecards = [];
      this.subjects = [];
      this.scoring_context = "";
      this.scoringSubjects = false;
      this.generatingSubjects = false;
      this.subjectsScoredByOx = false;
      let data = {
        topic: this.topic,
        topic_context: this.topic_context,
        gptInstanceGUID: this.gptInstanceGUID,
      };
      this.$generateFrameworkTimeout = setTimeout(this.showGenerateFrameworkSlow, 5000);
      await this.$sendEvent("oxgpt_generate_framework", data);
    },
    showGenerateFrameworkSlow() {
      this.generatingFrameworkError = "Hang in there, it'll just be a moment more.";
      this.$generateFrameworkTimeout = setTimeout(this.showGenerateFrameworkError, 25000);
    },
    showGenerateFrameworkError() {
      this.generatingFrameworkError =
        "Looks like we had an issue generating that framework.  Please give it another try!";
      this.generatingFramework = false;
    },
    handleOxGPTEvent(data) {
      if (data.data.gptInstanceGUID == this.gptInstanceGUID) {
        if (data.data.event_type == "generate-more-criteria") {
          this.handleGenerateMoreCriteria(data.data);
          return;
        }
        if (data.data.event_type == "generate-framework") {
          this.handleGenerateFramework(data.data);
          return;
        }
        if (data.data.event_type == "analyze-subjects") {
          this.handleScoreSubjects(data.data);
          return;
        }
        if (data.data.event_type == "generate-subjects") {
          this.handleGenerateSubjects(data.data);
          return;
        }
        if (data.data.event_type == "analyze-status-update") {
          this.handleStatusUpdate(data.data);
          return;
        }
        if (data.data.event_type == "analyze-file-contents") {
          this.handleFileAnalysis(data.data);
          return;
        }
      }
    },
    handleGenerateFramework(data) {
      if (this.generatingFramework) {
        if (this.$generateFrameworkTimeout) {
          clearTimeout(this.$generateFrameworkTimeout);
        }
        this.generatedFramework = data.framework;
        this.generatingFramework = false;
        this.generatingFrameworkError = "";
        setTimeout(() => this.$refs.seeGeneratedCriteria.scrollIntoView({ behavior: "smooth" }), 150);
      }
    },
    generateMoreCriteria() {
      this.generatingMoreCriteria = true;
      let data = {
        topic: this.topic,
        topic_context: this.topic_context,
        criteria: this.generatedFramework.criteria,
        gptInstanceGUID: this.gptInstanceGUID,
      };
      this.$sendEvent("oxgpt_generate_more_criteria", data);
    },
    handleGenerateMoreCriteria(data) {
      if (this.generatingMoreCriteria) {
        this.generatedFramework.criteria.push(...data.criteria);
        if (this.$refs.editCriteria) {
          this.$refs.editCriteria.updateFromSource();
        }
        this.generatingMoreCriteria = false;
      }
    },
    removeCriteria(idx) {
      this.clearPotentialRemoveCriteria(idx);
      this.generatedFramework.criteria.splice(idx, 1);
    },
    finishCriteriaSelection() {
      this.finishedCriteriaSelection = true;
      // setTimeout(() => this.$refs.weightCriteria.scrollIntoView({ behavior: "smooth" }), 150);
    },
    finishCriteriaWeight() {
      this.finishedCriteriaWeight = true;
      setTimeout(() => this.$refs.nameSubjects.scrollIntoView({ behavior: "smooth" }), 150);
    },
    finalizeAnalysis() {
      this.subjectsScoredByUser = true;
      setTimeout(() => this.$refs.finalizedScoresRef.scrollIntoView({ behavior: "smooth" }), 150);
    },
    scoreSubjects() {
      if (this.subjects == "") {
        this.subjectsError = true;
        setTimeout(() => this.$refs.nameSubjects.scrollIntoView({ behavior: "smooth" }), 150);
        return;
      }
      this.subjectsError = false;

      if (this.handAnalyzeSet) {
        let subjArr = this.subjects.split("\n");
        let scorecards = [];
        let index = 0;
        for (let sub of subjArr) {
          let sc = {
            scores: [],
            framework: this.generatedFramework,
            name: sub,
            index: index,
            // "scorer": this.framework,
          };
          let crit_index = 0;
          for (let crit of this.generatedFramework.criteria) {
            sc.scores.push({
              name: crit["name"],
              criteria: {
                name: crit["name"],
                description: crit["description"],
                weight: crit["weight"],
                index: crit_index,
              },
              score: 5,
              gpt_score: null,
              gpt_scored_last: false,
              skipped: false,
              comment: "",
            });
            crit_index++;
          }
          scorecards.push(sc);
          index++;
          // scorecards[topic]["scores"].append(
          //     {
          //         "name": crit["name"],
          //         "criteria": {
          //             "name": crit["name"],
          //             "description": crit["description"],
          //             "weight": weight,
          //         },
          //         "score": score,
          //         "gpt_score": score,
          //         "gpt_scored_last": True,
          //         "skipped": skipped,
          //         # "comment": f"OxGPT comment: {comment}\n(Raw score: {raw_score} / Independent speculation score: {separate_speculation} / Integrated speculation score: {speculation} / final score: {score} / raw skipped: {raw_skipped})",
          //         "comment": f"OxGPT comment: {comment}",
          //     }
          // )
          // weighted_score += weight * int(score)
          // max_weighted_score += weight * 10
          // # print(score, weight, weighted_score, max_weighted_score)
          // scorecards[topic]["scorer"] = {
          //     "id": oxgpt_id,
          //     "full_name": oxgpt_name,
          //     "modified_at_ms": modified_at_ms,
          // }
          // scorecards[topic]["framework"] = {
          //     "name": topic,
          //     "criteria": criteria,
          //     "id": 1,
          // }
          // scorecards[topic]["modified_at_ms"] = modified_at_ms
          // scorecards[topic]["created_at_ms"] = modified_at_ms
        }
        this.errorScoringSubjects = false;
        this.subjectsScoredByOx = true;
        this.subjectsScoredByUser = false;
        this.scoringSubjects = false;
        // this.subjectsScoredByUser = true;
        this.scorecards = scorecards;
        setTimeout(() => this.$refs.scorecardScoringEle.scrollIntoView({ behavior: "smooth" }), 150);
      } else {
        this.subjectsScoredByUser = false;
        this.scoringSubjects = true;
        this.scoreSubjectsError = "";
        this.urlsUsed = [];

        let data = {
          topic: this.topic,
          topic_context: this.topic_context,
          // scoring_context: this.scoring_context,
          scoring_context: this.topic_context,
          criteria: this.generatedFramework.criteria,
          subjects: this.subjects,
          sourceGeneralKnowledge: this.sourceGeneralKnowledge,
          sourceSearch: this.sourceSearch,
          sourceNews: this.sourceNews,
          sourceCustom: this.sourceCustom,
          sourceCustomText: this.sourceCustomText,
          sourceCustomDocs: this.sourceCustomDocs,
          sourceUrls: this.sourceUrls,
          sourceText: this.sourceText,
          fileContext: this.files,
          gptInstanceGUID: this.gptInstanceGUID,
        };
        setTimeout(() => this.$refs.bottom.scrollIntoView({ behavior: "smooth" }), 150);
        this.$scoreSubjectsTimeout = setTimeout(this.showScoreSubjectsSlow, 100);
        this.$sendEvent("oxgpt_analyze_subjects", data);
      }
    },
    handleScoreSubjects(data) {
      if (this.scoringSubjects) {
        if (this.$scoreSubjectsTimeout) {
          clearTimeout(this.$scoreSubjectsTimeout);
        }
        this.scoringSubjectsError = "";
        this.analyzingStatusMessage = [];
        try {
          this.subjectsScoredByUser = false;
          if (data.scorecards.length > 0) {
            this.scorecards = data.scorecards;
            this.errorScoringSubjects = false;
            this.subjectsScoredByOx = true;
          } else {
            this.errorScoringSubjects = true;
          }
          if (data.urls_used.length > 0) {
            this.urlsUsed = data.urls_used;
          }
          setTimeout(() => this.$refs.scorecardScoringEle.scrollIntoView({ behavior: "smooth" }), 150);
          // console.log(this.scorecards);
          this.scoringSubjects = false;
        } catch (e) {
          console.error(e);
          this.errorScoringSubjects = true;
          this.scoringSubjects = false;
        }
      }
    },
    handleStatusUpdate(data) {
      if (this.scoringSubjects) {
        this.analyzingStatusMessage.push(data);
        clearTimeout(this.$scoreSubjectsTimeout);
        this.$scoreSubjectsTimeout = setTimeout(this.showScoreSubjectsError, 995000);
        setTimeout(() => this.$refs.bottom.scrollIntoView({ behavior: "smooth" }), 150);
      }
    },
    removeFile(key) {
      delete this.files[key];
    },
    showScoreSubjectsSlow() {
      this.scoringSubjectsError =
        "Analyzing.  Sometimes this can take up to a few minutes as Ox does its research, so thanks for your patience!";
      this.$scoreSubjectsTimeout = setTimeout(this.showScoreSubjectsError, 495000);
    },
    showScoreSubjectsError() {
      this.scoringSubjectsError = "";
      this.analyzingStatusMessage = [];
      this.errorScoringSubjects = true;
      this.scoringSubjects = false;
    },
    generateSubjects() {
      this.subjectsScoredByUser = false;
      this.generatingSubjects = true;
      let data = {
        topic: this.topic,
        topic_context: this.topic_context,
        // scoring_context: this.scoring_context,
        scoring_context: this.topic_context,
        criteria: this.generatedFramework.criteria,
        subjects: this.subjects,
        gptInstanceGUID: this.gptInstanceGUID,
      };
      this.$sendEvent("oxgpt_generate_subjects", data);
    },
    handleGenerateSubjects(data) {
      if (this.generatingSubjects) {
        if (data.subjects.length > 0) {
          this.subjects = data.subjects;
        }
        setTimeout(() => this.$refs.nameSubjects.scrollIntoView({ behavior: "smooth" }), 150);
        // console.log(this.scorecards);
        this.generatingSubjects = false;
      }
    },
    handleFileUpload(event) {
      this.draggingOver = false;
      // console.log(event);
      for (let file of event.files) {
        let key = file.name + file.size;
        this.files[key] = {
          name: file.name,
          complete: false,
          file: file,
          size: file.size,
        };
        const reader = new FileReader();
        let v = this;

        // Define what should happen once the file is read
        reader.onload = function (event) {
          // event.target.result contains the Base64-encoded string
          const base64String = event.target.result.split(",")[1]; // Remove the prefix
          let data = {
            name: file.name,
            size: file.size,
            content: base64String,
            gptInstanceGUID: v.gptInstanceGUID,
          };
          v.$sendEvent("oxgpt_analyze_file", data);
        };
        // Read the file as a data URL to get a Base64-encoded string
        reader.readAsDataURL(file);
      }
    },
    handleFileAnalysis(data) {
      let key = String(data.filename) + String(data.size);

      this.files[key].text = data.text;
      this.files[key].num_words = data.num_words;
      this.files[key].type = data.type;
      this.files[key].complete = true;
      // this.uploadedFiles[key] = this.files[key];
    },
    async createAccountAndSave() {
      let data = {
        first_name: this.newUserFirstName,
        last_name: this.newUserLastName,
        email: this.newUserEmail,
        password: this.newUserPassword,
        gptInstanceGUID: this.gptInstanceGUID,
      };
      let ret = await this.$sendEvent("oxgpt_create_account", data);
      // console.log(ret);
      if (ret.data.success) {
        this.createdUser = true;
        this.newUserOxId = ret.data.ox_id;
        await this.saveFrameworkAndScores();
      } else {
        // console.log(ret);
        this.createdUser = false;
        this.saving = false;
        this.creationErrorMessage = ret.data.error_message;
      }
    },
    async logInAndSave() {
      let data = {
        email: this.newUserEmail,
        password: this.newUserPassword,
        gptInstanceGUID: this.gptInstanceGUID,
      };
      let ret = await this.$sendEvent("oxgpt_log_in", data);
      // console.log(ret);
      if (ret.data.success) {
        this.createdUser = true;
        this.newUserOxId = ret.data.ox_id;
        await this.saveFrameworkAndScores();
      } else {
        // console.log(ret);
        this.createdUser = false;
        this.saving = false;
        this.creationErrorMessage = ret.data.error_message;
      }
    },
    async saveFrameworkAndScores() {
      // this.subjectsScoredByUser = false;
      // this.scoringSubjects = true;
      let ret = {};
      if ((this.aurochsData && this.aurochsData.user) || this.newUserOxId) {
        this.saving = true;
        let docNames = [];
        if (this.files) {
          for (let f in this.files) {
            docNames.push(this.files[f].name);
          }
        }
        let data = {
          topic: this.topic,
          topic_context: this.topic_context,
          subjects: this.subjects,
          // scoring_context: this.scoring_context,
          scoring_context: this.topic_context,
          framework: this.generatedFramework,
          scorecards: this.scorecards,
          public_oxid: this.newUserOxId || "",
          password: this.newUserPassword || "",
          urlsUsed: this.urlsUsed || "",
          docNames: docNames || [],
          gptInstanceGUID: this.gptInstanceGUID,
        };
        try {
          let ret = await this.$sendEvent("oxgpt_save_results", data);
          if (ret.success) {
            // console.log(ret);
            if (this.createdUser) {
              window.location = `/${ret.data.target_obj_type}/${ret.data.target_obj_ox_id}`;
            } else {
              this.$router.push(`/${ret.target_obj_type}/${ret.target_obj_ox_id}`);
            }
            this.saving = false;
          } else {
            setTimeout(() => this.$refs.bottom.scrollIntoView({ behavior: "smooth" }), 150);
          }
          // console.log(this.scorecards);
          // this.scoringSubjects = false;
          // this.subjectsScoredByOx = true;
        } catch (e) {
          console.log(e);
          this.errorSaving = true;
          this.saving = false;
        }
      } else {
        this.saving = false;
        this.creatingUser = true;
      }
      return ret;
    },
    oxScore(scorecard) {
      let total = 0;
      let max = 0;
      for (let sc of scorecard.scores) {
        if (!sc.skipped) {
          total += sc.score * this.getCriteriaWeight(sc.criteria);
          max += 10 * sc.criteria.weight;
        }
      }
      if (max > 0) {
        return ((100 * total) / max).toFixed(0);
      }
      return 0;
    },
    hasSkipped(scorecard) {
      let skipped = false;
      for (let sc of scorecard.scores) {
        if (sc.skipped) {
          skipped = true;
          break;
        }
      }
      return skipped;
    },
    getCriteriaWeight(criteria) {
      for (let c of this.generatedFramework.criteria) {
        if (c.name == criteria.name) {
          return c.weight;
        }
      }
      return criteria.weight;
    },
    image_url(file_name) {
      let url =
        window.aurochs.data.config.guide_image_url.substring(
          0,
          window.aurochs.data.config.guide_image_url.indexOf("/intel") + 1
        ) + file_name;
      return url.replaceAll("/images/guide", "");
    },
    darkMode() {
      return (
        (!this.aurochsData.theme && window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ||
        this.aurochsData.theme == "dark"
      );
    },
    potentialRemoveCriteria(idx) {
      this.highlightedCriteriaForRemoval[String(idx)] = true;
    },
    clearPotentialRemoveCriteria(idx) {
      delete this.highlightedCriteriaForRemoval[String(idx)];
    },
    isHighlightedForRemoval(idx) {
      return idx in this.highlightedCriteriaForRemoval && this.highlightedCriteriaForRemoval[idx] === true;
    },
    getCriteriaColor(idx) {
      const color_idx = idx % this.chart_colors.length;
      return `background-color: ${this.chart_colors[color_idx]};`;
    },
    addBlankCriteria() {
      let nextIndex = 1;
      if (this.generatedFramework.criteria.length > 0) {
        nextIndex = this.generatedFramework.criteria.slice(-1)[0].index + 1;
      }
      this.generatedFramework.criteria.push({
        name: "",
        weight: 5,
        description: "",
        index: nextIndex,
      });
    },
    strippedUrl(url) {
      if (url.indexOf("?") != -1) {
        return url.slice(0, url.indexOf("?"));
      }
      return url;
    },
    onRemoveTemplatingFile(file, removeFileCallback, index) {
      removeFileCallback(index);
      this.totalSize -= parseInt(this.formatSize(file.size));
      this.totalSizePercent = this.totalSize / 10;
    },
    onClearTemplatingUpload(clear) {
      clear();
      this.totalSize = 0;
      this.totalSizePercent = 0;
    },
    onSelectedFiles(event) {
      // this.files.forEach((file) => {
      //     this.totalSize += parseInt(this.formatSize(file.size));
      // });
      for (let file of event.files) {
        let key = file.name + file.size;
        this.files[key] = {
          name: file.name,
          complete: false,
          file: file,
          size: file.size,
        };
      }
    },
    uploadEvent(callback) {
      this.totalSizePercent = this.totalSize / 10;
      callback();
    },
    onTemplatedUpload() {
      // toast.add({ severity: "info", summary: "Success", detail: "File Uploaded", life: 3000 });
    },
    formatSize(bytes) {
      if (bytes === 0) return "0 B";
      const k = 1024;
      const sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
    },
    formatNumber(num) {
      try {
        return num.toLocaleString();
      } catch (e) {
        return num;
      }
    },
    handleDragOver() {
      this.draggingOver = true;
    },
    handleDragLeave() {
      this.draggingOver = false;
    },
    openFileChooser() {
      // Select this and call click.
      document.querySelector("[data-pc-section=input]").click();
    },
  },
};
</script>

<style scoped>
html {
  @apply h-full;
}

::placeholder,
input::placeholder,
textarea::placeholder,
.textarea::placeholder {
  @apply text-dark-grey;
  opacity: 0.7;
}
body {
  @apply h-full;
}
.unscored-criteria {
  transition-duration: 0.2s;
}

.prose {
  max-width: 80vw;
  width: 80vw;
}
.dot-container {
  @apply mt-8 text-primary;
  display: flex;
  justify-content: center;
  align-items: center;
}

.dot {
  @apply bg-primary;
  width: 10px;
  height: 10px;
  margin: 0 5px;
  /*  background-color: #000;*/
  border-radius: 50%;
  animation: bounce 1s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}
.tabs {
  @apply justify-center;
}

@keyframes bounce {
  0%,
  80%,
  100% {
    transform: translateY(0);
  }

  40% {
    transform: translateY(-10px);
  }
}
li {
  list-style-type: disc;
  margin-left: 1.5rem;
}
div[data-pc-section="buttonbar"] {
  display: none;
}
div[data-pc-section="content"] {
  @apply bg-base-200;
}
</style>
<style>
div[data-pc-section="buttonbar"] {
  display: none;
  @apply border-0;
}
div[data-pc-section="content"] {
  @apply bg-base-200 border-0;
}
div[data-pc-section="content"].dragging {
  @apply bg-base-300 border-0;
}
</style>
