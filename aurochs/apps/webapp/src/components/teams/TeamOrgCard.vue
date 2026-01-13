<template>
  <div class="card bg-base-100 border border-base-300 shadow-lg mb-12" :data-item-name="slugify(target.name)">
    <div class="card-body">
      <div class="card-title">
        <div class="flex w-full flex-nowrap">
          <div class="text-2xl font-bold grow flex flex-nowrap">
            <FontAwesomeIcon v-if="type == 'team'" :icon="['fad', 'users']" class="mr-2 mt-2" />
            <FontAwesomeIcon v-if="type == 'organization'" :icon="['fad', 'globe']" class="mr-2 mt-2" />
            <span v-if="!editing" class="mt-1 ml-1">{{ target.name }}</span>
            <div v-if="editing" class="grow">
              <input
                v-model="formData.name"
                data-cy="team-name-input"
                autofocus
                type="text"
                class="w-full bg-base-100 text-2xl p-1 font-bold border-x-0 border-t-0 border-b-2 ring-0 focus:ring-0"
              />
            </div>
          </div>
          <template v-if="myUserCanManage">
            <button
              v-if="!editing"
              data-cy="start-edit"
              role="button"
              class="btn btn-outline btn-circle btn-primary whitespace-nowrap mr-2 -mt-2"
              @click="startEdit()"
            >
              <FontAwesomeIcon :icon="['fad', 'pen']" class="align-middle h-4 w-4" />
              <!-- Edit -->
            </button>
            <div
              :class="!target.can_be_deleted ? 'tooltip z-50 tooltip-left tooltip-bottom' : ''"
              :data-tip="
                !target.can_be_deleted && target.last_admin_for_count
                  ? 'This team cannot be deleted because it is the sole administrator of ' +
                    (target.last_admin_for_count.length == 0
                      ? 'one or more items'
                      : 'at least ' +
                        target.last_admin_for_count.length +
                        ' item' +
                        (target.last_admin_for_count.length > 1 ? 's' : '')) +
                    '.'
                  : ''
              "
            >
              <button
                v-if="!editing"
                role="button"
                :disabled="!target.can_be_deleted"
                class="btn btn-outline btn-circle whitespace-nowrap -mt-2 -mr-2"
                :class="target.can_be_deleted ? 'btn-error' : 'btn-base-300'"
                @click="deleteTarget()"
              >
                <FontAwesomeIcon :icon="['fad', 'trash-can']" class="align-middle h-4 w-4" />
                <!-- Delete -->
              </button>
            </div>
          </template>
        </div>
      </div>

      <p v-if="!editing" class="my-0" :class="!target.description ? 'mb-2' : ''">
        {{ target.description }}
      </p>
      <div v-if="editing" class="w-full">
        <OxTextarea
          v-model="formData.description"
          :placeholder="`About this ${target.__type}...`"
          input-type="textarea"
          label="Description"
          :classes="'w-full'"
          :size="'md'"
        />
      </div>
      <div v-if="type == 'team' || myUserCanManage || editing" class="flex">
        <div class="grow font-bold"></div>
        <!-- <div class="w-16 text-center font-bold">Active</div> -->
        <div class="w-16 text-center font-bold">Admin</div>
        <div v-if="editing" class="w-16 text-center font-bold"></div>
      </div>
      <div v-if="type == 'organization' && !myUserCanManage" class="flex">
        <div class="grow font-bold">Administrators</div>
        <!-- <div class="w-1/3 text-left font-bold">Email</div> -->
      </div>

      <template v-if="editing">
        <div v-for="(member, p_idx) in formData.members" :key="p_idx" class="flex">
          <div class="grow">
            {{ member.full_name ? member.full_name : getPerson(member.id).full_name }}
          </div>
          <!-- <div class="w-16 text-center">
            <button
              class="btn btn-square btn-sm text-success-content"
              :class="
                member.can_view
                  ? ' btn-success '
                  : ' btn-outline bg-base-300 border-base-300 hover:bg-medium-grey hover:border-base-300'
              "
              role="button"
              @click="togglePermission(member, 'can_view')"
            >
              <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
            </button>
          </div> -->
          <div class="w-16 text-center">
            <button
              class="btn btn-square btn-sm text-success-content"
              :class="
                member.can_manage
                  ? ' btn-success '
                  : ' btn-outline bg-base-300 border-base-300 hover:bg-medium-grey hover:border-base-300'
              "
              role="button"
              @click="togglePermission(member, 'can_manage')"
            >
              <FontAwesomeIcon :icon="['fad', 'check']" class="h-6 w-6" />
            </button>
          </div>
          <div v-if="editing" class="w-16 text-center">
            <button
              class="btn btn-circle btn-sm border-0 btn-outline hover:bg-error hover:border-error"
              role="button"
              @click="removeRole(member)"
            >
              <FontAwesomeIcon :icon="['fad', 'trash-can']" class="h-4 w-4" />
            </button>
          </div>
        </div>
        <div class="relative">
          <div v-if="addMenuOpen" class="mt-4 max-h-60">
            <div class="flex">
              <input
                ref="searchField"
                v-model="searchText"
                data-cy="search–existing"
                type="text"
                placeholder="Search for a user..."
                class="input input-bordered w-full"
                autofocus
                @input="updatePossibleRoles"
              />
              <div class="align-middle text-center w-12 h-12 pt-1 hover:text-error" role="button" @click="cancelAdd">
                <FontAwesomeIcon :icon="['fad', 'xmark']" class="h-8 w-8" />
              </div>
            </div>
            <ul class="menu bg-base-200 min-w-max max-w-96 pl-0 mr-12 max-h-48 overflow-hidden mt-0">
              <template v-for="(r, idx) in possibleRoles" :key="idx">
                <li
                  :data-cy="`possible-role-${idx}`"
                  role="button"
                  class="hover:bg-base-300 box-rounded rounded-md my-0 w-full"
                  @click="addRole(r)"
                >
                  <div class="p-2 align-middle">
                    <FontAwesomeIcon :icon="['fad', 'user']" class="mr-1 h-4 w-4" />
                    {{ type == "team" ? r.full_name : r.display }}
                  </div>
                </li>
              </template>
            </ul>
          </div>
        </div>
        <div class="flex w-full gap-4">
          <button
            v-if="!addMenuOpen"
            data-cy="add-existing"
            class="btn btn-primary mt-4"
            role="button"
            @click="addAnother"
          >
            <FontAwesomeIcon :icon="['fad', 'user']" class="mr-2" />
            Add Another
          </button>
          <button
            v-if="!addMenuOpen && type == 'organization'"
            data-cy="add-new"
            class="btn btn-primary mt-4"
            role="button"
            @click="startNewUser"
          >
            <FontAwesomeIcon :icon="['fad', 'plus']" class="mr-2" />
            New User
          </button>
        </div>
      </template>
      <template v-if="!editing">
        <div v-if="type == 'team'" class="flex">
          <div class="grow">
            <FontAwesomeIcon :icon="['fad', 'globe']" />
            {{ target.organization.name }}
          </div>
          <!--           <div class="w-16 text-center">
            <div>
              <FontAwesomeIcon :icon="['fad', 'check']" />
            </div>
          </div> -->
          <div class="w-16 text-center">
            <div>
              <FontAwesomeIcon :icon="['fad', 'check']" />
            </div>
          </div>
        </div>
        <template v-for="(member, p_idx) in target.members" :key="p_idx">
          <template v-if="type == 'team' || myUserCanManage">
            <div class="flex">
              <div class="grow">
                {{ getPerson(member.id).full_name }}
              </div>
              <!-- <div class="w-16 text-center">
                <div>
                  <FontAwesomeIcon
                    :icon="['fad', 'check']"
                    :class="member.can_view ? '' : 'text-base-300'"
                  />
                </div>
              </div> -->
              <div class="w-16 text-center">
                <div>
                  <FontAwesomeIcon :icon="['fad', 'check']" :class="member.can_manage ? '' : 'text-base-300'" />
                </div>
              </div>
            </div>
          </template>
          <template v-if="type == 'organization' && member.can_manage && !myUserCanManage">
            <div class="flex">
              <div class="grow">
                {{ getPerson(member.id).full_name }}
              </div>
              <!--        <div class="w-1/3 text-left">
                <div >
                  {{ getPerson(member.id).email }}
                </div>
              </div> -->
            </div>
          </template>
        </template>
      </template>
      <div v-if="editing">
        <div v-if="!haveValidPermissions" class="alert alert-error alert-outline my-4">
          <p class="m-0">
            <FontAwesomeIcon :icon="['fad', 'triangle-exclamation']" class="" />
            At least one user must have administration permissions.
          </p>
        </div>
        <div
          v-if="type == 'organization' && !myUserIsAdmin && haveValidPermissions"
          class="alert alert-warning alert-outline my-4"
        >
          <p class="m-0">
            <FontAwesomeIcon :icon="['fad', 'circle-info']" class="" />
            This will remove your ability to manage this organization.
          </p>
        </div>
        <div class="flex flex-row justify-end mt-6">
          <button
            type="button"
            role="button"
            class="btn btn-outline btn-base-300 hover:btn-error mr-2"
            @click="cancel()"
          >
            <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2 w-4 h-4 align-middle" />
            Cancel
          </button>
          <button
            data-cy="save"
            type="button"
            role="button"
            class="btn btn-success"
            :class="{ saving: saving }"
            :disabled="saving || !haveValidPermissions"
            @click="save"
          >
            <FontAwesomeIcon v-if="!saving" :icon="['fad', 'check']" class="mr-2 w-4 h-4 align-middle" />
            <FontAwesomeIcon v-if="saving" :icon="['fad', 'rotate']" class="mr-2 w-4 h-4 align-middle fa-spin" />
            {{ saving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
    </div>
    <div v-if="!editing" class="">
      <div class="stats lg:stats-horizontal shadow w-full">
        <!-- bg-ox-score text-ox-score-content -->
        <div class="stat place-items-center">
          <div class="stat-title">Members</div>
          <div class="stat-value">
            {{ target.members ? target.members.length : 0 }}
          </div>
        </div>
        <div class="stat place-items-center">
          <div class="stat-title">Admins</div>
          <div class="stat-value">{{ admins ? admins.length : 0 }}</div>
        </div>
        <div class="stat place-items-center">
          <div class="stat-title">Reports</div>
          <div class="stat-value">
            {{ target.num_reports }}
          </div>
        </div>
        <div class="stat place-items-center">
          <div class="stat-title">Frameworks</div>
          <div class="stat-value">
            {{ target.num_frameworks }}
          </div>
        </div>
        <div class="stat place-items-center">
          <div class="stat-title">Stacks</div>
          <div class="stat-value">
            {{ target.num_stacks }}
          </div>
        </div>
      </div>
    </div>
  </div>
  <input :id="`create-user-modal_${type}_${target.id}`" type="checkbox" class="modal-toggle" />
  <div class="modal">
    <div class="modal-box max-w-screen-sm p-10" :class="addMenuOpen ? ' ' : ''">
      <div class="relative">
        <label :for="`create-user-modal_${type}_${target.id}`" class="btn btn-sm btn-circle absolute right-0 top-0">
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="align-middle fa-swap-opacity" />
        </label>
      </div>
      <h3 class="text-2xl font-bold mt-0">
        <FontAwesomeIcon :icon="['fad', 'user']" class="mr-2 align-middle" />
        Create User
      </h3>
      <div class="">
        <form class="mt-6 space-y-8">
          <div class="grid grid-cols-1 gap-y-3 sm:grid-cols-6 sm:gap-x-6">
            <div class="sm:col-span-3">
              <OxInput
                :id="`first_name_${type}_${target.id}`"
                v-model="newUserFormData.first_name"
                placeholder="First Name"
                input-type="text"
                label="First Name"
                autofocus
                no-margin
                @input="updateHaveValidAddUserForm"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                :id="`last_name_${type}_${target.id}`"
                v-model="newUserFormData.last_name"
                placeholder="Last Name"
                input-type="text"
                label="Last Name"
                no-margin
                @input="updateHaveValidAddUserForm"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                :id="`email_${type}_${target.id}`"
                v-model="newUserFormData.email"
                placeholder="Email"
                input-type="text"
                label="Email"
                no-margin
                @input="updateHaveValidAddUserForm"
              />
            </div>

            <div class="sm:col-span-3 -mr-4">
              <div class="flex flex-nowrap">
                <OxInput
                  :id="`username_${type}_${target.id}`"
                  v-model="newUserFormData.username"
                  placeholder="Username"
                  input-type="text"
                  label="Username"
                  no-margin
                  class="grow"
                  @input="usernameChanged"
                />
                <div class="mt-12 pt-2 ml-2 w-2">
                  <FontAwesomeIcon
                    v-if="checkedUsername && !checkingUsername && usernameIsValid"
                    :icon="['fad', 'check']"
                    class="text-success"
                  />
                  <FontAwesomeIcon
                    v-if="checkedUsername && checkingUsername"
                    :icon="['fad', 'circle-notch']"
                    class="fa-spin"
                  />
                  <div class="tooltip tooltip-left" data-tip="This username is not available.">
                    <FontAwesomeIcon
                      v-if="checkedUsername && !checkingUsername && !usernameIsValid"
                      :icon="['fad', 'xmark']"
                      class="text-error fa-swap-opacity"
                    />
                  </div>
                </div>
              </div>
            </div>

            <div class="sm:col-span-3">
              <OxInput
                :id="`password_${type}_${target.id}`"
                v-model="newPassword"
                placeholder="Enter new password..."
                input-type="password"
                label="New Password"
                no-margin
                @input="updateHaveValidAddUserForm"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                :id="`confirmpassword_${type}_${target.id}`"
                v-model="confirmPassword"
                placeholder="Confirm password..."
                input-type="password"
                label="Confirm Password"
                no-margin
                @input="updateHaveValidAddUserForm"
              />
            </div>
          </div>
          <article class="prose max-w-none sm:col-span-6">
            <p
              v-if="newPassword.length > 0 && confirmPassword.length > 0 && newPassword != confirmPassword"
              class="text-md text-error"
            >
              Passwords do not match
            </p>
          </article>
        </form>
      </div>
      <div class="flex flex-row justify-end mt-6">
        <button
          type="button"
          role="button"
          class="btn btn-outline btn-base-300 hover:btn-error mr-2"
          @click="cancelNewUser"
        >
          <FontAwesomeIcon :icon="['fad', 'xmark']" class="mr-2" />
          Cancel
        </button>
        <button
          type="button"
          role="button"
          class="btn"
          :disabled="creatingUser || !haveValidAddUserForm"
          :class="{
            'disabled btn-outline': creatingUser || !haveValidAddUserForm,
            'btn-success': haveValidAddUserForm,
            saving: creatingUser,
          }"
          @click="createUser"
        >
          <FontAwesomeIcon :icon="['fad', 'check']" class="mr-2" />
          {{ creatingUser ? "Creating..." : "Create" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useAurochsData } from "../../stores/aurochs";
import { sendEvent } from "../../mixins/events.js";
import { ref, reactive } from "vue";
import OxTextarea from "../common/forms/OxTextarea.vue";
import OxInput from "../common/forms/OxInput.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faGlobe } from "@fortawesome/pro-duotone-svg-icons/faGlobe";
import { faUsers } from "@fortawesome/pro-duotone-svg-icons/faUsers";
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";
import { faPlus } from "@fortawesome/pro-duotone-svg-icons/faPlus";
import { faTrashCan } from "@fortawesome/pro-duotone-svg-icons/faTrashCan";
import { faXmark } from "@fortawesome/pro-duotone-svg-icons/faXmark";
import { faCircleNotch } from "@fortawesome/pro-duotone-svg-icons/faCircleNotch";

library.add(faGlobe, faUsers, faCheck, faPlus, faTrashCan, faXmark, faCircleNotch);

export default {
  components: {
    FontAwesomeIcon,
    OxTextarea,
    OxInput,
  },
  props: {
    target: {
      type: Object,
      required: true,
    },
    is_new: {
      type: Boolean,
    },
  },
  setup(props) {
    const formData = ref({ ...props.target });
    const editing_on = ref(false);
    const saving = ref(false);
    const addMenuOpen = ref(false);
    const addUserOpen = ref(false);
    const hasSaved = ref(false);
    const searchText = ref("");
    const type = ref(props.target.__type);
    const possibleRoles = ref([]);
    const newPassword = ref("");
    const confirmPassword = ref("");
    const newUserFormData = reactive({
      first_name: "",
      last_name: "",
      email: "",
      username: "",
      password: "",
    });
    const creatingUser = ref(false);
    const haveValidAddUserForm = ref(false);
    const checkingUsername = ref(false);
    const checkedUsername = ref(false);
    const usernameIsValid = ref(false);
    const have_cancelled = ref(false);

    return {
      aurochsData: useAurochsData(),
      formData,
      editing_on,
      saving,
      hasSaved,
      addMenuOpen,
      addUserOpen,
      searchText,
      type,
      possibleRoles,
      newUserFormData,
      newPassword,
      confirmPassword,
      creatingUser,
      have_cancelled,
      haveValidAddUserForm,
      checkingUsername,
      checkedUsername,
      usernameIsValid,
    };
  },
  computed: {
    admins() {
      var admins = [];
      for (var i in this.target.members) {
        if (this.target.members[i].can_manage) {
          admins.push(this.target.members[i]);
        }
      }
      return admins;
    },
    myUserCanManage() {
      let m;
      for (m in this.target.members) {
        if (this.target.members[m].id == this.aurochsData.user.id) {
          if (this.target.members[m].can_manage) {
            return true;
          }
          break;
        }
      }
      if (this.type == "team") {
        for (m in this.target.organization.members) {
          if (this.target.organization.members[m].id == this.aurochsData.user.id) {
            return this.target.organization.members[m].can_manage;
          }
        }
      }
      return false;
    },
    haveValidPermissions() {
      if (this.type == "organization") {
        for (let i in this.formData.members) {
          if (this.formData.members[i].can_manage) {
            return true;
          }
        }
        return false;
      }
      return true;
    },
    myUserIsAdmin() {
      for (let i in this.formData.members) {
        if (this.formData.members[i].can_manage && this.formData.members[i].id == this.aurochsData.user.id) {
          return true;
        }
      }
      return false;
    },
    isNew() {
      return !this.hasSaved && this.is_new;
    },
    editing() {
      // TODO: come back to this, edit by default isn't working cleanly and I don't know why.
      return this.editing_on;
      // return this.editing_on || (this.isNew && !this.have_cancelled)
    },
  },
  watch: {
    id: {
      handler: function () {
        this.updatePossibleRoles();
        this.have_cancelled = false;
        this.formData = { ...this.target };
      },
    },
  },
  mounted() {
    this.updatePossibleRoles();
    this.have_cancelled = false;
    this.formData = { ...this.target };
  },
  methods: {
    updatePossibleRoles() {
      if (!this.myUserCanManage) {
        return [];
      }
      let all_roles;
      let current_roles;
      let found = false;
      if (this.type == "organization") {
        all_roles = this.aurochsData.userPool;
      } else {
        all_roles = this.target.organization.members;
      }
      if (this.type == "organization") {
        current_roles = this.formData.members;
      } else {
        current_roles = this.formData.members;
      }
      var roles = [];
      for (var i in all_roles) {
        // TODO Ugh, this is deadline code and desperately eneds refactored.  So much ugh.
        let p = this.type == "team" ? this.getPerson(all_roles[i].id) : all_roles[i];
        let search_matched = false;
        if (this.searchText) {
          let lower_search_text = this.searchText.toLowerCase();
          if (
            (this.type == "team" && p.full_name.toLowerCase().indexOf(lower_search_text) != -1) ||
            (this.type == "organization" && p.display.toLowerCase().indexOf(lower_search_text) != -1)
          ) {
            search_matched = true;
          }
        } else {
          search_matched = true;
        }
        if (search_matched) {
          found = false;
          for (let j in current_roles) {
            if ((p.id && current_roles[j].id == p.id) || current_roles[j].id == p.id) {
              found = true;
              break;
            }
          }
          if (!found) {
            roles.push(p);
          }
          if (roles.length > 8) {
            break;
          }
        }
      }
      this.possibleRoles = roles;
    },
    addRole(role) {
      this.formData.members.push({
        can_view: true,
        can_manage: false,
        id: role.id,
        full_name: role.full_name,
        teams: [],
        organizations: [],
      });
      this.updatePossibleRoles();
    },
    removeRole(role) {
      let members = [];
      let found = false;
      for (let i in this.formData.members) {
        found = false;
        if (this.formData.members[i].id == role.id) {
          found = true;
        }
        if (!found) {
          members.push(this.formData.members[i]);
        }
      }
      this.formData.members = members;
      this.updatePossibleRoles();
    },
    getPerson(id) {
      if (id in this.aurochsData.users) {
        return this.aurochsData.users[id];
      }
      if (id in this.aurochsData.userPool) {
        return this.aurochsData.userPool[id];
      }
    },
    async usernameChanged() {
      clearTimeout(this.usernameTimeout);
      this.checkedUsername = false;
      this.checkingUsername = true;
      this.usernameIsValid = false;
      this.usernameTimeout = setTimeout(async () => {
        let ret_data = await sendEvent("check_username", { username: this.newUserFormData.username }, {});
        this.usernameIsValid = ret_data.available;
        this.updateHaveValidAddUserForm();
        this.checkingUsername = false;
        this.checkedUsername = true;
      }, 200);
    },
    updateHaveValidAddUserForm() {
      let valid =
        this.newUserFormData.first_name.length > 0 &&
        this.newUserFormData.last_name.length > 0 &&
        this.newUserFormData.email.length > 0 &&
        this.newUserFormData.email.indexOf("@") != -1 &&
        this.newUserFormData.email.indexOf(".") != -1 &&
        this.usernameIsValid &&
        this.newUserFormData.username.length > 0 &&
        this.newPassword.length > 0 &&
        this.confirmPassword.length > 0 &&
        this.newPassword == this.confirmPassword;
      if (valid != this.haveValidAddUserForm) {
        this.haveValidAddUserForm = valid;
      }
    },
    startEdit() {
      this.formData = { ...this.aurochsData[this.type + "s"][this.target.id] };
      let members = [];
      for (let i in this.formData.members) {
        members.push({ ...this.formData.members[i] });
      }
      this.formData.members = members;
      this.editing_on = true;
    },
    cancel() {
      this.editing_on = false;
      this.have_cancelled = true;
      this.formData = { ...this.aurochsData[this.type + "s"][this.target.id] };
    },
    async save() {
      this.saving = true;
      const data = {
        id: this.target.id,
        name: this.formData.name,
        description: this.formData.description,
        members: [],
      };
      for (let i in this.formData.members) {
        data.members.push({
          // can_view: this.formData.members[i].can_view,
          can_view: true,
          can_manage: this.formData.members[i].can_manage,
          id: this.formData.members[i].id,
        });
      }
      await this.$sendEvent(`update_${this.type}`, data);
      this.hasSaved = true;
      this.saving = false;
      this.editing_on = false;
    },
    async deleteTarget() {
      if (confirm(`Are you sure you want to delete this ${this.type}?`)) {
        const data = {
          id: this.target.id,
        };
        await this.$sendEvent(`delete_${this.type}`, data);
      }
    },
    togglePermission(member, permission) {
      for (var m in this.formData.members) {
        if (this.formData.members[m].id == member.id) {
          this.formData.members[m][permission] = !this.formData.members[m][permission];
        }
      }
    },
    cancelAdd() {
      this.addMenuOpen = false;
    },
    addAnother() {
      this.addMenuOpen = true;
      this.$nextTick(() => {
        this.$refs.searchField.focus();
      });
    },
    startNewUser() {
      this.addUserOpen = true;
      this.creatingUser = false;
      this.newUserFormData = {
        first_name: "",
        last_name: "",
        email: "",
        username: "",
        password: "",
      };
      document.getElementById(`create-user-modal_${this.type}_${this.target.id}`).checked = true;
      this.updateHaveValidAddUserForm();
    },
    cancelNewUser() {
      this.addUserOpen = false;
      document.getElementById(`create-user-modal_${this.type}_${this.target.id}`).checked = false;
      this.newUserFormData = {
        first_name: "",
        last_name: "",
        email: "",
        username: "",
        password: "",
      };
      this.newPassword = "";
      this.confirmPassword = "";
      this.updateHaveValidAddUserForm();
    },
    async createUser() {
      this.creatingUser = true;
      let data = { ...this.newUserFormData };
      data["password"] = this.newPassword;
      data["org_id"] = this.target.id;
      let ret_data = await this.$sendEvent("create_user", data);
      for (let i in this.aurochsData.organizations[this.target.id].members) {
        if (this.aurochsData.organizations[this.target.id].members[i].id == ret_data.target_obj_ox_id) {
          this.formData.members.push({ ...this.aurochsData.organizations[this.target.id].members[i] });
        }
      }
      this.creatingUser = false;
      this.cancelNewUser();
    },
    slugify(name) {
      return name.toLowerCase().replaceAll(" ", "_").replaceAll('"', "'");
    },
  },
};
</script>

<style scoped>
article {
  width: 80vw;
}
</style>
