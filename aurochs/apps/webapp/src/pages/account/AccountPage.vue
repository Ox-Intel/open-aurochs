<template>
  <DefaultLayout>
    <div class="flex-1 xl:overflow-y-auto">
      <div class="max-w-3xl mx-auto py-10 px-4 sm:px-6 lg:py-12 lg:px-8">
        <div v-if="showAccountSucessAlert" class="alert alert-success shadow-lg mb-5">
          <span>
            <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />Account successfully
            updated!</span
          >
        </div>

        <h1 class="text-3xl font-extrabold">My Account</h1>

        <form class="mt-6 space-y-8">
          <div class="grid grid-cols-1 gap-y-3 sm:grid-cols-6 sm:gap-x-6">
            <article class="prose sm:col-span-6">
              <!-- <h2 class="text-xl font-medium">Profile</h2> -->
              <p class="text-md">If needed, update your account information below.</p>
            </article>

            <div class="sm:col-span-3">
              <OxInput
                id="first_name"
                v-model="formData.first_name"
                data-cy="first_name"
                placeholder="First Name"
                input-type="text"
                label="First Name"
                no-margin
                @keyup="accountInfoChanged"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                id="last_name"
                v-model="formData.last_name"
                data-cy="last_name"
                placeholder="Last Name"
                input-type="text"
                label="Last Name"
                no-margin
                @keyup="accountInfoChanged"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                id="email"
                v-model="formData.email"
                data-cy="email"
                placeholder="Email"
                input-type="text"
                label="Email"
                no-margin
                @keyup="accountInfoChanged"
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                id="first_name"
                v-model="formData.username"
                data-cy="username"
                placeholder="Username"
                input-type="text"
                label="Username"
                no-margin
                @keyup="accountInfoChanged"
              />
            </div>
          </div>

          <div class="flex justify-end">
            <div class="flex justify-end">
              <button
                data-cy="save-profile"
                type="button"
                role="button"
                class="btn"
                :disabled="savingAccount || !infoHasChanged"
                :class="{
                  'disabled btn-outline': savingAccount || !infoHasChanged,
                  'btn-success': infoHasChanged,
                  saving: savingAccount,
                }"
                @click="updateAccount"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
                {{ savingAccount ? "Saving..." : "Save Changes" }}
              </button>
            </div>
          </div>

          <hr class="border border-blue-gray-900" />

          <div v-if="showPasswordSucessAlert" class="alert alert-success shadow-lg">
            <span>
              <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
              Account successfully updated!</span
            >
          </div>
          <div class="grid grid-cols-1 gap-y-6 sm:grid-cols-6 sm:gap-x-6">
            <article class="prose sm:col-span-6">
              <h2 class="text-xl font-medium">Password</h2>
              <p class="text-md">If you need to change your password, you can update it below.</p>
              <p
                v-if="!validPassword && newPassword.length > 0 && confirmPassword.length > 0"
                class="text-md text-error"
              >
                Passwords do not match
              </p>
            </article>

            <div class="sm:col-span-3">
              <OxInput
                id="newPassword"
                v-model="newPassword"
                placeholder="Enter new password..."
                input-type="password"
                label="New Password"
                no-margin
              />
            </div>

            <div class="sm:col-span-3">
              <OxInput
                id="confirmPassword"
                v-model="confirmPassword"
                placeholder="Confirm password..."
                input-type="password"
                label="Confirm Password"
                no-margin
              />
            </div>
          </div>

          <div class="flex justify-end">
            <div class="flex justify-end">
              <button
                type="button"
                role="button"
                class="btn"
                :disabled="savingPassword || !validPassword"
                :class="{
                  'disabled btn-outline': !validPassword,
                  'btn-success': validPassword,
                  saving: savingPassword,
                }"
                data-cy="update-password-button"
                @click="updatePassword"
              >
                <FontAwesomeIcon :icon="['fad', 'check']" class="h-4 w-4 mr-2" aria-hidden="true" />
                {{ savingPassword ? "Saving..." : "Update Password" }}
              </button>
            </div>
          </div>
          <!-- <hr class="border border-blue-gray-900" />
          <div>
            <h2 class="text-xl font-medium">Ox Interface</h2>
            <div class="form-control">
              <label class="label">
                <span class="label-text">Dark Mode</span>
              </label>
              <div class="btn-group">
                <button class="btn btn-outline">Auto</button>
                <button class="btn btn-primary">Dark</button>
                <button class="btn btn-outline">Light</button>
              </div>
            </div>
          </div> -->
        </form>
      </div>
    </div>
  </DefaultLayout>
</template>

<script>
import DefaultLayout from "../../layouts/DefaultLayout.vue";
import { useAurochsData } from "../../stores/aurochs";
import { ref } from "vue";
import OxInput from "../../components/common/forms/OxInput.vue";

// Font awesome config
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
// Skip the tree-shaking that slows down build by deep-importing, and get better errors.
import { faCheck } from "@fortawesome/pro-duotone-svg-icons/faCheck";

library.add(faCheck);

export default {
  components: { DefaultLayout, FontAwesomeIcon, OxInput },
  setup() {
    const aurochsData = useAurochsData();
    const savingAccount = ref(false);
    const savingPassword = ref(false);
    const infoHasChanged = ref(false);
    const newPassword = ref("");
    const confirmPassword = ref("");
    const formData = ref({});
    const showAccountSucessAlert = ref(false);
    const showPasswordSucessAlert = ref(false);
    document.title = "Your Profile";

    return {
      aurochsData,
      savingAccount,
      savingPassword,
      infoHasChanged,
      newPassword,
      confirmPassword,
      formData,
      showAccountSucessAlert,
      showPasswordSucessAlert,
    };
  },
  computed: {
    user() {
      return this.aurochsData?.user;
    },
    validPassword() {
      return this.newPassword === this.confirmPassword && this.newPassword !== "";
    },
  },
  mounted() {
    this.resetForm();
  },
  methods: {
    accountInfoChanged() {
      this.infoHasChanged = !(
        this.formData.first_name == this.user.first_name &&
        this.formData.last_name == this.user.last_name &&
        this.formData.email == this.user.email &&
        this.formData.username == this.user.username
      );
    },
    resetForm() {
      this.formData = {
        first_name: this.user.first_name,
        last_name: this.user.last_name,
        email: this.user.email,
        username: this.user.username,
      };
    },
    async updateAccount() {
      this.savingAccount = true;
      const data = { ...this.formData };
      await this.$sendEvent("update_my_user", data);
      this.resetForm();
      this.accountInfoChanged();
      this.displayAccountSuccess();
      this.savingAccount = false;
    },
    async updatePassword() {
      if (this.newPassword) {
        this.savingPassword = true;
        const data = {
          new_password: this.newPassword,
        };
        await this.$sendEvent("change_password", data);
        this.displayPasswordSuccess();
        this.newPassword = "";
        this.confirmPassword = "";
        this.savingPassword = false;
      }
    },
    displayAccountSuccess() {
      this.showAccountSucessAlert = true;
      setTimeout(() => {
        this.showAccountSucessAlert = false;
      }, 1500);
    },
    displayPasswordSuccess() {
      this.showPasswordSucessAlert = true;
      setTimeout(() => {
        this.showPasswordSucessAlert = false;
      }, 1500);
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
</style>
