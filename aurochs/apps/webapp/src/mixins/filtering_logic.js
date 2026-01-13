export default {
  computed: {
    filterByUser() {
      return this.activities.filter((value) => {
        let users = value.permissions.administer.users;
        let userIds = users.map((record) => {
          return record?.id;
        });
        if (userIds.length > 0) {
          return userIds.includes(this.userId);
        }
        return false;
      });
    },
    filterByTeam() {
      const filterTeamId = this.filterOrgModel.record.id;
      return this.activities.filter((value) => {
        let teams = value.permissions.read.teams;
        let teamIds = teams.map((record) => {
          return record.id;
        });
        if (teamIds.length > 0) {
          return teamIds.includes(filterTeamId);
        } else {
          return false;
        }
      });
    },
    filterByOrganization() {
      const filterOrgId = this.filterOrgModel.record.id;
      return this.activities.filter((value) => {
        let organizations = value.permissions.read.organizations;
        let orgIds = organizations.map((record) => {
          return record?.id;
        });
        if (orgIds.length > 0) {
          return orgIds.includes(filterOrgId);
        }
        return false;
      });
    },
    filterBySearchAndUser() {
      return this.activities.filter((value) => {
        let users = value.permissions.administer.users;
        let userIds = users.map((record) => {
          return record?.id;
        });
        return (
          value.search_text.toLowerCase().search(this.searchQuery.toLowerCase()) > -1 && userIds.includes(this.userId)
        );
      });
    },
    filterBySearch() {
      if (this.searchQuery) {
        return this.activities.filter((value) => {
          return value.search_text.toLowerCase().search(this.searchQuery.toLowerCase()) > -1;
        });
      }
      return this.activities;
    },
    filterBySearchAndOrg() {
      const filterOrgId = this.filterOrgModel.record.id;
      return this.activities.filter((value) => {
        let organizations = value.permissions.read.organizations;
        let orgIds = organizations.map((record) => {
          return record.id;
        });
        return (
          value.search_text.toLowerCase().search(this.searchQuery.toLowerCase()) > -1 &&
          (orgIds ? orgIds.includes(filterOrgId) : false)
        );
      });
    },
    filterBySearchAndTeam() {
      const filterTeamId = this.filterOrgModel.record.id;
      return this.activities.filter((value) => {
        let teams = value.permissions.read.teams;
        let teamIds = teams.map((record) => {
          return record.id;
        });
        return (
          value.search_text.toLowerCase().search(this.searchQuery.toLowerCase()) > -1 &&
          (teamIds ? teamIds.includes(filterTeamId) : false)
        );
      });
    },
    filteredActivities() {
      if (this.searchQuery && this.filterOrgModel) {
        if (this.filterOrgModel.key.startsWith("organization_")) {
          return this.filterBySearchAndOrg;
        } else if (this.filterOrgModel.key.startsWith("team_")) {
          return this.filterBySearchAndTeam;
        } else if (this.filterOrgModel.key == "all") {
          return this.filterBySearch;
        } else if (this.filterOrgModel.key == "mine") {
          return this.filterBySearchAndUser;
        }
      } else if (this.filterOrgModel) {
        if (this.filterOrgModel.key == "mine") {
          return this.filterByUser;
        } else if (this.filterOrgModel.key.startsWith("organization_")) {
          return this.filterByOrganization;
        } else if (this.filterOrgModel.key.startsWith("team_")) {
          return this.filterByTeam;
        }
      } else if (this.searchQuery) {
        return this.filterBySearch;
      }
      return this.activities;
    },
  },
  methods: {
    sortActivities() {
      let sortedActivities = [...this.filteredActivities];
      sortedActivities.sort((a, b) => {
        let first_record, second_record;
        switch (this.sortCategory) {
          case "created":
            first_record = a.created_at_ms ? a.created_at_ms : new Date(a.created_at);
            second_record = b.created_at_ms ? b.created_at_ms : new Date(b.created_at);
            if (!this.sortAsc) {
              return first_record - second_record;
            } else {
              return second_record - first_record;
            }
          case "updated":
            first_record = a.modified_at_ms;
            second_record = b.modified_at_ms;
            if (!this.sortAsc) {
              return first_record - second_record;
            } else {
              return second_record - first_record;
            }
          case "name":
            if (a.record) {
              first_record = a.record.name ? a.record.name.trim().toLowerCase() : "";
              second_record = b.record.name ? b.record.name.trim().toLowerCase() : "";
            } else {
              first_record = a.name ? a.name.trim().toLowerCase() : "";
              second_record = b.name ? b.name.trim().toLowerCase() : "";
            }

            if (!this.sortAsc) {
              return first_record.localeCompare(second_record);
            } else {
              return second_record.localeCompare(first_record);
            }
        }
      });
      this.sortedActivities = sortedActivities;
    },
  },
};
