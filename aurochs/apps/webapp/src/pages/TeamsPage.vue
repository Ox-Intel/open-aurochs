<template>
  <DefaultLayout>
    <main class="w-full">
      <article class="prose max-w-none w-full">
        <div class="flex gap-12">
          <div class="basis-1/2" data-cy="orgs">
            <div class="flex">
              <h1 class="grow">My Organizations</h1>
              <!-- <div class="btn btn-outline btn-primary" @click="createOrg" data-cy="create-org">
                <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />Create
                Organization
              </div> -->
            </div>
            <div v-for="(org, idx) in aurochsData.user.organizations" :key="idx" :data-cy="`org-${idx}`">
              <TeamOrgCard :target="org" :is_new="isNewOrg[org.id]" />
            </div>
          </div>
          <div class="basis-1/2" data-cy="teams">
            <div class="flex">
              <h1 class="grow">My Teams</h1>
              <div class="btn btn-outline btn-primary" data-cy="create-team" @click="startCreateTeam">
                <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />Create Team
              </div>
            </div>
            <div v-for="(team, idx) in allTeams" :key="idx">
              <TeamOrgCard :target="team" :is_new="isNewTeam[team.id]" />
            </div>
          </div>
        </div>
      </article>
      <input id="add-team-modal" type="checkbox" class="modal-toggle" />
      <div class="modal">
        <div class="modal-box relative">
          <label for="add-team-modal" class="btn btn-sm btn-circle absolute right-4 top-4">✕</label>
          <h3 class="text-lg font-bold">Add Team</h3>
          <p class="py-4 font-bold">Which organization is this team a part of?</p>
          <OxSearchBox
            data-cy="team-org-search"
            :options="aurochsData.organizations"
            :placeholder="'Search for an organization...'"
            @selected-choice="setAddTeamOrganization"
          />
          <div class="flex justify-end">
            <div
              data-cy="finish-create-team"
              role="button"
              class="mt-4 btn btn-primary"
              :class="{
                'btn-disabled': !newTeamOrgId || addingTeam,
                saving: addingTeam,
              }"
              @click="createTeam()"
            >
              {{ addingTeam ? "Creating..." : "Create team" }}
            </div>
          </div>
        </div>
      </div>
    </main>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "../layouts/DefaultLayout.vue";
import { useAurochsData } from "../stores/aurochs";
import { ref } from "vue";
import OxSearchBox from "../components/common/OxSearchBox.vue";
import TeamOrgCard from "../components/teams/TeamOrgCard.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";

library.add(faGlobe, faUsers, faCheck, faPlus);

export default {
  components: {
    DefaultLayout,
    FontAwesomeIcon,
    TeamOrgCard,
    OxSearchBox,
  },
  setup() {
    const newTeamOrgId = ref(null);
    const addingTeam = ref(false);
    let aurochsData = useAurochsData();

    let isNewTeam = {};
    for (let t in aurochsData.user.teams) {
      isNewTeam[String(aurochsData.user.teams[t].id)] = false;
    }
    let isNewOrg = {};
    for (let o in aurochsData.user.organizations) {
      isNewOrg[String(aurochsData.user.organizations[o].id)] = false;
    }

    return {
      aurochsData,
      newTeamOrgId,
      addingTeam,
      isNewOrg,
      isNewTeam,
    };
  },
  computed: {
    allTeams() {
      // return this.aurochsData.teams;
      let teams = [...this.aurochsData.user.teams];
      teams = teams.sort((a, b) => {
        return b.created_at_ms - a.created_at_ms;
      });
      //   for (let m in this.aurochsData.teams[t]?.organization?.members) {
      //     if (
      //       this.aurochsData.teams[t]?.organization?.members[m].id == this.aurochsData.user.id &&
      //       this.aurochsData.teams[t]?.organization?.members[m].can_manage
      //     ) {
      //       let found = false;
      //       for (let i in this.aurochsData.user.teams) {
      //         if (this.aurochsData.user.teams[i].id == this.aurochsData.teams[t].id) {
      //           found = true;
      //         }
      //       }
      //       if (!found) {
      //         teams.push(this.aurochsData.teams[t]);
      //       }
      //     }
      //   }
      // }
      return teams;
    },
  },
  methods: {
    async startCreateTeam() {
      if (this.aurochsData.user.organizations && this.aurochsData.user.organizations.length == 1) {
        this.newTeamOrgId = this.aurochsData.user.organizations[0].id;
        return this.createTeam();
      } else {
        // Show org picking dialog.
        document.getElementById("add-team-modal").checked = true;
      }
    },
    async createTeam() {
      this.addingTeam = true;
      const data = {
        blank: true,
        org_id: this.newTeamOrgId,
      };
      let ret_data = await this.$sendEvent("create_team", data);
      for (let t in this.aurochsData.user.teams) {
        this.isNewTeam[String(this.aurochsData.user.teams[t].id)] = false;
      }
      this.isNewTeam[String(ret_data.target_obj_ox_id)] = true;

      this.newTeamOrgId = null;
      this.addingTeam = false;
      this.allTeams;
      document.getElementById("add-team-modal").checked = false;
    },
    async createOrg() {
      const data = {
        blank: true,
      };
      let ret_data = await this.$sendEvent("create_organization", data);
      this.isNewOrg[String(ret_data.target_obj_ox_id)] = true;
    },
    setAddTeamOrganization(org) {
      if (org) {
        this.newTeamOrgId = org.id;
      } else {
        this.newTeamOrgId = null;
      }
    },
  },
};
</script>
