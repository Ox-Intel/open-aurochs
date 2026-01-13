<template>
  <input id="permissions-modal" type="checkbox" class="modal-toggle" />
  <div class="modal" data-cy="permissions">
    <div class="modal-box max-w-screen-sm p-10" :class="addMenuOpen ? ' ' : ''">
      <div class="relative">
        <label for="permissions-modal" class="btn btn-sm btn-circle absolute right-0 top-0" data-cy="close-permissions">
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle fa-swap-opacity" />
        </label>
      </div>
      <template v-if="canManage">
        <h3 class="text-2xl font-bold">
          <FontAwesomeIcon :icon="['fad', 'unlock']" class="mr-2 align-middle" />
          Set Permissions
        </h3>
        <p class="py-4">Which users, teams, and organizations should have access?</p>
        <table class="w-full">
          <tr>
            <th class="text-left">Role</th>
            <th v-if="target_obj?.__type == 'report'" class="permission_caption w-16">Score</th>
            <th class="permission_caption w-16">View</th>
            <th class="permission_caption w-16">Edit</th>
            <th class="permission_caption w-16">Admin</th>
            <th class="w-16" />
          </tr>
          <tr v-for="(p, idx) in newPermissions" :key="idx" :data-cy="`role-${slugify(p.role_name)}`">
            <td class="text-left">
              <FontAwesomeIcon v-if="p.type == 'user'" :icon="['fad', 'user']" class="mr-1 align-middle h-6 w-6" />
              <FontAwesomeIcon v-if="p.type == 'team'" :icon="['fad', 'users']" class="mr-1 align-middle h-6 w-6" />
              <FontAwesomeIcon
                v-if="p.type == 'organization'"
                :icon="['fad', 'globe']"
                class="mr-1 align-middle h-6 w-6"
              />
              {{ p.role_name }}
            </td>
            <!--             
            <td colspan="4" class="pr-8">
              <input
                class="range range-md range-primary ox-slider ox-slidery ml-4 "
                type="range"
                :value="getPermissionNumber(p)"
                min="1"
                max="4"
                step="1"
              />
            </td> -->

            <td v-if="target_obj?.__type == 'report'" class="text-center">
              <button
                data-cy="can-score"
                class="btn btn-square btn-sm text-success-content"
                :class="
                  p.score || p.write || p.administer
                    ? ' btn-success '
                    : ' btn-outline bg-base-300 border-base-300 btn-outline bg-base-300 border-base-300 '
                "
                role="button"
                @click="togglePermission(p, 'score')"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
              </button>
            </td>
            <td class="text-center">
              <button
                data-cy="can-read"
                class="btn btn-square btn-sm text-success-content"
                :class="
                  p.read || p.write || p.administer
                    ? ' btn-success '
                    : ' btn-outline bg-base-300 border-base-300 btn-outline bg-base-300 border-base-300 '
                "
                role="button"
                @click="togglePermission(p, 'read')"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
              </button>
            </td>
            <td class="text-center">
              <button
                data-cy="can-write"
                class="btn btn-square btn-sm text-success-content"
                :class="
                  p.write || p.administer
                    ? ' btn-success '
                    : ' btn-outline bg-base-300 border-base-300 btn-outline bg-base-300 border-base-300 '
                "
                role="button"
                @click="togglePermission(p, 'write')"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
              </button>
            </td>
            <td class="text-center">
              <button
                data-cy="can-admin"
                class="btn btn-square btn-sm text-success-content"
                :class="
                  p.administer
                    ? ' btn-success '
                    : ' btn-outline bg-base-300 border-base-300 btn-outline bg-base-300 border-base-300 '
                "
                role="button"
                @click="togglePermission(p, 'administer')"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
              </button>
            </td>

            <td class="text-center">
              <button
                data-cy="remove-role"
                class="btn btn-sm btn-circle btn-ghost hover:btn-error"
                @click="removePermission(p)"
              >
                <FontAwesomeIcon :icon="['fad', 'trash-can']" class="h-4 w-4" />
              </button>
            </td>
          </tr>
        </table>
        <div class="relative">
          <div v-if="addMenuOpen" class="mt-4 max-h-60">
            <div class="flex">
              <input
                v-model="searchText"
                data-cy="search-roles"
                type="text"
                placeholder="Search for a user, team, or organization..."
                class="input input-bordered w-full"
                autofocus
                @input="updatePossibleRoles"
              />
              <div class="align-middle text-center w-12 h-12 pt-1 hover:text-error" role="button" @click="cancelAdd">
                <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-8 w-8" />
              </div>
            </div>
            <ul
              class="menu bg-base-200 min-w-max max-w-96 pl-0 mr-12 max-h-48 overflow-hidden"
              data-cy="potential-roles"
            >
              <template v-for="(r, idx) in possibleRoles" :key="idx">
                <li
                  v-if="shouldBeVisible(r)"
                  data-cy="role"
                  role="button"
                  class="hover:bg-base-300 box-rounded rounded-md mb-0 w-full"
                  @click="addRole(r)"
                >
                  <div class="p-2 align-middle">
                    <FontAwesomeIcon v-if="r.type == 'user'" :icon="['fad', 'user']" class="mr-1 h-4 w-4" />
                    <FontAwesomeIcon v-if="r.type == 'team'" :icon="['fad', 'users']" class="mr-1 h-4 w-4" />
                    <FontAwesomeIcon v-if="r.type == 'organization'" :icon="['fad', 'globe']" class="mr-1 h-4 w-4" />
                    {{ r.role_name }}
                  </div>
                </li>
              </template>
            </ul>
          </div>
        </div>
        <button
          v-if="!addMenuOpen"
          data-cy="add-another"
          class="btn btn-primary mt-4"
          role="button"
          @click="addAnother"
        >
          <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
          Add Another
        </button>
        <div v-if="!haveValidPermissions" class="alert alert-error alert-outline my-4">
          <p>
            <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="" />
            {{ invalidPermissionsMessage }}
          </p>
        </div>
        <div v-if="haveWarningMessage && haveValidPermissions" class="alert alert-warning alert-outline my-4">
          <p>
            <FontAwesomeIcon :icon="['fad', 'circle-info']" class="" />
            {{ permissionsWarningMessage }}
          </p>
        </div>
        <div class="flex flex-row justify-end mx-5 mt-6">
          <button type="button" role="button" class="btn btn-outline btn-base-300 hover:btn-error mr-2" @click="cancel">
            <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2" />
            Cancel
          </button>
          <button
            data-cy="save-permissions"
            type="button"
            role="button"
            class="btn btn-success"
            :class="{ saving: saving }"
            :disabled="saving || !haveValidPermissions"
            @click="savePermissions"
          >
            <FontAwesomeIcon :icon="['fad', 'check']" class="mr-2" />
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </template>
      <template v-if="!canManage">
        <h3 class="text-2xl font-bold">
          <FontAwesomeIcon :icon="['fad', 'unlock']" class="mr-2 align-middle" />
          Permissions
        </h3>
        <p class="py-4">
          Which users, teams, and organizations have access to this
          {{ target.__type }}?
        </p>
        <table class="w-full my-4" data-cy="read-only-permissions">
          <tr>
            <th class="pb-2 text-left">Role</th>
            <th v-if="target_obj?.__type == 'report'" class="permission_caption w-16">Score</th>
            <th class="pb-2 w-16 permission_caption">View</th>
            <th class="pb-2 w-16 permission_caption">Edit</th>
            <th class="pb-2 w-16 permission_caption">Admin</th>
          </tr>
          <tr v-for="(p, idx) in newPermissions" :key="idx">
            <td class="text-left">
              <FontAwesomeIcon v-if="p.type == 'user'" :icon="['fad', 'user']" class="mr-1 align-middle h-6 w-6" />
              <FontAwesomeIcon v-if="p.type == 'team'" :icon="['fad', 'users']" class="mr-1 align-middle h-6 w-6" />
              <FontAwesomeIcon
                v-if="p.type == 'organization'"
                :icon="['fad', 'globe']"
                class="mr-1 align-middle h-6 w-6"
              />
              {{ p.role_name }}
            </td>
            <td v-if="target_obj?.__type == 'report'" class="text-center">
              <FontAwesomeIcon v-if="p.score" :icon="['fad', 'check']" class="h-4 w-4" />
            </td>
            <td class="text-center">
              <FontAwesomeIcon v-if="p.read" :icon="['fad', 'check']" class="h-4 w-4" />
            </td>
            <td class="text-center">
              <FontAwesomeIcon v-if="p.write" :icon="['fad', 'check']" class="h-4 w-4" />
            </td>
            <td class="text-center">
              <FontAwesomeIcon v-if="p.administer" :icon="['fad', 'check']" class="h-4 w-4" />
            </td>
          </tr>
        </table>
      </template>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import { ref } from "vue";

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
import { faDownload } from "@fortawesome/pro-duotone-svg-icons/faDownload";
import { faTriangleExclamation } from "@fortawesome/pro-duotone-svg-icons/faTriangleExclamation";
import { faCircleInfo } from "@fortawesome/pro-duotone-svg-icons/faCircleInfo";
import { faUser } from "@fortawesome/pro-duotone-svg-icons/faUser";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";

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
  faDownload,
  faTriangleExclamation,
  faCircleInfo,
  faUser,
  faUsers,
  faGlobe
);

