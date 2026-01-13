<template>
  <DefaultLayout>
    <div v-if="!report || !canSee">
      <div class="w-full min-h-[75vh]">
        <div class="card w-full bg-base-200 card-bordered mt-32 mx-auto max-w-screen-md" data-cy="not-found">
          <div v-if="!report" class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <OxObjectIcon :type="'report'" :classes="'h-12 w-12'" :greyscale="true" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Report not found.</div>
                <div class="text-xl text-dark-grey">
                  This report either doesn't exist, or you don't have permissions to view it.
                </div>
              </div>
            </div>
          </div>
          <div v-else class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <FontAwesomeIcon :icon="['fad', 'lock']" class="h-12 w-12 text-medium-grey" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Report is private.</div>
                <div class="text-xl text-dark-grey">
                  You don't have permissions to view this report. If you think this is incorrect, please contact an
                  administrator: {{ admin_list }}.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <template v-if="report && canSee">
      <main class="overflow-x-hidden" data-cy="report">
        <div class="w-full">
          <!-- Main Space -->
          <div class="w-full min-h-[75vh]">
            <div class="w-full">
              <div class="w-full">
                <div class="w-full">
                  <article class="prose max-w-none">
                    <div class="flex justify-between gap-2 lg:flex-nowrap flex-wrap">
                      <div class="flex flex-nowrap mb-4 w-full">
                        <OxObjectIcon
                          :type="'report'"
                          :classes="(report?.subtitle || editing ? 'w-12 h-12' : 'w-12 h-12') + ' mr-4 align-middle'"
                        />
                        <div class="block grow">
                          <h1 class="py-0 my-0">
                            <div v-if="!editing" data-cy="name" :class="report?.subtitle ? 'mt-0.5' : 'mt-1'">
                              {{ report?.name }}
                            </div>
                            <div v-if="editing" class="w-full max-w-[70vw]">
                              <input
                                v-model="formData.name"
                                data-cy="input-report-name"
                                placeholder="Report Title"
                                autofocus
                                type="text"
                                class="w-auto max-w-100 text-4xl p-0 font-extra-bold border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-medium-grey focus:border-medium-grey text-neutral mt-0.5"
                                :style="`width: ${
                                  3 + (formData?.name?.length || 0) * 0.8
                                }ch; max-width: 100%; min-width: 250px;`"
                              />
                            </div>
                          </h1>
                          <div v-if="editing" class="w-full max-w-[70vw]">
                            <input
                              v-model="formData.subtitle"
                              data-cy="input-report-subtitle"
                              type="text"
                              placeholder="Report subtitle..."
                              class="w-auto max-w-100 text-lg font-light p-0 border-x-0 border-t-0 border-b ring-offset-0 ring-transparent focus:ring-offset-0 focus:ring-transparent ring-0 focus:ring-0 bg-base-100 border-medium-grey focus:border-medium-grey text-neutral"
                              :style="`width: ${
                                3 + (formData?.subtitle?.length || 0) * 0.7
                              }ch; max-width: 100%; min-width: 250px;`"
                            />
                          </div>
                          <p
                            v-if="!editing"
                            class="text-lg font-light prose-p pr-4 my-0 max-h-20 p-0 overflow-hidden"
                            data-cy="subtitle"
                          >
                            {{ report?.subtitle }}
                          </p>
                        </div>
                        <template v-if="editing">
                          <button
                            type="button"
                            role="button"
                            data-cy="cancel"
                            class="ml-8 btn btn-outline btn-base-300 hover:btn-error mr-2"
                            @click="cancel"
                          >
                            <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2 w-4 h-4 align-middle" />
                            Cancel
                          </button>
                          <button
                            type="button"
                            role="button"
                            data-cy="save"
                            class="btn btn-success"
                            :class="saving ? 'saving' : ''"
                            :disabled="saving"
                            @click="saveReport"
                          >
                            <FontAwesomeIcon
                              v-if="!saving"
                              :icon="['fad', 'check']"
                              class="mr-2 w-4 h-4 align-middle"
                            />
                            <FontAwesomeIcon
                              v-if="saving"
                              :icon="['fad', 'rotate']"
                              class="mr-2 w-4 h-4 align-middle fa-spin"
                            />
                            {{ saving ? "Saving..." : "Save" }}
                          </button>
                        </template>

                        <template v-if="!editing">
                          <label
                            v-if="canScore"
                            data-cy="add-scorecard"
                            role="button"
                            class="btn btn-primary"
                            for="add-scorecard-modal"
                          >
                            <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2 align-middle" />
                            Add Scorecard
                          </label>

                          <button
                            v-if="canEdit"
                            data-cy="edit"
                            type="button"
                            role="button"
                            title="Edit Report"
                            class="btn btn-outline btn-primary ml-2"
                            @click="startEditing"
                          >
                            <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2 align-middle" />
                            Edit
                          </button>
                          <div class="dropdown dropdown-end">
                            <button
                              v-if="canView"
                              data-cy="download-report"
                              type="button"
                              role="button"
                              title="Download Report"
                              class="btn btn-outline btn-primary whitespace-nowrap block ml-2"
                              tabindex="40"
                            >
                              <FontAwesomeIcon :icon="['fad', 'download']" class="mr-2 align-middle" />
                              Export
                            </button>
                            <ul
                              tabindex="0"
                              class="dropdown-content menu p-2 mt-0 shadow-md bg-base-100 rounded-box w-auto whitespace-nowrap"
                            >
                              <li>
                                <a href="#" class="no-underline" @click="openDownload()">
                                  <FontAwesomeIcon :icon="['fad', 'file-pdf']" class="mr-2 w-8 h-8" />
                                  Download PDF
                                </a>
                              </li>
                              <li>
                                <a href="#" class="no-underline" @click="downloadCSV()">
                                  <FontAwesomeIcon :icon="['fad', 'file-csv']" class="mr-2 w-8 h-8" />
                                  Download CSV
                                </a>
                              </li>
                              <!-- <li>
                                <a href="#" class="no-underline" @click="downloadPPT()">
                                  <FontAwesomeIcon :icon="['fad', 'file-powerpoint']" class="mr-2 w-8 h-8" />
                                  Download Powerpoint
                                </a>
                              </li> -->
                            </ul>
                          </div>
                          <!--                         <button
                          data-cy="open-permissions"
                          type="button"
                          role="button"
                          title="Permissions"
                          class="btn btn-outline btn-primary  ml-2"
                          @click="openPermissions"
                        >
                          <FontAwesomeIcon :icon="['fad', 'unlock']" class="mr-2 align-middle" />
                          Permissions
                        </button> -->
                          <button
                            v-if="canManage"
                            type="button"
                            role="button"
                            data-cy="delete"
                            title="Delete Report"
                            class="btn btn-outline btn-error ml-2"
                            :class="deleting ? 'disabled btn-disabled' : ''"
                            :disabled="deleting"
                            @click="deleteReport"
                          >
                            <FontAwesomeIcon :icon="['fad', 'trash-can']" class="mr-2 align-middle" />
                            Delete
                          </button>
                        </template>
                      </div>
                    </div>
                    <div class="flex justify-between">
                      <div v-if="!editing">
                        <OxStackBadges :object="report" :can-add="true" />
                        <OxTags class="mt-2" :target="report" :can-edit="canEdit" />
                      </div>
                      <div
                        v-if="!editing && canView && report?.ox_score !== null"
                        class="flex-nowrap"
                        :class="report?.subtitle ? ' -mt-6' : ' -mt-2'"
                      >
                        <div class="stats lg:stats-horizontal shadow overflow-x-visible rounded-lg">
                          <div
                            data-cy="average-ox-score"
                            class="stat rounded-l-lg text-ox-score-content place-items-center"
                            :class="
                              (report?.has_skipped ? 'bg-medium-grey' : 'bg-ox-score') +
                              (report?.feedback_score ||
                              report?.feedback_score === 0 ||
                              (report?.feedback_score != '' && report?.feedback_score != null)
                                ? ' '
                                : ' rounded-r-lg')
                            "
                          >
                            <div class="">Average Ox Score</div>
                            <div class="stat-value" :class="report?.has_skipped ? 'ml-4' : ''">
                              {{ report?.ox_score }}<span class="text-xl">%</span>
                              <div
                                v-if="report?.has_skipped"
                                data-cy="star"
                                class="z-50 star tooltip tooltip-left cursor-pointer"
                                data-tip="At least one criteria was skipped by all scorers."
                              >
                                <div class="text-md">*</div>
                              </div>
                            </div>
                          </div>
                          <div
                            v-if="
                              report?.feedback_score ||
                              report?.feedback_score === 0 ||
                              (report?.feedback_score != '' && report?.feedback_score != null)
                            "
                            class="stat place-items-center"
                          >
                            <div class="stat-title">Outcome Score</div>
                            <div class="stat-value">
                              {{ Math.round(report?.feedback_score) }}<span class="text-xl">%</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </article>
                </div>
              </div>
            </div>

            <div class="lg:min-w-0 lg:flex-1">
              <!-- MAIN SPACE -->
              <ReportsTab
                :report="report"
                :scorecards-by-framework="scorecardsByFramework"
                @permissions-updated="permissionsUpdated"
              />
              <!-- <div class="pb-16 flex" :class="report?.scorecards.length == 0 ? 'mt-24' : ''">
                <OxTags :target="report" :can-edit="canEdit" />
                <div class="box max-w-fit b-base-300 border rounded-md p-4 text-sm">
                  <div>
                    <b>Updated</b>
                    {{ report?.modified_by ? "by " + report?.modified_by.full_name : "" }}
                    {{ report?.modified_at_ms ? "on " + formatDate(report.modified_at_ms) : "" }}.
                  </div>
                  <div>
                    <b>Created</b>
                    {{ report?.created_by ? "by " + report?.created_by.full_name : "" }}
                    {{ report?.created_at_ms ? "on " + formatDate(report.created_at_ms) : "" }}.
                  </div>
                </div>
              </div> -->
            </div>
          </div>
        </div>
        <input id="add-scorecard-modal" type="checkbox" class="modal-toggle" />
        <div class="modal">
          <div
            :class="
              'modal-box relative' + (showOxGPTFlow ? 'w-screen-lg max-w-screen-lg' : 'w-screen-md max-w-screen-md')
            "
            data-cy="scorecard-framework-search"
          >
            <label class="btn btn-sm btn-circle absolute right-4 top-4" @click="closeAddScorecard">✕</label>
            <h3 class="text-lg font-bold">Add Scorecard</h3>
            <p class="py-4 font-bold">Which framework would you like to use?</p>
            <OxSearchBox
              :options="possibleFrameworks"
              :placeholder="'Search for a framework...'"
              @selected-choice="setAddScorecardFramework"
            />
            <div v-if="!showOxGPTFlow" class="flex justify-end gap-8">
              <div
                data-cy="add-scorecard-from-modal"
                role="button"
                class="mt-4 btn btn-outline"
                :class="addScorecardFramework && !addingScorecard ? '' : 'btn-disabled'"
                @click="addScorecard()"
              >
                {{ addingScorecard ? "Adding..." : "Score manually" }}
              </div>
              <div
                v-if="!addingScorecard"
                data-cy="add-scorecard-from-modal"
                role="button"
                class="mt-4 btn btn-primary"
                :class="addScorecardFramework && !addingScorecard ? '' : 'btn-disabled'"
                @click="addOxGPTScorecard()"
              >
                {{ addingScorecard ? "Adding..." : "Score with AI" }}
              </div>
            </div>
            <div v-if="showOxGPTFlow">
              <div class="mb-2 mt-12 font-bold">
                Share any context or guidance you'd like Ox to consider (recommended):
              </div>
              <OxTextarea
                v-model="topic_context"
                class="w-full"
                placeholder="Add any additional context that you feel is very important, explaining it as you would to an expert in the topic.

Context could include things like your job or sector, criteria that you care more about, your risk tolerance, your long-term outlook, how thorough the due dlligence process needs to be, etc."
                input-type="textarea"
              />
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
                    <FontAwesomeIcon
                      v-if="sourceNews"
                      :icon="['fad', 'check']"
                      class="h-4 w-4 mr-2"
                      aria-hidden="true"
                    />
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
                                <div v-if="!file.complete" class="mx-auto badge badge-warning mt-3 w-20">
                                  Analyzing..
                                </div>
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
                                  <FontAwesomeIcon
                                    v-if="!file.type"
                                    :icon="['fad', 'file']"
                                    class="mt-2 h-8 w-8 -ml-1"
                                  />
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
              <div class="flex justify-between">
                <div
                  v-if="!scoringSubjects && !subjectsScoredByOx"
                  class="btn btn-outline text-medium-grey border-medium-grey"
                  @click="showOxGPTFlow = false"
                >
                  Cancel
                </div>
                <div v-if="!scoringSubjects && !subjectsScoredByOx" class="btn btn-primary" @click="scoreSubjects">
                  Analyze using Ox AI
                  <FontAwesomeIcon :icon="['fad', 'angle-right']" class="h-4 w-4 ml-2 align-middle" />
                </div>
              </div>
              <div v-if="scoringSubjects">&nbsp;</div>
            </div>
            <div ref="bottom">
              <div v-if="scoringSubjectsError" class="mt-4">
                {{ scoringSubjectsError }}
              </div>
              <div v-if="errorScoringSubjects" ref="errorScoringSubjects" class="mt-4">
                <div class="alert alert-warning alert-outline my-4 mx-auto max-w-screen-md p-6">
                  <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="h-10 w-10 mr-2 mt-8" />
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
                v-if="(scoringSubjects && statusUpdatesSorted) || subjectsScoredByOx"
                class="mt-2 mb-20 text-left max-w-screen-md mx-auto"
              >
                <div class="font-bold mb-1 text-xl">
                  <span v-if="!subjectsScoredByOx">Analyzing</span><span v-if="subjectsScoredByOx">Analyzed</span> using
                  Ox AI<span v-if="!subjectsScoredByOx">.</span><span v-if="subjectsScoredByOx">:</span>
                </div>
                <div v-if="!subjectsScoredByOx" class="mb-2">
                  Sometimes this can take up to a few minutes as Ox does its research, so thanks for your patience!
                </div>
                <div v-for="(message, idx) in statusUpdatesSorted" :key="idx">
                  <div :class="'flex ' + (message.inset ? 'pl-6' : '')">
                    <FontAwesomeIcon
                      v-if="message.complete || subjectsScoredByOx"
                      :icon="['fad', 'check']"
                      class="h-4 w-4 mr-2 mt-1 pt-0.5"
                    />
                    <FontAwesomeIcon
                      v-if="!message.complete && !subjectsScoredByOx"
                      :icon="['fas', 'spinner-third']"
                      class="h-4 w-4 mr-2 mt-1 pt-0.5 fa-spin opacity-50"
                    />
                    <div v-html="message.message"></div>
                  </div>
                </div>
                <div v-if="subjectsScoredByOx" class="flex text-left">
                  <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2 mt-1 pt-0.5" />
                  <div class="font-bold">Scoring complete.</div>
                </div>
              </div>
              <div v-if="scoringSubjects">
                <div class="dot-container mb-8">
                  <div class="dot"></div>
                  <div class="dot"></div>
                  <div class="dot"></div>
                </div>
              </div>
              <div v-if="subjectsScoredByOx" class="w-full">
                <div class="flex justify-end">
                  <div
                    :class="'btn ' + (savingScorecard ? 'btn-disabled' : 'btn-primary')"
                    @click="saveFrameworkAndScores"
                  >
                    <span v-if="!savingScorecard">Save and View Scorecard</span>
                    <FontAwesomeIcon
                      v-if="!savingScorecard"
                      :icon="['fad', 'angle-right']"
                      class="h-4 w-4 ml-2 align-middle"
                    />
                    <FontAwesomeIcon
                      v-if="savingScorecard"
                      :icon="['fas', 'spinner-third']"
                      class="h-4 w-4 mr-2 mt-1 pt-0.5 fa-spin opacity-50"
                    />
                    <span v-if="savingScorecard">Saving...</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <DownloadPDFModal :target="report" :is-open="downloadModalOpen" @close="closeDownload" />
      </main>
      <OxOwnerFooter :object="report" />
    </template>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "../layouts/DefaultLayout.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faUnlock } from "@fortawesome/pro-duotone-svg-icons/faUnlock";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faFileCsv } from "@fortawesome/pro-duotone-svg-icons/faFileCsv";
import { faClone } from "@fortawesome/pro-duotone-svg-icons/faClone";
import { faPen } from "@fortawesome/pro-duotone-svg-icons/faPen";
import { faFileLines } from "@fortawesome/pro-duotone-svg-icons/faFileLines";
import { faChartSimpleHorizontal } from "@fortawesome/pro-duotone-svg-icons/faChartSimpleHorizontal";
import { faCompass } from "@fortawesome/pro-duotone-svg-icons/faCompass";
import { faMessages } from "@fortawesome/pro-duotone-svg-icons/faMessages";
import { faFiles } from "@fortawesome/pro-duotone-svg-icons/faFiles";
import { faFilePdf } from "@fortawesome/pro-duotone-svg-icons/faFilePdf";
import { faFilePowerpoint } from "@fortawesome/pro-duotone-svg-icons/faFilePowerpoint";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faRotate } from "@fortawesome/pro-duotone-svg-icons/faRotate";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faLayerPlus } from "@fortawesome/pro-light-svg-icons/faLayerPlus";
import { faDownload } from "@fortawesome/pro-duotone-svg-icons/faDownload";
import { faMinus } from "@fortawesome/pro-duotone-svg-icons/faMinus";
import { faRepeat } from "@fortawesome/pro-duotone-svg-icons/faRepeat";
import { faAngleRight } from "@fortawesome/pro-duotone-svg-icons/faAngleRight";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";
import { faSpinnerThird } from "@fortawesome/pro-duotone-svg-icons/faSpinnerThird";
import { faFileDoc } from "@fortawesome/pro-duotone-svg-icons/faFileDoc";
import { faFile } from "@fortawesome/pro-duotone-svg-icons/faFile";
import { faX } from "@fortawesome/pro-duotone-svg-icons/faX";

library.add(
  faUnlock,
  faTrashCan,
  faFileCsv,
  faClone,
  faPen,
  faFileLines,
  faChartSimpleHorizontal,
  faCompass,
  faMessages,
  faFiles,
  faFilePdf,
  faFilePowerpoint,
  faXmark,
  faCheck,
  faRotate,
  faPlus,
  faLayerPlus,
  faDownload,
  faMinus,
  faRepeat,
  faAngleRight,
  faTriangleExclamation,
  faSpinnerThird,
  faFileDoc,
  faFile,
  faX
);

import { ref } from "vue";
import { useAurochsData } from "../stores/aurochs";
import { standardDeviation } from "../mixins/stats.js";
import { getReportScorecardsByFramework } from "../mixins/format_scorecards.js";
import { checkCanScore, checkCanView, checkCanEdit, checkCanManage, checkCanSee } from "../mixins/permissions.js";
import formatDate from "../mixins/format_date";
import OxTags from "../components/common/OxTags.vue";
import OxTextarea from "../components/common/forms/OxTextarea.vue";
// import OxSlider from "../components/common/forms/OxSlider.vue";
import OxStackBadges from "../components/common/OxStackBadges.vue";
import OxOwnerFooter from "../components/common/OxOwnerFooter.vue";
// import PermissionsModal from "../components/common/PermissionsModal.vue";
import DownloadPDFModal from "../components/common/DownloadPDFModal.vue";
import OxSearchBox from "../components/common/OxSearchBox.vue";
import OxObjectIcon from "../components/common/icons/OxObjectIcon.vue";
import ReportsTab from "../components/reports/ReportsTab.vue";
import DownloadMixin from "../mixins/download_file";
import FileUpload from "primevue/fileupload";

export default {
  components: {
    DefaultLayout,
    // PermissionsModal,
    DownloadPDFModal,
    OxSearchBox,
    OxTags,
    ReportsTab,
    // OxSlider,
    OxStackBadges,
    OxOwnerFooter,
    OxTextarea,
    OxObjectIcon,
    FontAwesomeIcon,
    FileUpload,
  },
  mixins: [standardDeviation, formatDate, DownloadMixin],
  props: {
    id: {
      type: String,
      required: true,
    },
    new: {
      type: Boolean,
      default: false,
    },
    dataCy: {
      type: String,
      default: () => "",
    },
  },
  emits: ["permissions-updated"],
  setup(props) {
    const expanded = ref(false);
    const addingScorecard = ref(false);
    const addingOxGPTScorecard = ref(false);
    const showOxGPTFlow = ref(false);
    const permissionsModalOpen = ref(false);
    const downloadModalOpen = ref(false);
    const expandedPanel = ref("");
    const addScorecardFramework = ref(null);
    const saving = ref(false);
    const deleting = ref(false);
    const scoringSubjects = ref(false);
    const savingScorecard = ref(false);
    const subjectsScoredByOx = ref(false);
    const errorScoringSubjects = ref(false);

    const sourceGeneralKnowledge = ref(true);
    const sourceSearch = ref(false);
    const sourceNews = ref(false);
    const sourceCustom = ref(false);
    const sourceCustomText = ref(false);
    const sourceCustomDocs = ref(false);
    const draggingOver = ref(false);
    const gptInstanceGUID = ref(Date.now().toString(36) + Math.random().toString(36).substring(2));
    const sourceUrls = ref("");
    const sourceText = ref("");
    const topic_context = ref("");
    const scoringSubjectsError = ref("");
    const analyzingStatusMessage = ref([]);

    const totalSize = ref(0);
    const totalSizePercent = ref(0);
    const files = ref({});
    const uploadedFiles = ref({});
    const scorecards = ref({});

    const is_new = ref(props.new);
    const editing = ref(props.new);
    let formData = {};

    return {
      aurochsData: useAurochsData(),
      expanded,
      expandedPanel,
      addingScorecard,
      addingOxGPTScorecard,
      showOxGPTFlow,
      permissionsModalOpen,
      addScorecardFramework,
      editing,
      saving,
      deleting,
      downloadModalOpen,
      savingScorecard,
      // report,
      is_new,
      formData: ref(formData),
      sourceGeneralKnowledge,
      sourceSearch,
      sourceNews,
      sourceCustom,
      sourceCustomText,
      sourceCustomDocs,
      topic_context,
      draggingOver,
      sourceUrls,
      sourceText,
      totalSize,
      totalSizePercent,
      files,
      uploadedFiles,
      scorecards,
      analyzingStatusMessage,
      scoringSubjects,
      subjectsScoredByOx,
      scoringSubjectsError,
      gptInstanceGUID,
      errorScoringSubjects,
    };
  },
  computed: {
    report() {
      if (this.aurochsData.reports && this.id && String(this.id)) {
        return this.aurochsData.reports[String(this.id)];
      }
      return null;
    },
    possibleFrameworks() {
      let frameworks = [];
      for (let f_id in this.aurochsData.frameworks) {
        let f = this.aurochsData.frameworks[f_id];
        if (checkCanSee(f, this.aurochsData.user)) {
          frameworks.push(f);
        }
      }
      return frameworks;
    },
    admin_list() {
      let admin_str = "";
      if (this.report) {
        for (let p_id in this.report.permissions) {
          if (this.report.permissions[p_id].substring(3, 4) == "1") {
            admin_str += this.aurochsData.users[p_id.substring(2)].full_name + ", ";
          }
        }
        if (admin_str.length > 2) {
          admin_str = admin_str.slice(0, -2);
        }
      }
      return admin_str;
    },
    canScore() {
      return checkCanScore(this.report, this.aurochsData.user);
    },
    canView() {
      return checkCanView(this.report, this.aurochsData.user);
    },
    canEdit() {
      return checkCanEdit(this.report, this.aurochsData.user);
    },
    canManage() {
      return checkCanManage(this.report, this.aurochsData.user);
    },
    canSee() {
      return checkCanSee(this.report, this.aurochsData.user);
    },
    scorecardsByFramework() {
      return getReportScorecardsByFramework(this.report);
    },
    stacks() {
      if (this.report.__type == "report" && this.report.stack_ids?.length > 0) {
        let stacks = [];
        for (let s_id of this.report.stack_ids) {
          stacks.push(this.aurochsData.stacks[s_id]);
        }
        return stacks;
      }
      return [];
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
    strippedFramework() {
      let f = { ...this.addScorecardFramework };
      delete f["created_by"];
      delete f["average_feedback_score"];
      delete f["comments"];
      delete f["highest_scoring_criterion"];
      delete f["lowest_scoring_criterion"];
      delete f["modified_by"];
      delete f["permissions"];
      delete f["search_text"];
      delete f["report_id_list"];
      return f;
    },
  },
  watch: {
    id: {
      handler: function (newVal) {
        document.title = this.aurochsData.reports[String(newVal)].name;
        this.canEdit = checkCanEdit(this.report, this.aurochsData.user);
        this.canManage = checkCanManage(this.report, this.aurochsData.user);
        if (this.is_new) {
          this.editing = true;
        } else {
          this.editing = false;
        }
        this.scorecardsByFramework;
        this.formData = {
          name: this.report?.name || "",
          subtitle: this.report?.subtitle || "",
          feedback_score: this.report?.feedback_score || null,
          feedback_comment: this.report?.feedback_comment || "",
        };
      },
    },
    new: {
      handler: function (newVal) {
        this.is_new = newVal || newVal == "true" ? true : false;
        if (this.is_new) {
          this.editing = true;
        }
      },
    },
  },
  mounted() {
    // this.getNotes();
    document.title = this.report?.name || "Ox Report";
    if (this.$route.query.new) {
      this.editing = true;
      this.is_new = true;
    }
    this.emitter.on("oxgpt_event", this.handleOxGPTEvent);
  },
  methods: {
    startAddScorecard() {},
    setAddScorecardFramework(framework) {
      this.addScorecardFramework = framework;
    },
    async addOxGPTScorecard() {
      this.showOxGPTFlow = true;
    },
    async addScorecard() {
      // Do the actual add.
      this.addingScorecard = true;
      var data = {
        report_id: this.report.id,
        framework_id: this.addScorecardFramework.id,
        blank: true,
        scores: [],
      };
      await this.$sendEvent("create_scorecard", data);
      this.closeAddScorecard();

      // Switch to my scorecards
      this.$router.push(`/report/${this.report.id}/#scorecards`);

      // Clear the add dialog.
      // this.addScorecardFramework = null;
      this.emitter.emit("clearSearchBox", {
        previousSelected: this.addScorecardFramework,
      });
    },
    openDownload() {
      this.downloadModalOpen = true;
      document.getElementById("download-modal").checked = true;
    },
    closeDownload() {
      this.downloadModalOpen = false;
      document.getElementById("download-modal").checked = false;
    },
    downloadPPT() {
      let url = "/export/report/ppt/" + this.report.id;
      this.downloadFile(url, "Chart_Report_" + this.report.id, ".pptx");
    },
    startEditing() {
      this.formData = {
        name: this.report?.name || "",
        subtitle: this.report?.subtitle || "",
        feedback_score: this.report?.feedback_score || null,
        feedback_comment: this.report?.feedback_comment || "",
      };
      this.editing = true;
    },
    stopEditing() {
      this.editing = false;
    },
    permissionsUpdated() {
      // console.log("permissionsUpdated reportspage");
      this.$emit("permissions-updated");
    },
    cancel() {
      this.formData = {
        name: this.report?.name || "",
        subtitle: this.report?.subtitle || "",
        feedback_score: this.report?.feedback_score || null,
        feedback_comment: this.report?.feedback_comment || "",
      };
      this.stopEditing();
    },
    openStack(s) {
      this.$router.push(`/stack/${s.id}`);
    },
    async saveReport() {
      this.saving = true;
      const data = {
        id: this.report.id,
        name: this.formData.name,
        subtitle: this.formData.subtitle,
        feedback_score: this.formData.feedback_score,
        feedback_comment: this.formData.feedback_comment,
      };
      await this.$sendEvent("update_report", data);
      this.saving = false;
      this.stopEditing();
      if (this.is_new) {
        this.$router.push(`/report/${this.report.id}`);
      }
      this.is_new = false;
    },
    async deleteReport() {
      this.deleting = true;
      if (
        confirm(
          "Are you sure you want to delete this report?\n\nThis will also delete all scorecards within the report.\nThere is no undo.\n\nDelete report?"
        )
      ) {
        var data = {
          id: this.report.id,
        };
        await this.$sendEvent("delete_report", data);
        this.$router.push("/library");
      }
      this.deleting = false;
    },
    downloadCSV() {
      var now = new Date();
      this.downloadFile(
        "/export/report/csv/" + this.id,
        this.report?.name.replace(" ", "_").replace('"', "'") + "-" + now.toISOString(),
        ".csv"
      );
    },
    handleOxGPTEvent(data) {
      if (data.data.gptInstanceGUID == this.gptInstanceGUID) {
        if (data.data.event_type == "analyze-subjects") {
          this.handleScoreSubjects(data.data);
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
      console.log(data);

      this.files[key].text = data.text;
      this.files[key].num_words = data.num_words;
      this.files[key].type = data.type;
      this.files[key].complete = true;
      // this.uploadedFiles[key] = this.files[key];
    },
    scoreSubjects() {
      if (this.subjects == "") {
        this.subjectsError = true;
        setTimeout(() => this.$refs.nameSubjects.scrollIntoView({ behavior: "smooth" }), 150);
        return;
      }
      this.subjectsError = false;
      this.subjectsScoredByUser = false;
      this.scoringSubjects = true;
      this.scoreSubjectsError = "";
      this.urlsUsed = [];

      let data = {
        topic: this.report.name,
        topic_context: this.topic_context,
        // scoring_context: this.scoring_context,
        scoring_context: this.topic_context,
        criteria: this.addScorecardFramework.criteria,
        subjects: this.report.name,
        sourceGeneralKnowledge: this.sourceGeneralKnowledge,
        sourceSearch: this.sourceSearch,
        sourceNews: this.sourceNews,
        sourceCustom: this.sourceCustom,
        sourceCustomText: this.sourceCustomText,
        sourceCustomDocs: this.sourceCustomDocs,
        sourceUrls: this.sourceUrls,
        sourceText: this.sourceText,
        gptInstanceGUID: this.gptInstanceGUID,
        fileContext: { ...this.files },
      };
      // console.log(data);
      setTimeout(() => this.$refs.bottom.scrollIntoView({ behavior: "smooth" }), 150);
      this.$scoreSubjectsTimeout = setTimeout(this.showScoreSubjectsSlow, 100);
      this.$sendEvent("oxgpt_analyze_subjects", data);
    },
    handleScoreSubjects(data) {
      // console.log("handleScoreSubjects");
      // console.log(data);
      // console.log(this.scoringSubjects);
      if (this.scoringSubjects) {
        if (this.$scoreSubjectsTimeout) {
          clearTimeout(this.$scoreSubjectsTimeout);
        }
        this.scoringSubjectsError = "";
        // this.analyzingStatusMessage = [];
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
          // setTimeout(() => this.$refs.scorecardScoringEle.scrollIntoView({ behavior: "smooth" }), 150);
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
      // console.log("handleStatusUpdate");
      // console.log(this.scoringSubjects);
      // console.log(data);
      if (this.scoringSubjects) {
        this.analyzingStatusMessage.push(data);
        clearTimeout(this.$scoreSubjectsTimeout);
        this.$scoreSubjectsTimeout = setTimeout(this.showScoreSubjectsError, 995000);
        setTimeout(() => this.$refs.bottom.scrollIntoView({ behavior: "smooth" }), 150);
      }
    },
    showScoreSubjectsError() {
      this.scoringSubjectsError = "";
      this.analyzingStatusMessage = [];
      this.errorScoringSubjects = true;
      this.scoringSubjects = false;
    },
    removeFile(key) {
      delete this.files[key];
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
    async saveFrameworkAndScores() {
      this.savingScorecard = true;
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
          topic: this.report.name,
          topic_context: this.topic_context,
          subjects: this.report.name,
          report_id: this.report.id,
          // scoring_context: this.scoring_context,
          scoring_context: this.topic_context,
          framework: this.strippedFramework,
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
            console.log(ret);

            // Clear the add dialog.
            // this.addScorecardFramework = null;
            this.closeAddScorecard();

            this.emitter.emit("clearSearchBox", {
              previousSelected: this.addScorecardFramework,
            });

            // this.$router.push(`/${ret.target_obj_type}/${ret.target_obj_ox_id}`);
            this.$router.push(`/report/${this.report.id}/#scorecards`);

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
    closeAddScorecard() {
      console.log("closeAddScorecard");
      this.addingScorecard = false;
      document.getElementById("add-scorecard-modal").checked = false;

      // Full reset
      this.emitter.emit("clearSearchBox", {
        previousSelected: this.addScorecardFramework,
      });
      this.addScorecardFramework = null;
      this.addingScorecard = false;
      this.addingOxGPTScorecard = false;
      this.showOxGPTFlow = false;
      this.permissionsModalOpen = false;
      this.downloadModalOpen = false;
      this.expandedPanel = "";
      this.addScorecardFramework = null;
      this.saving = false;
      this.deleting = false;
      this.scoringSubjects = false;
      this.savingScorecard = false;
      this.subjectsScoredByOx = false;

      this.savingScorecard = false;

      this.scoringSubjects = false;
      this.savingScorecard = false;
      this.subjectsScoredByOx = false;

      this.sourceGeneralKnowledge = true;
      this.sourceSearch = false;
      this.sourceNews = false;
      this.sourceCustom = false;
      this.sourceCustomText = false;
      this.sourceCustomDocs = false;
      this.draggingOver = false;
      this.sourceUrls = "";
      this.sourceText = "";
      this.topic_context = "";
      this.scoringSubjectsError = "";
      this.analyzingStatusMessage = [];

      this.totalSize = 0;
      this.totalSizePercent = 0;
      this.files = {};
      this.uploadedFiles = {};
      this.scorecards = {};
    },
  },
};
</script>

<style scoped>
html {
  @apply h-full;
}

body {
  @apply h-full;
}

.star {
  /*  @apply absolute;*/
  top: 0;
}
.stats {
  @apply overflow-x-visible rounded-lg;
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
</style>
