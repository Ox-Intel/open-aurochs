<template>
  <DefaultLayout class="">
    <div v-if="!framework || !canSee">
      <div class="w-full min-h-[75vh]">
        <div class="card w-full bg-base-200 card-bordered mt-32 mx-auto max-w-screen-md" data-cy="not-found">
          <div v-if="!framework" class="card-body w-full">
            <div class="flex">
              <div class="mt-4 w-12 text-center">
                <OxObjectIcon :type="'framework'" :classes="'h-12 w-12'" :greyscale="true" />
              </div>
              <div class="grow text-left px-4 pt-2">
                <div class="text-2xl w-full font-bold">Framework not found.</div>
                <div class="text-xl text-dark-grey">
                  This framework either doesn't exist, or you don't have permissions to view it.
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
                <div class="text-2xl w-full font-bold">Framework is private.</div>
                <div class="text-xl text-dark-grey">
                  You don't have permissions to view this framework. If you think this is incorrect, please contact an
                  administrator: {{ admin_list }}.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <main v-if="framework && canSee" class="" data-cy="framework">
      <div class="w-full">
        <!-- Main Space -->
        <div class="w-full min-h-[75vh]">
          <div class="w-full">
            <div class="w-full">
              <div class="w-full">
                <article class="prose max-w-none">
                  <div class="flex flex-nowrap mb-4 w-full gap-2 lg:flex-nowrap flex-wrap">
                    <OxObjectIcon
                      v-if="framework && framework?.criteria && framework?.criteria.length"
                      ref="topIcon"
                      :target="framework"
                      :classes="'align-middle mr-2 h-12 w-12 '"
                    />
                    <div class="block grow">
                      <h1 class="py-0 my-0">
                        <div v-if="!editing" data-cy="name" :class="framework?.subtitle ? 'mt-0.5' : 'mt-1'">
                          {{ framework?.name }}
                        </div>
                        <div v-if="editing" class="w-full max-w-[70vw]">
                          <input
                            v-model="formData.name"
                            data-cy="input-framework-name"
                            placeholder="framework Title"
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
                          data-cy="input-framework-subtitle"
                          type="text"
                          placeholder="Framework subtitle..."
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
                        {{ framework?.subtitle }}
                      </p>
                    </div>
                    <template v-if="editing">
                      <button
                        type="button"
                        role="button"
                        data-cy="cancel"
                        class="ml-8 btn btn-outline btn-base-300 hover:btn-error"
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
                        @click="saveFramework"
                      >
                        <FontAwesomeIcon v-if="!saving" :icon="['fad', 'check']" class="mr-2 w-4 h-4 align-middle" />
                        <FontAwesomeIcon
                          v-if="saving"
                          :icon="['fad', 'rotate']"
                          class="mr-2 w-4 h-4 align-middle fa-spin"
                        />
                        {{ saving ? "Saving..." : "Save" }}
                      </button>
                    </template>

                    <template v-if="!editing">
                      <button
                        v-if="!editing && canEdit"
                        type="button"
                        data-cy="edit"
                        title="Edit Framework"
                        role="button"
                        class="btn btn-outline btn-primary"
                        @click="editing = true"
                      >
                        <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2 align-middle" />
                        Edit
                      </button>
                      <button
                        data-cy="clone-framework"
                        type="button"
                        title="Clone Framework"
                        role="button"
                        class="btn btn-outline btn-primary"
                        @click="showCloneFramework = true"
                      >
                        <FontAwesomeIcon :icon="['fad', 'clone']" class="mr-2 align-middle" />
                        Clone
                      </button>
                      <button
                        data-cy="download-csv"
                        type="button"
                        title="Download Framework"
                        role="button"
                        class="btn btn-outline btn-primary"
                        @click="downloadCSV"
                      >
                        <FontAwesomeIcon :icon="['fad', 'file-csv']" class="mr-2 align-middle" />
                        CSV
                      </button>
                      <button
                        v-if="canManage"
                        type="button"
                        data-cy="delete"
                        title="Delete Framework"
                        role="button"
                        class="btn btn-outline btn-error"
                        @click="confirmDeleteFramework"
                      >
                        <FontAwesomeIcon :icon="['fad', 'trash-can']" class="mr-2 align-middle" />
                        Delete
                      </button>
                    </template>
                  </div>

                  <OxTags v-if="!editing" :target="framework" :can-edit="canEdit" />
                </article>
              </div>
            </div>
          </div>
          <div class="mx-auto mt-2 pb-8">
            <TabGroup :selected-index="Number(selectedTab)" @change="changeTab">
              <TabList class="tabs w-full">
                <Tab v-for="tab in tabs" v-slot="{ selected }" :key="tab.name" as="template">
                  <div
                    :data-cy="`tab-${tab.hash}`"
                    class="tab tab-bordered tab-lg focus:outline-none"
                    :class="selected ? 'tab-active' : ''"
                  >
                    <FontAwesomeIcon :icon="tab.icon" :class="tab.class" class="mr-2 align-middle" />
                    <span>{{ tab.name }}</span>
                  </div>
                </Tab>
              </TabList>
              <TabPanels class="mt-8">
                <TabPanel>
                  <div class="relative">
                    <DownloadButton
                      v-if="criterias?.length > 0"
                      class="btn absolute right-0 top-0 btn-ghost btn-border-base-200 removedInExport z-50"
                      @click.stop.prevent="
                        downloadArea($refs.viewCriteria, `${framework.name} - ${selectedCriteria.name}`)
                      "
                    />
                  </div>
                  <div ref="viewCriteria" class="grid grid-cols-12">
                    <div class="col-span-7">
                      <div class="flex flex-row justify-between mr-10 mt-2">
                        <span v-if="showEditCriteria" class="text-base mr-6" />
                        <span v-if="haveOneCriteriaVisible" class="text-base mr-6">Importance (1-10)</span>
                      </div>
                      <div v-if="showEditCriteria">
                        <EditCriteria
                          :criteria-list="criterias"
                          :saving="saving"
                          @update-criteria="updateCriteria"
                          @save-criteria="saveCriteria"
                          @cancel="cancelEditCriteria"
                        />
                      </div>
                      <div v-else class="mr-10">
                        <div v-if="haveOneCriteriaVisible">
                          <ul role="list" class="relative z-0">
                            <li
                              v-for="(criteria, idx) in criterias"
                              :key="criteria.id"
                              class="relative pr-6 py-2 sm:py-2 h-min"
                            >
                              <CriteriaListItem :criteria="criteria" :idx="idx" :thin="false" />
                            </li>
                          </ul>
                          <div v-if="canEdit" class="text-right my-2 mr-5 removedInExport">
                            <button
                              type="button"
                              role="button"
                              class="btn btn-primary"
                              data-cy="edit-criteria"
                              @click="toggleShowEditCriteria"
                            >
                              <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2" />
                              Edit Criteria
                            </button>
                          </div>
                        </div>
                        <div v-else class="card w-full bg-base-200 card-bordered m-8 max-w-screen-lg">
                          <div class="card-body w-full">
                            <div class="flex">
                              <FontAwesomeIcon
                                :icon="['fad', 'chart-simple-horizontal']"
                                class="h-12 w-12 mr-2 align-middle text-medium-grey"
                              />
                              <div class="grow text-left px-4 pt-2 flex justify-between">
                                <div class="text-xl text-medium-grey">No criteria added.</div>
                                <label
                                  for="add-report-modal"
                                  class="btn btn-primary -mt-2 removedInExport"
                                  role="button"
                                  data-cy="add-criteria"
                                  @click="showEditCriteria = true"
                                >
                                  <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
                                  Add Criteria
                                </label>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-span-5" data-cy="framework-chart">
                      <OxChartIcon
                        ref="criteriaChart"
                        :criteria="graphCriterias"
                        :hover="true"
                        class="flex justify-center h-80 w-80 mx-auto"
                      />

                      <div v-if="criterias.length > 0 || showEditCriteria" class="text-md mt-4 text-center">
                        <div v-if="!hoveredChartCriteria" class="italic mb-6 p-2">Relative Importance</div>
                        <div
                          v-if="hoveredChartCriteria"
                          :style="`background-color: ${getCriteriaColor(hoveredChartCriteria.index)}`"
                          class="justify-center text-neutral-content min-w-fit max-w-fit mx-auto rounded-md py-2 px-4"
                        >
                          <div class="font-bold">{{ hoveredChartCriteria.name }}</div>
                          <div>{{ Math.round(hoveredChartCriteria.relative_weight_as_percent) }}%</div>
                        </div>
                      </div>
                      <StatsBox v-if="criterias.length > 0" :framework="framework" />
                    </div>
                  </div>
                </TabPanel>
                <TabPanel>
                  <!-- Explorer -->
                  <div class="container mx-auto">
                    <article class="prose max-w-none relative pt-8 pb-12">
                      <div class="btn-group flex-wrap">
                        <div
                          v-for="(criteria, idx) in framework?.criteria"
                          :key="criteria.id"
                          class="btn btn-outline bg-base-100 hover:bg-base-300 hover:text-neutral relative"
                          :class="selectedCriteria && selectedCriteria.id == criteria.id ? 'btn-active' : ''"
                          :style="`${
                            selectedCriteria && selectedCriteria.id == criteria.id ? 'background-color' : 'nothing'
                          }: ${getCriteriaColor(criteria.index)}`"
                          :data-cy="`explore-criteria-${idx}`"
                          @click="exploreCriteria(criteria, idx)"
                        >
                          <div
                            class="w-full h-1 absolute left-0 bottom-0"
                            :style="{
                              'background-color': getCriteriaColor(criteria.index),
                            }"
                          />
                          {{ criteria.name }}
                        </div>
                      </div>

                      <div v-if="selectedCriteria" ref="explorer" class="pb-8">
                        <DownloadButton
                          class="btn btn-ghost btn-border-base-200 removedInExport absolute right-0"
                          @click.stop.prevent="
                            downloadArea($refs.explorer, `${framework.name} - ${selectedCriteria.name}`)
                          "
                        />
                        <h1 class="mb-0 mt-8" data-cy="criteria-name">
                          {{ selectedCriteria.name }}
                        </h1>
                        <p class="mt-0 text-linebreaks" data-cy="criteria-description">
                          {{ selectedCriteria.description }}
                        </p>
                        <div class="rounded-lg w-full bg-base-100 card-bordered shadow-md my-8">
                          <div class="card-body p-0">
                            <div class="flex flex-row" data-cy="report-all">
                              <div class="w-1/3 text-base-content text-left relative">
                                <div
                                  class="left-bar rounded-tl-lg rounded-bl-lg"
                                  :style="{
                                    'background-color': getCriteriaColor(selectedCriteriaColorIndex),
                                  }"
                                />
                                <div class="align-middle items-center h-full flex">
                                  <div class="flex">
                                    <OxObjectIcon :type="'report'" :classes="'mt-8 ml-8 mr-4 w-12 h-12 align-middle'" />
                                    <div class="grow pr-4">
                                      <div class="text-xl font-bold pt-8 inline-block">All Reports</div>
                                      <!-- <p class="ml-8">{{ obj.report.subtitle }}</p> -->
                                      <div class="mb-4">{{ criteriaReports.length }} reports use this framework.</div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <div class="w-1/2 align-middle py-4 px-2">
                                <!-- <div class="left-bar" :style="{'background-color': 'grey'}"></div> -->
                                <DotPlot
                                  :report="{ name: 'All Reports' }"
                                  :group-by-report="true"
                                  :scores_by_criteria="allScores"
                                  :color="getCriteriaColor(selectedCriteriaColorIndex)"
                                  :idx="-1"
                                />
                              </div>
                              <div class="w-1/6">
                                <div class="pl-6 h-full flex align-middle">
                                  <div class="flex items-center">
                                    <div class="badge mt-1 mr-2" :class="getNoiseBadgeClass(allScores)">
                                      <FontAwesomeIcon
                                        v-if="allScores.stddev > 2.25"
                                        :icon="['fad', 'triangle-exclamation']"
                                        class="h-4 w-4 mr-2 align-middle inline"
                                      />

                                      {{ getNoiseText(allScores) }}
                                    </div>
                                    <div
                                      v-if="allScores.stddev > 2.25"
                                      class="tooltip z-50 inline-block text-linebreaks text-left float-right mr-4"
                                      :data-tip="`${allScores.criteria.name} appears to result in noisy judgments${
                                        allScores.criteria.weight >= 3 ? ' and has significant importance' : ''
                                      }.\n\nTo reduce scoring noise, Ox suggests collecting more information on how users make this judgment${
                                        allScores.criteria.weight >= 3
                                          ? ' or reducing the importance of this criterion in the framework'
                                          : ''
                                      }.`"
                                    >
                                      <div
                                        class="bg-ox-score text-ox-score-content rounded-2xl rounded-circle align-middle w-8 h-8 pt-1"
                                      >
                                        <OxHorns class="block h-6 w-6 mt-2 ml-1" />
                                      </div>
                                    </div>
                                    <div
                                      v-if="allScores.stddev < 1.2 && allScores.criteria.weight < 4"
                                      class="tooltip z-50 inline-block text-linebreaks text-left float-right mr-4"
                                      :data-tip="`${allScores.criteria.name} appears to have a low level of scoring noise, without high importance.\n\nOx recommends reviewing the importance of this criterion in the framework.`"
                                    >
                                      <div
                                        class="bg-ox-score text-ox-score-content rounded-2xl rounded-circle align-middle w-8 h-8 pt-1"
                                      >
                                        <OxHorns class="block h-6 w-6 mt-2 ml-1" />
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div class="rounded-lg w-full bg-base-200 card-bordered my-8 mr-24 shadow-inner table">
                          <div
                            v-for="(obj, idx) in criteriaReports"
                            :key="idx"
                            :data-cy="`report-${idx}`"
                            class="table-row card-body w-full p-0 border-base-300 border-b"
                            :class="idx % 2 ? 'bg-base-300' : ''"
                          >
                            <router-link
                              :to="`/report/${obj.report.id}`"
                              class="table-cell align-middle w-1/3 h-full no-underline"
                            >
                              <div class="h-full text-left relative" role="button">
                                <div
                                  class="left-bar h-full"
                                  :style="{
                                    'background-color': getCriteriaColor(selectedCriteriaColorIndex),
                                  }"
                                ></div>
                                <div class="align-middle content-center h-full pb-2">
                                  <div class="flex">
                                    <OxObjectIcon :type="'report'" :classes="'mt-8 ml-8 mr-4 w-12 h-12 align-middle'" />
                                    <div class="grow pr-4">
                                      <div class="text-xl font-bold pt-8 inline-block" data-cy="report-name">
                                        {{ obj.report.name }}
                                      </div>
                                      <!-- <p class="ml-8">{{ obj.report.subtitle }}</p> -->
                                      <div class="mb-4">
                                        Updated
                                        {{ formatDate(obj.report.modified_at_ms) }}
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </router-link>
                            <template v-if="obj?.scores.length > 0">
                              <div class="align-middle w-1/2 py-4 px-2 table-cell align-middle">
                                <DotPlot
                                  :report="obj.report"
                                  :scores_by_criteria="obj"
                                  :color="getCriteriaColor(selectedCriteriaColorIndex)"
                                  :idx="idx"
                                />
                              </div>
                            </template>
                            <template v-if="obj?.scores.length == 0">
                              <div class="w-1/2 table-cell align-middle">
                                <div class="pl-4 h-full flex align-middle">
                                  <div class="flex items-center w-full">
                                    <div class="w-full text-center text-medium-grey">No scores yet.</div>
                                  </div>
                                </div>
                              </div>
                            </template>
                            <div class="w-1/6 table-cell align-middle">
                              <div class="pl-6 h-full flex align-middle">
                                <div class="flex items-center">
                                  <div class="badge mt-1 mr-2" :class="getNoiseBadgeClass(obj)">
                                    <FontAwesomeIcon
                                      v-if="obj.stddev > 2.25"
                                      :icon="['fad', 'triangle-exclamation']"
                                      class="h-4 w-4 mr-2 align-middle inline"
                                    />

                                    {{ getNoiseText(obj) }}
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div
                        v-if="!selectedCriteria"
                        class="bg-base-100 rounded text-lg p-12 mt-12 border-2 border-grey w-96"
                      >
                        Select a criteria to explore.
                      </div>
                    </article>
                  </div>
                </TabPanel>
                <TabPanel>
                  <div class="" data-cy="report-list">
                    <div class="mt-8 max-w-screen-xl grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-10 w-full">
                      <template v-for="(r, idx) in reports" :key="idx">
                        <OxObjectCard :object="r" :index="key" class="border-base-300" />
                      </template>
                      <div
                        class="h-48 card shadow-md bg-base-300 cursor-pointer border-base-300 hover:border-report text-medium-grey hover:text-report border-2"
                        data-cy="new-report"
                        @click="createBlankReport"
                      >
                        <div class="card-body p-4 text-center place-content-center place-items-center">
                          <FontAwesomeIcon :icon="['fad', 'plus']" class="h-12 w-12" />
                          <div class="mt-2 text-2xl font-bold">New Report</div>
                        </div>
                      </div>
                    </div>
                    <!-- <div v-for="(r, idx) in reports" :key="idx">
                      <div
                        :data-cy="`report-${idx}`"
                        class="card w-full bg-base-100 card-bordered shadow-md m-8"
                        role="button"
                        @click="openReport(r)"
                      >
                        <div class="card-body w-full">
                          <div class="flex">
                            <div class="w-12 text-center">
                              <OxObjectIcon :type="'report'" :classes="'h-12 w-12 mr-2 align-middle'" />
                            </div>
                            <div class="grow text-left px-4">
                              <div class="text-xl font-bold" data-cy="report-name">
                                {{ r.name }}
                              </div>
                              <div class="text-linebreaks">
                                {{ r.subtitle }}
                              </div>
                              <div class="font-light mt-4">Updated {{ formatDate(r.modified_at_ms) }}</div>
                              <div
                                v-for="(s_id, s_idx) in r.stack_ids"
                                :key="s_idx"
                                class="badge badge-lg badge-outline border-stack border-opacity-50 rounded-md hover:bg-base-200 hover:bg-stack hover:bg-opacity-5 hover:border-opacity-100 gap-1 mt-2 text-sm select-none overflow-hidden whitespace-nowrap"
                                @click.stop.prevent="openStack(s_id)"
                              >
                                <OxObjectIcon :type="'stack'" :classes="'h-4 w-4 mr-2 align-middle'" />
                                {{ getStack(s_id).name }}
                              </div>
                            </div>
                            <div class="w-12">
                              <OxScoreBox :ox-score="Number(r.ox_score)" :has-skipped="r.has_skipped"/>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div> -->
                  </div>
                </TabPanel>
                <TabPanel>
                  <NotesPanel :target="framework" />
                </TabPanel>
                <TabPanel>
                  <DiscussionPanel :target="framework" />
                </TabPanel>
                <TabPanel>
                  <PermissionsPanel
                    :target="framework"
                    :can-manage="canManage"
                    @permissions-updated="permissionsUpdated"
                  />
                </TabPanel>
              </TabPanels>
            </TabGroup>
          </div>
        </div>
      </div>
      <ConfirmDelete
        :open="showConfirmDelete"
        :message="confirmDeleteMsg"
        @close="closeConfirmDelete"
        @confirm="deleteFramework"
      />
      <OxModalLayout :open="showEditFramework">
        <EditFramework :framework="framework" @close="closeEditFramework" @save="saveFramework" />
      </OxModalLayout>
      <OxModalLayout :open="showCloneFramework">
        <EditFramework :framework="framework" :is-clone="true" @close="closeCloneFramework" @save="cloneFramework" />
      </OxModalLayout>
    </main>
    <OxOwnerFooter :object="framework" />
  </DefaultLayout>
</template>

<script>
/**
 * TODO: Replace hardcoded  links
 *
 */
import "regenerator-runtime/runtime";
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
import { faMemoPad } from "@fortawesome/pro-duotone-svg-icons/faMemoPad";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";
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
  faMemoPad,
  faTriangleExclamation
);

import { TabGroup, TabList, Tab, TabPanels, TabPanel } from "@headlessui/vue";
import { ref } from "vue";
// import { getCriteriaColor } from "../mixins/criteria_color";
import OxObjectIcon from "../components/common/icons/OxObjectIcon.vue";
import OxHorns from "../components/logo/OxHorns.vue";
import OxObjectCard from "../components/common/OxObjectCard";
import OxChartIcon from "../components/common/icons/OxChartIcon.vue";
import StatsBox from "../components/framework/StatsBox.vue";
import CriteriaListItem from "../components/framework/CriteriaListItem.vue";
import OxTags from "../components/common/OxTags.vue";
import OxOwnerFooter from "../components/common/OxOwnerFooter.vue";
// import OxScoreBox from "../components/common/OxScoreBox.vue";
import { useAurochsData } from "../stores/aurochs";
import { standardDeviation } from "../mixins/stats.js";
import { checkCanEdit, checkCanManage, checkCanSee } from "../mixins/permissions.js";
import DownloadMixins from "../mixins/download_file";
import ConfirmDelete from "../components/common/ConfirmDelete";
import EditFramework from "../components/framework/EditFramework.vue";
import EditCriteria from "../components/framework/EditCriteria.vue";
import OxModalLayout from "../components/common/OxModalLayout.vue";
import PermissionsPanel from "../components/common/PermissionsPanel.vue";
import formatDate from "../mixins/format_date";
import DotPlot from "../components/reports/charts/DotPlot.vue";
import DiscussionPanel from "../components/common/DiscussionPanel.vue";
import NotesPanel from "../components/common/NotesPanel.vue";
import DownloadButton from "../components/common/DownloadButton.vue";
import downloadArea from "../mixins/download_area";

export default {
  components: {
    DefaultLayout,
    OxChartIcon,
    StatsBox,
    CriteriaListItem,
    ConfirmDelete,
    EditFramework,
    EditCriteria,
    OxModalLayout,
    TabGroup,
    TabList,
    Tab,
    TabPanels,
    TabPanel,
    DotPlot,
    OxHorns,
    DiscussionPanel,
    NotesPanel,
    PermissionsPanel,
    OxTags,
    OxOwnerFooter,
    // OxScoreBox,
    OxObjectCard,
    FontAwesomeIcon,
    OxObjectIcon,
    DownloadButton,
  },
  mixins: [DownloadMixins, formatDate, downloadArea],
  props: {
    id: {
      type: String,
      required: true,
    },
    new: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const showCreateModal = ref(false);
    const permissionsModalOpen = ref(false);
    const expanded = ref(false);
    const showConfirmDelete = ref(false);
    const showEditFramework = ref(false);
    const showEditCriteria = ref(false);
    const showCloneFramework = ref(false);
    const is_new = ref(props.new);
    const frameworkId = ref(props.id);
    const editing = ref(props.new);
    const saving = ref(false);
    const expandedPanel = ref("");
    const tabs = [
      {
        name: "Criteria",
        hash: "criteria",
        class: "mr-2",
        icon: ["fad", "chart-simple-horizontal"],
      },
      {
        name: "Explorer",
        hash: "explorer",
        class: "mr-2",
        icon: ["fad", "compass"],
      },
      {
        name: "Reports",
        hash: "reports",
        class: "mr-2",
        icon: ["fad", "file-lines"],
      },
      {
        name: "Notes",
        hash: "notes",
        classes: "mr-2",
        // icon: ["fad", "memo"],
        // icon: ["fad", "note"],
        // icon: ["fad", "notes"],
        icon: ["fad", "memo-pad"],
      },
      {
        name: "Discussion",
        hash: "discussion",
        class: "mr-2",
        icon: ["fad", "messages"],
      }, // badge: 2
      {
        name: "Permissions",
        hash: "permissions",
        classes: "mr-2",
        icon: ["fad", "lock"],
      },
    ];
    const selectedCriteria = ref(false);
    const selectedCriteriaColorIndex = ref(0);
    const criteriaReports = ref([]);
    const allScores = ref({});
    const selectedTab = ref(0);
    const formData = ref({});

    return {
      tabs,
      aurochsData: useAurochsData(),
      expanded,
      showCreateModal,
      permissionsModalOpen,
      showConfirmDelete,
      showEditFramework,
      showEditCriteria,
      showCloneFramework,
      expandedPanel,
      graphCriteriaCopy: ref([]),
      selectedCriteria,
      criteriaReports,
      selectedCriteriaColorIndex,
      allScores,
      editing,
      saving,
      frameworkId,
      is_new,
      selectedTab,
      hoveredChartCriteria: ref(null),

      formData: ref(formData),
    };
  },
  computed: {
    framework() {
      if (this.aurochsData.frameworks && this.id && String(this.id)) {
        return this.aurochsData.frameworks[String(this.id)];
      }
      return null;
    },
    canEdit() {
      return checkCanEdit(this.framework, this.aurochsData.user);
    },
    canManage() {
      return checkCanManage(this.framework, this.aurochsData.user);
    },
    canSee() {
      return checkCanSee(this.framework, this.aurochsData.user);
    },
    admin_list() {
      let admin_str = "";
      if (this.framework) {
        for (let p_id in this.framework.permissions) {
          if (this.framework.permissions[p_id].substring(3, 4) == "1") {
            admin_str += this.aurochsData.users[p_id.substring(2)].full_name + ", ";
          }
        }
        if (admin_str.length > 2) {
          admin_str = admin_str.slice(0, -2);
        }
      }
      return admin_str;
    },
    criterias() {
      if (this.framework?.criteria) {
        let criteria_list = [];
        for (let c in this.framework.criteria) {
          let slim_criteria = {};
          for (let k in this.framework.criteria[c]) {
            if (k != "created_by") {
              slim_criteria[k] = this.framework.criteria[c][k];
            }
          }
          criteria_list.push(slim_criteria);
        }
        return criteria_list;
      }
      return [];
    },
    graphCriterias() {
      return this.graphCriteriaCopy;
    },
    confirmDeleteMsg() {
      return `Are you sure you want to delete the framework ${this.framework?.name}?`;
    },
    sortedCriteria() {
      let criterias = [...this.criterias];
      return criterias.sort((a, b) => {
        return b.relative_weight_as_percent - a.relative_weight_as_percent;
      });
    },
    createdBy() {
      if (this.framework) {
        return this.framework?.created_by;
      }
      return null;
    },
    reports() {
      var report_list = [];
      for (var i of this.framework.report_id_list) {
        report_list.push(this.aurochsData.reports[i]);
      }
      return report_list.sort((a, b) => {
        return b.modified_at_ms - a.modified_at_ms;
      });
    },
    haveOneCriteriaVisible() {
      return (
        (this.showEditCriteria && this.graphCriteriaCopy?.length > 0) ||
        (!this.showEditCriteria && this.criterias.length > 0)
      );
    },
  },
  watch: {
    id: {
      handler: function (newVal) {
        // this.id = Number(newVal);
        document.title = this.aurochsData.frameworks[String(newVal)].name;
        this.graphCriteriaCopy = this.criterias;
        this.selectedCriteria = false;
        this.is_new = this.$route.query.new == "true";
        this.editing = this.$route.query.new == "true";
        this.showEditCriteria = false;
        this.formData = {
          name: this.framework?.name || "",
          subtitle: this.framework?.subtitle || "",
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
    $route: {
      deep: true,
      handler: function (newVal) {
        if (newVal.hash) {
          for (var t in this.tabs) {
            if (this.tabs[t].hash == newVal.hash.substring(1)) {
              this.selectedTab = t;
              break;
            }
          }
        } else {
          this.selectedTab = 0;
        }
      },
    },
  },
  mounted() {
    this.formData = {
      name: this.framework?.name || "",
      subtitle: this.framework?.subtitle || "",
    };
    document.title = this.framework?.name || "Ox Framework";
    if (this.$route.hash) {
      for (var t in this.tabs) {
        if (this.tabs[t].hash == this.$route.hash.substring(1)) {
          this.selectedTab = t;
          break;
        }
      }
    } else {
      this.selectedTab = 0;
    }
    this.emitter.on("hovered-criteria", (e) => {
      this.hoveredChartCriteria = e.criteria;
    });
  },
  created() {
    this.graphCriteriaCopy = this.criterias;
  },
  methods: {
    async saveCriteria(criterias) {
      this.saving = true;
      let data = { id: this.id, criteria: [] };
      for (let c in criterias.criterias) {
        data["criteria"].push({
          id: criterias.criterias[c].id,
          name: criterias.criterias[c].name,
          description: criterias.criterias[c].description,
          weight: criterias.criterias[c].weight,
        });
      }
      await this.$sendEvent("update_framework", data);
      this.saving = false;
      this.showEditCriteria = false;
    },
    async saveFramework() {
      this.saving = true;
      await this.$sendEvent(
        "update_framework",
        {
          id: this.framework.id,
          name: this.formData.name,
          subtitle: this.formData.subtitle,
        },
        this.aurochsData
      );
      this.showEditFramework = false;
      this.saving = false;
      this.editing = false;
      if (this.is_new) {
        this.$router.push(`/framework/${this.framework.id}`);
      }
      this.is_new = false;
    },
    confirmDeleteFramework() {
      if (window.confirm("Are you sure you want to delete this framework?")) {
        this.deleteFramework();
      }
      // this.showConfirmDelete = true;
    },
    closeConfirmDelete() {
      this.showConfirmDelete = false;
    },
    closeEditFramework() {
      this.showEditFramework = false;
    },
    closeCloneFramework() {
      this.showCloneFramework = false;
    },
    async deleteFramework() {
      this.showConfirmDelete = false;
      var data = {
        id: this.id,
      };
      await this.$sendEvent("delete_framework", data);
      this.$router.push("/library");
    },
    async cloneFramework(framework) {
      this.showCloneFramework = false;
      let data = {
        id: this.id,
        name: framework?.name || "",
        subtitle: framework?.subtitle || "",
      };
      let ret_data = await this.$sendEvent("clone_framework", data);
      if (ret_data.success) {
        this.$router.push(`/framework/${ret_data.obj_pk}`);
      } else {
        alert(`Error in save: ${ret_data.error_message}`);
      }
    },
    downloadCSV() {
      var now = new Date();
      this.downloadFile(
        "/export/framework/csv/" + this.id,
        this.framework?.name.replace(" ", "_").replace('"', "'") + "-" + now.toISOString(),
        ".csv"
      );
    },
    toggleShowEditCriteria() {
      this.showEditCriteria = !this.showEditCriteria;
    },
    updateCriteria(criterias) {
      this.graphCriteriaCopy = [...criterias];
      this.$refs.criteriaChart.updateCriteria(criterias);
      if (this.$refs?.topIcon) {
        this.$refs.topIcon.updateCriteria(criterias);
      }
    },
    cancelEditCriteria(criterias) {
      this.showEditCriteria = false;
      this.graphCriteriaCopy = criterias;
    },
    expandReports() {
      if (this.expandedPanel === "reports") {
        this.expanded = false;
        this.expandedPanel = "";
      } else {
        this.expanded = true;
        this.expandedPanel = "reports";
      }
    },
    expandDiscuss() {
      if (this.expandedPanel === "discuss") {
        this.expanded = false;
        this.expandedPanel = "";
      } else {
        this.expanded = true;
        this.expandedPanel = "discuss";
      }
    },
    getCriteriaColor(idx) {
      const remainder = idx % 40;
      return `var(--criteria-color-${remainder + 1})`;
    },
    exploreCriteria(criteria, criteriaColorIndex) {
      this.selectedCriteria = criteria;
      this.selectedCriteriaColorIndex = criteriaColorIndex;
      this.criteriaReports = [];
      var my_scores = [];
      var my_total_scores = 0;
      this.allScores = {
        criteria: criteria,
        average_score: criteria.average_score,
        scores: [],
      };
      let sc;
      let report_ids = [];
      for (var r_index in this.aurochsData.reports) {
        let r = this.aurochsData.reports[r_index];
        for (sc of r.scorecards) {
          if (sc.framework.id == this.selectedCriteria.framework_pk && report_ids.indexOf(r.id) == -1) {
            report_ids.push(r.id);
            this.criteriaReports.push({ report: r });
          }
        }
      }
      var allStdDevs = [];
      for (var i in this.criteriaReports) {
        var d = this.criteriaReports[i];
        var scores = [];
        var scoreValues = [];
        var total_score = 0;

        for (sc of d.report.scorecards) {
          for (var sc_index in sc.scores) {
            var scs = sc.scores[sc_index];
            if (scs.criteria.id == criteria.id) {
              scs.report = d.report;
              scores.push(scs);
              if (scs.score != null) {
                scoreValues.push(Number(scs.score));
                total_score += Number(scs.score);
                if (sc.scorer.id == this.aurochsData.user.id) {
                  my_scores.push(scs);
                  my_total_scores += Number(scs.score);
                }
              }
            }
          }
        }
        this.criteriaReports[i].criteria = criteria;
        this.criteriaReports[i].scores = scores;
        this.criteriaReports[i].scoreValues = scoreValues;
        if (scoreValues.length > 0) {
          this.criteriaReports[i].average_score = total_score / scoreValues.length;
          this.allScores["scores"].push({
            score: this.criteriaReports[i].average_score,
            scorer: {
              full_name: this.criteriaReports[i].report.name,
              initials: this.criteriaReports[i].report.name.slice(0, 2),
            },
          });
        }

        if (scoreValues.length > 1) {
          this.criteriaReports[i].stddev = standardDeviation(scoreValues);
          allStdDevs.push(Number(this.criteriaReports[i].stddev));
        }
      }
      // console.log(allStdDevs);
      if (allStdDevs.length > 0) {
        this.allScores.stddev = allStdDevs.reduce((a, b) => a + b) / allStdDevs.length;
      }
      // console.log(this.allScores.stddev);

      if (my_scores.length > 0) {
        this.allScores["scores"].push({
          score: my_total_scores / my_scores.length,
          scorer: {
            full_name: "My Average Score",
            initials: this.aurochsData.user.initials.slice(0, 1),
          },
          average: true,
        });
      }
    },
    getNoiseBadgeClass(obj) {
      if (obj.stddev < 1.2) {
        return "bg-base-200 border-0 text-neutral";
      } else if (obj.stddev > 2.25) {
        return "badge-error text-primary-content";
      }
      if (obj.stddev) {
        return "bg-base-200  border-0  text-neutral";
      } else {
        return "hidden";
      }
    },
    getNoiseText(score) {
      if (score.stddev < 1.2) {
        return "Low Noise";
      } else if (score.stddev > 2.25) {
        return "High Noise";
      }
      if (score.stddev) {
        return "Medium Noise";
      } else {
        return "";
      }
    },
    getStack(s_id) {
      return this.aurochsData.stacks[s_id];
    },
    permissionsUpdated() {},
    startEditing() {
      this.editing = true;
    },
    stopEditing() {
      this.editing = false;
    },
    cancel() {
      this.formData = {
        name: this.framework?.name || "",
        subtitle: this.framework?.subtitle || "",
      };
      this.editing = false;
    },
    changeTab(tab) {
      this.$router.push(`/framework/${this.framework.id}/#${this.tabs[tab].hash}`);
    },
    async createBlankReport() {
      let ret_data = await this.$sendEvent("create_report", {
        name: "New Report",
      });
      this.$router.push({
        path: `/report/${ret_data.obj_pk}`,
        query: { new: true },
      });
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
.left-bar {
  @apply h-full w-4 absolute;
}

.ox-framework-nav {
  @apply inline-flex items-center px-3 py-2 border border-transparent hover:shadow-sm text-lg leading-4  focus:outline-none;
}

.framework-action-icon {
  @apply h-4 w-4 mr-1;
}

.reports-btn {
  @apply text-white bg-sky-600 hover:bg-sky-700;
}

.discussion-btn {
  @apply text-white bg-indigo-600 hover:bg-indigo-700;
}
</style>