export default {
  components: {
    FontAwesomeIcon,
  },
  props: {
    target_obj: {
      type: Object,
      default: () => {},
    },
    id: {
      type: String,
      default: () => undefined,
    },
    isOpen: {
      type: Boolean,
      default: () => false,
    },
    canManage: {
      type: Boolean,
      default: () => false,
    },
  },
  emits: ["close", "permissions-updated"],
  setup(props) {
    const saving = ref(false);
    const addMenuOpen = ref(false);
    const searchText = ref("");
    const newPermissions = ref({});
    const possibleRoles = ref([]);
    const targetPermissions = { ...props.target_obj?.permissions };

    return {
      saving,
      addMenuOpen,
      targetPermissions,
      newPermissions,
      possibleRoles,
      searchText,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
    target() {
      return this.aurochsData[this.target_obj?.__type + "s"][this.id];
    },
    allRoles() {
      return {
        ...this.aurochsData.users,
        ...this.aurochsData.teams,
        ...this.aurochsData.organizations,
      };
    },
    haveValidPermissions() {
      var foundAdmin = false;
      for (var i in this.newPermissions) {
        if (this.newPermissions[i].administer) {
          foundAdmin = true;
          break;
        }
      }
      return foundAdmin;
    },
    invalidPermissionsMessage() {
      return "At least one role must have administer permissions.";
    },
    haveWarningMessage() {
      var perm, j;
      for (var i in this.newPermissions) {
        perm = this.newPermissions[i];
        if (perm.administer) {
          if (perm.type == "user") {
            if (perm.id == this.aurochsData.user.id) {
              return false;
            }
          } else {
            if (perm.type == "team") {
              for (j in this.aurochsData.user.teams) {
                if (this.aurochsData.user.teams[j].id == perm.id) {
                  return false;
                }
              }
            }
            if (perm.type == "organization") {
              for (j in this.aurochsData.user.organizations) {
                if (this.aurochsData.user.organizations[j].id == perm.id) {
                  return false;
                }
              }
            }
          }
        }
      }
      return true;
    },
    permissionsWarningMessage() {
      return "This will remove your ability to make future permission changes.";
    },
  },
  watch: {
    id: {
      handler: function () {
        this.targetPermissions = { ...this.target.permissions };
        this.createNewPermissions();
        this.updatePossibleRoles();
      },
    },
  },
  mounted() {
    this.targetPermissions = { ...this.target.permissions };
    this.createNewPermissions();
    this.updatePossibleRoles();
  },
  methods: {
    shouldBeVisible(role) {
      return !(`${role.__type}_${role.id}` in this.newPermissions);
    },
    togglePermission(role, permission) {
      if (permission in this.newPermissions[`${role.type}_${role.id}`]) {
        this.newPermissions[`${role.type}_${role.id}`][permission] =
          !this.newPermissions[`${role.type}_${role.id}`][permission];
      } else {
        this.newPermissions[`${role.type}_${role.id}`][permission] = true;
      }
      this.addMenuOpen = false;
    },
    addRole(role) {
      this.newPermissions[`${role.type}_${role.id}`] = this.newPermissions[`${role.type}_${role.id}`] || {
        id: role.id,
        type: role.type,
        role_name: role.role_name,
      };
      this.newPermissions[`${role.type}_${role.id}`].score = true;
      this.newPermissions[`${role.type}_${role.id}`].read = true;
      this.newPermissions[`${role.type}_${role.id}`].write = false;
      this.newPermissions[`${role.type}_${role.id}`].administer = false;
      this.updatePossibleRoles();
    },
    removePermission(role) {
      delete this.newPermissions[`${role.type}_${role.id}`];
      this.addMenuOpen = false;
      this.updatePossibleRoles();
    },
    createNewPermissions() {
      this.newPermissions = {};
      // val = {
      //     "score": {"teams": [], "organizations": [], "users": []},
      //     "read": {"teams": [], "organizations": [], "users": []},
      //     "write": {"teams": [], "organizations": [], "users": []},
      //     "administer": {"teams": [], "organizations": [], "users": []},
      // }
      const role_types = ["users", "organizations", "teams"];
      const access_types = ["score", "read", "write", "administer"];
      var o;
      for (var i in role_types) {
        var role = role_types[i];
        for (var j in access_types) {
          var access = access_types[j];
          for (var user_idx in this.targetPermissions[access][role]) {
            o = this.targetPermissions[access][role][user_idx];
            this.newPermissions[`${o.__type}_${o.id}`] = this.newPermissions[`${o.__type}_${o.id}`] || {
              type: o.__type,
              id: o.id,
              role_name: o.__type == "user" ? o.full_name : o.name,
            };
            this.newPermissions[`${o.__type}_${o.id}`][access] = true;
          }
        }
      }
    },
    updatePossibleRoles() {
      var roles = [];
      const lower_search_text = this.searchText.toLowerCase();
      this.newPermissions;
      var i, o;
      for (i in this.aurochsData.users) {
        o = this.aurochsData.users[i];
        if (
          this.inNewPermissions({ id: o.id, type: "user" }) === false &&
          (!lower_search_text || o.full_name.toLowerCase().indexOf(lower_search_text) != -1)
        ) {
          roles.push({
            id: o.id,
            type: o.__type,
            role_name: o.full_name,
          });
        }
      }

      for (i in this.aurochsData.teams) {
        o = this.aurochsData.teams[i];
        if (
          this.inNewPermissions({ id: o.id, type: "team" }) === false &&
          (!lower_search_text || o.name.toLowerCase().indexOf(lower_search_text) != -1)
        ) {
          roles.push({
            id: o.id,
            type: o.__type,
            role_name: o.name,
          });
        }
      }

      for (i in this.aurochsData.organizations) {
        o = this.aurochsData.organizations[i];
        if (
          this.inNewPermissions({ id: o.id, type: "organization" }) === false &&
          (!lower_search_text || o.name.toLowerCase().indexOf(lower_search_text) != -1)
        ) {
          roles.push({
            id: o.id,
            type: o.__type,
            role_name: o.name,
          });
        }
      }
      this.possibleRoles = roles;
    },
    inNewPermissions(role) {
      var found = `${role.type}_${role.id}` in this.newPermissions;
      return found;
    },
    async savePermissions() {
      this.saving = true;
      var perm_list = [];
      for (var i in this.newPermissions) {
        var p = this.newPermissions[i];
        perm_list.push({
          id: p.id,
          type: p.type,
          score: p.score,
          read: p.read,
          write: p.write,
          administer: p.administer,
        });
      }
      const data = {
        id: this.target.id,
        type: this.target.__type,
        permissions: perm_list,
      };
      await this.$sendEvent("update_permissions", data);
      this.saving = false;
      this.$emit("close", true);
      this.$emit("permissions-updated");
    },
    cancelAdd() {
      this.addMenuOpen = false;
    },
    cancel() {
      this.targetPermissions = { ...this.target.permissions };
      this.addMenuOpen = false;
      this.createNewPermissions();
      this.updatePossibleRoles();
      this.$emit("close", true);
    },
    addAnother() {
      this.addMenuOpen = true;
    },
    slugify(name) {
      return name.toLowerCase().replaceAll(" ", "_").replaceAll('"', "'");
    },
  },
};
</script>

<style scoped>
.permission_caption {
  line-height: 1em;
  vertical-align: bottom;
  padding-bottom: 4px;
}
</style>
