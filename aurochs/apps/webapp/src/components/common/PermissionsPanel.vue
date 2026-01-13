<template>
  <article class="prose max-w-none" data-cy="permissions">
    <p class="text-lg">
      Ox {{ target.__type }}s can be shared with other users, teams, and organizations. This {{ target.__type }} can be
      accessed by:
    </p>

    <div class="card w-11/12 md:w-9/12 lg:w-3/5 bg-base-100 shadow-md cursor-pointer border border-base-200">
      <div class="card-body">
        <template v-if="canManage && editing">
          <table class="w-full">
            <tr>
              <th class="text-left text-md">Role</th>
              <th v-if="target?.__type == 'report'" class="permission_caption">Score</th>
              <th class="permission_caption">View</th>
              <th class="permission_caption">Edit</th>
              <th class="permission_caption">Admin</th>
              <th class="w-24" />
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

              <td v-if="target?.__type == 'report'" class="text-center">
                <button
                  data-cy="can-score"
                  class="btn btn-square btn-sm text-success-content cursor-pointer"
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
                  class="btn btn-square btn-sm text-success-content cursor-pointer"
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
                  class="btn btn-square btn-sm text-success-content cursor-pointer"
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
                  class="btn btn-square btn-sm text-success-content cursor-pointer"
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
                  v-if="Object.keys(newPermissions).length > 1"
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
                class="menu bg-base-200 min-w-max max-w-96 pl-0 mr-12 max-h-64 overflow-hidden"
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
                      <span class="align-middle">{{ r.role_name }}</span>
                    </div>
                  </li>
                </template>
              </ul>
            </div>
          </div>
          <div>
            <div
              v-if="!addMenuOpen"
              data-cy="add-another"
              class="btn btn-primary mt-4"
              role="button"
              @click="addAnother"
            >
              <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
              Add Another
            </div>
          </div>
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
            <button
              type="button"
              role="button"
              class="btn btn-outline btn-base-300 hover:btn-error mr-2"
              @click="cancel"
            >
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
        <template v-if="!canManage || !editing">
          <table class="w-full my-4" data-cy="read-only-permissions">
            <tr>
              <th class="text-left text-md">Role</th>
              <th v-if="target?.__type == 'report'" class="permission_caption">Score</th>
              <th class="permission_caption">View</th>
              <th class="permission_caption">Edit</th>
              <th class="permission_caption">Admin</th>
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
              <td v-if="target?.__type == 'report'" class="text-center">
                <FontAwesomeIcon v-if="p.score || p.write || p.administer" :icon="['fad', 'check']" class="h-4 w-4" />
              </td>
              <td class="text-center">
                <FontAwesomeIcon v-if="p.read || p.write || p.administer" :icon="['fad', 'check']" class="h-4 w-4" />
              </td>
              <td class="text-center">
                <FontAwesomeIcon v-if="p.write || p.administer" :icon="['fad', 'check']" class="h-4 w-4" />
              </td>
              <td class="text-center">
                <FontAwesomeIcon v-if="p.administer" :icon="['fad', 'check']" class="h-4 w-4" />
              </td>
            </tr>
          </table>
          <div v-if="canManage" class="flex flex-row-reverse">
            <button type="button" role="button" class="btn btn-primary" data-cy="edit-permissions" @click="startEdit()">
              <FontAwesomeIcon :icon="['fad', 'pen']" class="mr-2" />
              Edit
            </button>
          </div>
        </template>
      </div>
    </div>
  </article>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import { getRoleFromPermissionsString, getPermissionsDictFromAccessString } from "../../mixins/permissions.js";
import { ref } from "vue";
// import OxAvatar from "./OxAvatar.vue";

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
    // OxAvatar,
  },
  props: {
    target: {
      type: Object,
      default: () => {},
    },
    canManage: {
      type: Boolean,
      default: () => false,
    },
  },
  emits: ["permissions-updated"],
  setup(props) {
    const saving = ref(false);
    const addMenuOpen = ref(false);
    const editing = ref(false);
    const searchText = ref("");
    const newPermissions = ref({});
    const possibleRoles = ref([]);
    const targetPermissions = { ...props.target?.permissions };

    return {
      saving,
      addMenuOpen,
      editing,
      targetPermissions,
      newPermissions,
      possibleRoles,
      searchText,
      aurochsData: useAurochsData(),
    };
  },
  computed: {
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
      // const role_types = ["users", "organizations", "teams"];
      // const access_types = ["score", "read", "write", "administer"];

      for (var id_str in this.targetPermissions) {
        let o = getRoleFromPermissionsString(id_str, this.aurochsData);
        let permissions_dict = getPermissionsDictFromAccessString(this.targetPermissions[id_str]);

        this.newPermissions[`${o.__type}_${o.id}`] = this.newPermissions[`${o.__type}_${o.id}`] || {
          type: o.__type,
          id: o.id,
          role_name: o.__type == "user" ? o.full_name : o.name,
        };

        this.newPermissions[`${o.__type}_${o.id}`] = {
          ...this.newPermissions[`${o.__type}_${o.id}`],
          ...permissions_dict,
        };
      }
    },
    updatePossibleRoles() {
      var roles = [];
      const lower_search_text = this.searchText.toLowerCase();
      this.newPermissions;
      let num_to_show = 4;
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
          if (roles.length >= num_to_show) {
            this.possibleRoles = roles;
            return;
          }
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
          if (roles.length >= num_to_show) {
            this.possibleRoles = roles;
            return;
          }
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
          if (roles.length >= num_to_show) {
            this.possibleRoles = roles;
            return;
          }
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
          score: p.score || p.write || p.administer,
          read: p.read || p.write || p.administer,
          write: p.write || p.administer,
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
      this.editing = false;
      this.$emit("permissions-updated");
    },
    cancelAdd() {
      this.addMenuOpen = false;
    },
    startEdit() {
      this.editing = true;
    },
    cancel() {
      this.targetPermissions = { ...this.target.permissions };
      this.addMenuOpen = false;
      this.createNewPermissions();
      this.updatePossibleRoles();
      this.editing = false;
      // this.$emit("close", true);
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
  @apply text-center w-16;
  line-height: 1em;
  vertical-align: bottom;
  padding-bottom: 4px;
}
</style>
