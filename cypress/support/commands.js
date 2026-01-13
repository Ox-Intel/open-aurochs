import { addMatchImageSnapshotCommand } from '@simonsmith/cypress-image-snapshot/command';

addMatchImageSnapshotCommand({
  failureThreshold: 0.05, // threshold for entire image
  failureThresholdType: 'percent', // percent of image or number of pixels
  customDiffConfig: { threshold: 0.1 }, // threshold for each pixel
  capture: 'viewport', // capture viewport in screenshot
  allowSizeMismatch: true,
});

function slugify(name) {
  return name.toLowerCase().replaceAll(' ', '_').replaceAll('"', "'")
}
function normalize_to_score_data_cy(score) {
  return String(Number(score).toFixed(1)).replace(".", "_")  
}

Cypress.Commands.add('createOrg', (orgName) => {
  cy.visit(Cypress.env("APP_URL") + "/administration/")
  cy.wait(250)
  cy.get("a[href='/administration/organizations/organization/add/']").click()
  cy.wait(250)
  cy.get("#id_name").type(orgName);
  cy.get("input[name='_save']").click()
  cy.visit(Cypress.env("APP_URL") + "/administration/")
  cy.wait(250)
});

Cypress.Commands.add('createUser', (username, password, suffix, name, email) => {
  if (!suffix) {
    suffix = ""
  }
  if (!name) {
    name = chance.name()
  }
  if (!email) {
    email = chance.email()
  }
  cy.visit(Cypress.env("APP_URL") + "/administration/organizations/user/add/")
  cy.wait(250)
  cy.get("#id_username").type(username);
  cy.get("#id_password1").type(password);
  cy.get("#id_password2").type(password);

  cy.get("input[name='_continue']").click()
  cy.get("#id_first_name").type(name.split(" ")[0] + suffix);
  cy.get("#id_last_name").type(name.split(" ")[1] + suffix);
  cy.get("#id_email").type(email + suffix);
  cy.get("input[name='_continue']").click()
  cy.visit(Cypress.env("APP_URL") + "/administration/")
  cy.wait(250)
});

Cypress.Commands.add('addUserToOrg', (orgName, username) => {
  let slug = slugify(orgName);
  cy.get("[data-cy=nav-user-menu]").click()
  cy.get("[data-cy=nav-teams]").click()
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=start-edit]`).click()
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=add-existing]`).click()
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=search–existing]`).clear().type(username)
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=possible-role-0]`).contains(username).should('exist')
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=possible-role-0]`).click()
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=save]`).click()
  cy.get(`[data-cy=orgs] [data-item-name=${slug}] [data-cy=save].saving`).should('not.exist')
  
});

Cypress.Commands.add('addUserToTeam', (teamName, username) => {
  let slug = slugify(teamName);
  cy.get("[data-cy=nav-user-menu]").click()
  cy.get("[data-cy=nav-teams]").click()
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=start-edit]`).click()
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=add-existing]`).click()
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=search–existing]`).clear().type(username)
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=possible-role-0]`).contains(username).should('exist')
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=possible-role-0]`).click()
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=save]`).click()
  cy.get(`[data-cy=teams] [data-item-name=${slug}] [data-cy=save].saving`).should('not.exist')
  
});

Cypress.Commands.add('deleteOrg', (orgName) => {
  cy.visit(Cypress.env("APP_URL") + "/administration/organizations/organization/")
  cy.wait(250)
  // cy.get("a[href='?all=']").click()
  cy.get("#changelist-search #searchbar").type(orgName)
  cy.get("#changelist-search input[type='submit']").click()
  cy.get("a").contains(orgName).click();
  cy.get(".deletelink").click();
  cy.get("input[type='submit']").should("have.value", "Yes, I’m sure").click()
});

Cypress.Commands.add('deleteUser', (username) => {
  cy.visit(Cypress.env("APP_URL") + "/administration/organizations/user/")
  cy.wait(250)
  // cy.get("a[href='?all=']").click()
  cy.get("#changelist-search #searchbar").type(username)
  cy.get("#changelist-search input[type='submit']").click()
  cy.get("a").contains(username).click();
  cy.get(".deletelink").click();
  cy.get("input[type='submit']").should("have.value", "Yes, I’m sure").click()
});


Cypress.Commands.add('loginAsSuperIfNeeded', () => {
  cy.get('body')
  .then(($body) => {
    cy.log($body.find('[data-cy="login-form"] #id_username').length)
    if ($body.find('[data-cy="login-form"] #id_username').length) {
      cy.loginAsSuper()
    }
  });
})
Cypress.Commands.add('login', (username, password) => {
    cy.visit(Cypress.env("APP_URL") + "/accounts/login/")
    cy.get("[data-cy='login-form'] #id_username").should("be.visible")
    cy.get("[data-cy='login-form'] #id_password").should("be.visible")
    cy.get("[data-cy='login-form'] #id_submit").should("be.visible")
    cy.get("[data-cy='login-form'] #id_username").focus().type(username)
    cy.get("[data-cy='login-form'] #id_password").focus().type(password).blur()

    cy.intercept('POST', Cypress.env("APP_URL") + '/accounts/login/').as('logIn')
    cy.get("[data-cy='login-form']").should("exist")
    cy.get("[data-cy='login-form'] #id_submit").click()
    cy.wait(25)
    cy.wait("@logIn")
    cy.get("[data-cy='login-form']").should("not.exist")
    cy.get("[data-cy='dashboard']").should("be.visible")

});

Cypress.Commands.add('loginAsTestUser', (suffix) => {
  if (!suffix) {
    suffix = ""
  }
  cy.get("@orgNormalUsername" + suffix).then(username=> {
    cy.get("@orgNormalPassword" + suffix).then(password=> {
      cy.login(username, password)
    })
  })
});

Cypress.Commands.add('loginAsTestAdmin', (suffix) => {
  if (!suffix) {
    suffix = ""
  }
  cy.log("Suffix: " + suffix + ".")
  cy.get("@orgAdminUsername" + suffix).then(username=> {
    cy.get("@orgAdminPassword" + suffix).then(password=> {
      cy.login(username, password)
    })
  })
});

Cypress.Commands.add('setupTestOrgAndUsers', (suffix) => {
  cy.on('uncaught:exception', (err, runnable) => {

    return false
  })
  if (!suffix) {
    suffix = ""
  }
  // Create an org user and admin
  cy.clearCookies()
  cy.clearLocalStorage()
  cy.viewport("macbook-13")
  cy.loginAsSuper()

  var namesuffix = (suffix == "") ? "" : "-" + suffix;
  var orgAdminUsername = chance.word({syllables: 3}) + namesuffix;
  cy.wrap(orgAdminUsername).as("orgAdminUsername" + suffix);
  var orgAdminPassword = chance.word({syllables: 3});
  cy.wrap(orgAdminPassword).as("orgAdminPassword" + suffix);
  var orgNormalUsername = chance.word({syllables: 3}) + namesuffix;
  cy.wrap(orgNormalUsername).as("orgNormalUsername" + suffix);
  var orgNormalPassword = chance.word({syllables: 3});
  cy.wrap(orgNormalPassword).as("orgNormalPassword" + suffix);
  
  var orgAdminName = chance.name()
  cy.wrap(orgAdminName).as("orgAdminName" + suffix);
  var orgNormalName = chance.name()
  cy.wrap(orgNormalName).as("orgNormalName" + suffix);

  var adminEmail = chance.email()
  cy.wrap(adminEmail).as("orgAdminEmail" + suffix);
  var normalEmail = chance.email()
  cy.wrap(normalEmail).as("orgNormalEmail" + suffix);

  var orgName = "e2eOrg - " + chance.word({syllables: 3}) + namesuffix;
  cy.wrap(orgName).as("orgName" + suffix);

  cy.createOrg(orgName)
  
  cy.createUser(orgAdminUsername, orgAdminPassword, suffix, orgAdminName, adminEmail)
  cy.createUser(orgNormalUsername, orgNormalPassword, suffix, orgNormalName, normalEmail)
  
  cy.addAdminUserToOrg(orgName, orgAdminUsername)
  cy.get("#logout-form button").click()

  cy.loginAsTestAdmin(suffix)
  cy.addUserToOrg(orgName, orgNormalUsername)
  cy.logOut()

  
  cy.visit(Cypress.env("APP_URL"))
  cy.wait(250)
})
Cypress.Commands.add('ensureOrgAndUsers', (context, suffix) => {
  if (!suffix) {
    suffix = ""
  }
  cy.wrap(context['orgNormalUsername' + suffix]).as("orgNormalUsername" + suffix)
  cy.wrap(context['orgNormalPassword' + suffix]).as("orgNormalPassword" + suffix)
  cy.wrap(context['orgNormalName' + suffix]).as("orgNormalName" + suffix)
  cy.wrap(context['orgNormalEmail' + suffix]).as("orgNormalEmail" + suffix)
  cy.wrap(context['orgAdminUsername' + suffix]).as("orgAdminUsername" + suffix)
  cy.wrap(context['orgAdminPassword' + suffix]).as("orgAdminPassword" + suffix)
  cy.wrap(context['orgAdminName' + suffix]).as("orgAdminName" + suffix)
  cy.wrap(context['orgAdminEmail' + suffix]).as("orgAdminEmail" + suffix)
  cy.wrap(context['orgName' + suffix]).as("orgName" + suffix)

})
Cypress.Commands.add('addAdminUserToOrg', (orgName, username) => {
  // cy.intercept(Cypress.env("APP_URL") + '/static/admin/js/inlines.js').as('adminJs')
  cy.visit(Cypress.env("APP_URL") + "/administration/organizations/organization/")
  
  // cy.wait('@adminJs')
  cy.wait(500)
  // cy.get("a[href='?all=']").click()
  cy.get("a").contains(orgName).click();
  cy.get("#organization_form .form-row:not(.empty-form) select[id^=id_organizationrole_set-][id$=-user]").last().select(username);
  cy.get("#organization_form .form-row:not(.empty-form) input[id^=id_organizationrole_set-][id$='-can_view']").last().check();
  cy.get("#organization_form .form-row:not(.empty-form) input[id^=id_organizationrole_set-][id$='-can_manage']").last().check();
  cy.get("input[name='_save']").click()
});
Cypress.Commands.add('setDarkMode', () => {
  // cy.get('html').should('have.attr', 'data-theme').then((theme) => {
  //   if (theme == "light") {
      cy.get("[data-cy=nav-user-menu]").click()
      cy.get("[data-cy=nav-toggle-mode]").click()
    // }
    cy.get("html[data-theme=dark]").should("exist")
  // })
});
Cypress.Commands.add('setLightMode', () => {
  // cy.get('html').should('have.attr', 'data-theme').then((theme) => {
  //   if (theme == "dark") {
      cy.get("[data-cy=nav-user-menu]").click()
      cy.get("[data-cy=nav-toggle-mode]").click()
      cy.get("[data-cy=nav-toggle-mode]").click()
    // }
    cy.get("html[data-theme=light]").should("exist")
  // })
});
Cypress.Commands.add('tearDownTestOrg', (suffix) => {
  // cy.on('uncaught:exception', (err, runnable) => {
  //   return false
  // })
  // try {
  //   if (!suffix) {
  //     suffix = ""
  //   }
    
  //   cy.visit(Cypress.env("APP_URL") + "/accounts/logout/")
  //   cy.wait(250)
  //   cy.visit(Cypress.env("APP_URL") + "/administration/logout/")
  //   cy.wait(250)
  //   cy.clearCookies()
  //   cy.clearLocalStorage()
  //   // cy.get("a[href='?all=']").click()
    
  //   // Log in as the test admin
  //   cy.loginAsTestAdmin(suffix)

  //   // Clear the library
  //   cy.clearLibrary()

  //   // Log in as test superuser
  //   cy.logOut()
  //   cy.loginAsSuper()

  //   // Delete the org & test users
  //   cy.get('@orgAdminUsername' + suffix).then(adminUsername => {
  //     cy.get('@orgNormalUsername' + suffix).then(normalUsername => {
  //       cy.get('@orgName' + suffix).then(orgName => {
  //         cy.deleteUser(adminUsername);
  //         cy.deleteUser(normalUsername);
  //         cy.deleteOrg(orgName);
  //       })
  //     })
  //   })

  //   cy.get("#logout-form button").click()
  // } catch {
  //   // If we fail here, don't fail the tests.  There are some flaky parts in the admin.
  // }

})

Cypress.Commands.add("loginAsSuper", (org_num) => {
  org_num = org_num ? org_num : ""
  cy.visit(Cypress.env("APP_URL") + "/administration/login/")
  cy.wait(250)
  cy.get("input[name=username]").should("be.visible")
  cy.get("input[name=password]").should("be.visible")
  cy.get("input[type='submit']").should("be.visible")

  // Fill in valid username and pass, then submit.
  cy.get("input[name=username]").type("test-super")
  cy.get("input[name=password]").type("0x1ntelEnter")
  cy.get("input[type='submit']").click()
  cy.get("input[type='submit']").should("not.exist")
});

Cypress.Commands.add("loginAsAdmin", (org_num) => {
  org_num = org_num ? org_num : ""
  cy.login("cust-admin" + org_num, "0x1ntelEnter")
  
});

Cypress.Commands.add("loginAsUser", (org_num) => {
  org_num = org_num ? org_num : ""
  cy.login("cust-user" + org_num, "0x1ntelEnter")
});

Cypress.Commands.add("logOut", () => {
  // Log out.
  cy.get("[data-cy=nav-user-menu]").should("be.visible")
  cy.get("[data-cy=nav-user-menu]").click()
  cy.get("[data-cy=nav-logout]").click()
  cy.get("[data-cy=nav-user-menu]").should('not.exist')
});

Cypress.Commands.add("ensureReportIsVisible", (report_name) => {
  cy.get("[data-cy=nav-library]").click()
  cy.get("[data-cy=library]").contains(report_name).should("exist")
});

Cypress.Commands.add("ensureReportIsNotVisible", (report_name) => {
  report_name = report_name + "--" + Cypress.env("run_prefix")
  cy.goToLibrary()
  cy.get("[data-cy=library]").should("not.contain", report_name)
});

Cypress.Commands.add("goToLibrary", () => {
  cy.get("[data-cy=nav-library]").click()
  cy.get("[data-cy=library]").should("be.visible")
});

Cypress.Commands.add("addPermissionsAdmin", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  // cy.get("[data-cy=permissions] [data-cy=can-read]:last").click()
  // cy.get("[data-cy=permissions] [data-cy=can-write]:last").click()
  cy.get("[data-cy=permissions] [data-cy=can-admin]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsReadNoScore", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  // We default to read and score permissions
  // cy.get("[data-cy=permissions] [data-cy=can-read]:last").click()
  cy.get("[data-cy=permissions] [data-cy=can-score]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsReadOnly", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  // We default to read and score permissions
  // cy.get("[data-cy=permissions] [data-cy=can-read]:last").click()
  // cy.get("[data-cy=permissions] [data-cy=can-score]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsScoreOnly", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  // cy.get("[data-cy=permissions] [data-cy=can-score]:last").click()
  cy.get("[data-cy=permissions] [data-cy=can-read]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsReadWrite", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  // cy.get("[data-cy=permissions] [data-cy=can-read]:last").click()
  cy.get("[data-cy=permissions] [data-cy=can-write]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsWrite", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  cy.get("[data-cy=permissions] [data-cy=can-write]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("addPermissionsAdmin", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=add-another]").click();
  cy.get("[data-cy=permissions] [data-cy=search-roles]").type(role_name);
  cy.get("[data-cy=permissions] [data-cy=potential-roles] [data-cy=role]:first").click()
  cy.get("[data-cy=permissions] [data-cy=can-admin]:last").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});
Cypress.Commands.add("removeRoleFromPermissions", (role_name) => {
  let slug = slugify(role_name)
  cy.get("[data-cy=tab-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
  cy.get(`[data-cy=permissions] [data-cy=role-${slug}] [data-cy=remove-role]`).click();
  cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
  cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')
});

Cypress.Commands.add("createTeam", (team_name) => {
  cy.get("[data-cy=nav-user-menu]").click()
  cy.get("[data-cy=nav-teams]").click()
  cy.get("[data-cy=teams]").should("be.visible")
  cy.get("[data-cy=create-team]").click()

  // For when we allow multiple orgs
  // cy.get("[data-cy=team-org-search] [data-cy=searchbox-search").type(team_name)
  // cy.get("[data-cy=team-org-search] ul li").contains(team_name).click()
  // cy.get("[data-cy=finish-create-team]").click()
  // cy.get("[data-cy=finish-create-team].saving").should('not.exist')

  cy.get(`[data-cy=teams] [data-item-name=new_team] [data-cy=start-edit]`).click()
  cy.get(`[data-cy=teams] [data-item-name=new_team] [data-cy=team-name-input]`).clear().type(team_name)
  cy.get(`[data-cy=teams] [data-item-name=new_team] [data-cy=save]`).click()
  cy.get(`[data-cy=teams] [data-item-name=new_team] [data-cy=save].saving`).should("not.exist")
});

Cypress.Commands.add("createFramework", (framework_name, team_name) => {
  // Start from the library page, and add a report to a framework.
  cy.goToLibrary()
  framework_name = framework_name
    ? framework_name
    : chance.sentence({ words: 5 });

  cy.get("div").should("not.contain", )
  // Make a new framework
  cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
  // This won't be visible because cypress doesn't have a way to trigger hover.
  cy.get("[data-cy=nav-new-framework]").click({'force': true})
  
  cy.get("[data-cy=input-framework-name]").clear().type(framework_name)

  cy.get("[data-cy=framework] [data-cy=save]").click()
  cy.get("[data-cy=framework] [data-cy=save].saving").should('not.exist')

  if (team_name != undefined) {
    cy.addPermissionsAdmin(team_name)
  }

  // Make sure it's there.
  cy.goToLibrary()
  cy.get("[data-cy=library-feed-item]")
    .contains(framework_name)
    .should("exist")
});

Cypress.Commands.add(
  "addReportToFramework",
  (report_name, framework_name, team_name) => {
    // Start from the library page, and add a report to a framework.
    report_name = report_name ? report_name : chance.sentence({ words: 5 })
    cy.addScorecards(report_name, framework_name, [])
  }
)
// Add a source
Cypress.Commands.add("createSource", (source_name, team_name, subtitle) => {
  // Start from the library page, and add a source.
  source_name = source_name
    ? source_name
    : chance.sentence({ words: 5 });

  subtitle = subtitle
    ? subtitle
    : chance.sentence({ words: 5 });

  // Make a new source
  cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
  // This won't be visible because cypress doesn't have a way to trigger hover.
  cy.get("[data-cy=nav-new-source]").click({'force': true})
  
  cy.get("[data-cy=input-source-name]").clear()
  cy.wait(5)
  cy.get("[data-cy=input-source-name]").type(source_name)
  cy.get("[data-cy=input-source-subtitle]").clear()
  cy.wait(5)
  cy.get("[data-cy=input-source-subtitle]").type(subtitle)

  cy.get("[data-cy=source] [data-cy=save]").click()
  cy.get("[data-cy=source] [data-cy=save].saving").should('not.exist')
  if (team_name) {
    cy.addPermissionsAdmin(team_name)
  }
  // Make sure it's there.
  cy.goToLibrary()
  cy.get("[data-cy=library-feed-item]")
    .contains(source_name)
    .should("exist")
})
// Add a report
Cypress.Commands.add("createReport", (report_name, team_name) => {
  // Start from the library page, and add a report.
  report_name = report_name
    ? report_name
    : chance.sentence({ words: 5 });

  // Make a new report
  cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
  // This won't be visible because cypress doesn't have a way to trigger hover.
  cy.get("[data-cy=nav-new-report]").click({'force': true})
  
  cy.get("[data-cy=input-report-name]").clear().type(report_name)

  cy.get("[data-cy=report] [data-cy=save]").click()
  cy.get("[data-cy=report] [data-cy=save].saving").should('not.exist')

  if (team_name) {
    cy.addPermissionsAdmin(team_name)
  }
  // Make sure it's there.
  cy.goToLibrary()
  cy.get("[data-cy=library-feed-item]")
    .contains(report_name)
    .should("exist")
})

// Add a stack
Cypress.Commands.add("createStack", (stack_name, team_name) => {
  // Start from the library page, and add a stack.
  stack_name = stack_name
    ? stack_name
    : chance.sentence({ words: 5 });

  // Make a new stack
  cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
  // This won't be visible because cypress doesn't have a way to trigger hover.
  cy.get("[data-cy=nav-new-stack]").click({'force': true})
  
  cy.get("[data-cy=stack] [data-cy=save]").should('be.visible')
  cy.get("[data-cy=input-stack-name]").clear().type(stack_name)

  cy.get("[data-cy=stack] [data-cy=save]").click()
  cy.get("[data-cy=stack] [data-cy=save].saving").should('not.exist')

  if (team_name) {
    cy.addPermissionsAdmin(team_name)
  }
  // Make sure it's there.
  cy.goToLibrary()
  cy.get("[data-cy=library-feed-item]")
    .contains(stack_name)
    .should("exist")
})
Cypress.Commands.add("addReportToStack", (stack_name, report_name) => {
  cy.goToItem(stack_name);
  cy.get("[data-cy=add-report-to-stack]").click()
  cy.get("[data-cy=add-report-modal]")
  cy.get("[data-cy=add-report-modal] [data-cy=searchbox-search]").type(report_name)
  cy.get("[data-cy=add-report-modal] ul li").contains(report_name).click()
  cy.get("[data-cy=add-report-to-stack-from-modal]").click()
  cy.get("[data-cy=overview] [data-cy=name]").contains(report_name).should("exist")
});
Cypress.Commands.add("addStackToReport", (stack_name, report_name) => {
  cy.get("[data-cy=add-to-stack]").click()
  cy.get("[data-cy=add-stack-modal]")
  cy.get("[data-cy=add-stack-modal] [data-cy=searchbox-search]").type(stack_name)
  cy.get("[data-cy=add-stack-modal] ul li").contains(stack_name).click()
  cy.get("[data-cy=add-stack-to-report-from-modal]").click()
  cy.get("[data-cy=stack-badges] .stack-badge").contains(stack_name).should("exist")
});


Cypress.Commands.add("deleteObject", () => {
  cy.get("[data-cy=delete]").click()
  // Checks for window confirm:
  cy.on("window:confirm", () => true)
  cy.get("[data-cy=library]")
});


// From the library page, adds a team with a specific organization, then goes back to the library page.
Cypress.Commands.add(
  "addTeam",
  (team_lead, team_name, organization_name, description) => {
    // set description name if it comes in undefined
    if (description === undefined) {
      description = "description undefined"
    }

    cy.visit(Cypress.env("APP_URL") + "/administration")
    cy.wait(250)
    // cy.get("a[href='?all=']").click()

    cy.visit(Cypress.env("APP_URL") + "/administration/organizations/team/add/")
    cy.wait(600)
    cy.get("input[name=name]").should("exist").type(team_name)
    cy.get("textarea[name=description]").should("exist").type(description)

    cy.get("select[name=organization]")
      .should("exist")
      .select(organization_name)
    cy.get("select[name=teammember_set-0-user]").should("exist").select(team_lead)
    // cy.get("select[name=teammember_set-0-user] option[selected]").contains(team_lead).should("exist")

    cy.get("input[name=teammember_set-0-can_view]").click()
    cy.get("input[name=teammember_set-0-can_manage]").click()

    cy.get("input[name=_save]").click()

    cy.visit(Cypress.env("APP_URL") + "/library")
    cy.wait(250)
    // cy.get("a[href='?all=']").click()
  }
)
Cypress.Commands.add("changePassword", (new_password) => {
  // From dashboard, click on change password on user menu.
  cy.get("body").click()
  cy.get("[data-cy=nav-user-menu]").click()
  cy.get("[data-cy=nav-profile]").click()

  // Changes password.
  cy.get("div").contains("Update Password").should("exist")
  cy.get("input[id=newPassword]").type(new_password)
  cy.get("input[id=confirmPassword]").type(new_password)

  // Submit Button.
  cy.get("[data-cy=update-password-button]").click()

  // Click away from the user menu option
  cy.get("body").click(0, 0)
  cy.get("body").click(0, 0)
  cy.wait(500)
})
Cypress.Commands.add("goToItem", (search_term) => {
  cy.get("[data-cy=nav-search-box]").clear().type(search_term);
  cy.get("[data-cy=nav-search-results] li:first").click()
  cy.get("[data-cy=nav-search-results] li:first").should('not.exist')
});
Cypress.Commands.add("itemDoesNotExist", (search_term) => {
  cy.get("[data-cy=nav-search-box]").clear().type(search_term);
  cy.get("[data-cy=nav-search-results] li:first").should('not.exist')
});

Cypress.Commands.add(
  "cloneFramework",
  (original_framework_name, new_framework_name) => {
    cy.goToLibrary()
    cy.get(`[data-cy=my-library-list]`)
      .contains(original_framework_name)
      .click()

    cy.get(`[data-cy=clone-framework]`).click()
    if (new_framework_name) {
      cy.get("[data-cy=framework-name]").clear().type(new_framework_name)
    }
    cy.intercept('POST', Cypress.env("APP_URL") + '/event/').as('event')
    cy.get("[data-cy=save-clone]").click()
    cy.wait("@event")
    // cy.get("body").click(0, 0)
  }
)
Cypress.Commands.add(
  "addCriteriaToFramework",
  (framework_name, criteria_list) => {
    cy.goToLibrary()
    cy.get(`[data-cy=my-library-list]`).contains(framework_name).click()
    cy.get("[data-cy=edit-criteria]").click()
    for (var i = 0; i < criteria_list.length; i++) {
      cy.get("[data-cy=new-criteria]").click()
      cy.get(`[data-cy=name-edit-${i}]`)
        .find("input[name=name]")
        .type(criteria_list[i].name)
      cy.get(`[data-cy=description-edit-${i}] textarea`)
        .find("textarea[name=description]")
        .type(criteria_list[i].description)
      cy.get(`[data-cy=criteria-weight-${i}] input`).invoke('val', criteria_list[i].weight).trigger('change').click({force:true})
    }
    cy.get("div").contains("Save").click()

    for (var i = 0; i < criteria_list.length; i++) {
      cy.get("div").contains(criteria_list[i].name).should("exist")
      cy.get("div").contains(criteria_list[i].description).should("exist")
      cy.get(
  `div[data-cy=framework-criteria-card-${i}] [data-cy=weight]`)
        .find("div")
        .contains(criteria_list[i].weight)
        .should("exist")
    }
  }
)
Cypress.Commands.add(
  "addCriteriaToEmptyFramework",
  (framework_name, criteria_list) => {
    cy.goToLibrary()
    cy.get(`[data-cy=my-library-list]`).contains(framework_name).click()
    cy.get("[data-cy=add-criteria]").click()
    for (var i = 0; i < criteria_list.length; i++) {
      if (i != 0) {
        cy.get("[data-cy=new-criteria]").click()
      }
      cy.get(`[data-cy=name-edit-${i}]`)
        .type(criteria_list[i].name)
      if (criteria_list[i].description) {
        cy.get(`[data-cy=description-edit-${i}] textarea`)
          .type(criteria_list[i].description)
      }

      cy.get(`[data-cy=criteria-weight-${i}] input`).invoke('val', criteria_list[i].weight).trigger('change').click({force:true})
    }
    cy.get("[data-cy=save-criteria]").click()
    cy.get("[data-cy=save-criteria].saving").should('not.exist')

    for (var i = 0; i < criteria_list.length; i++) {
      cy.get(`[data-cy=framework-criteria-card-${i}] [data-cy=name]`).contains(criteria_list[i].name).should("exist")
      if (criteria_list[i].description) {
        cy.get(`[data-cy=framework-criteria-card-${i}] [data-cy=description]`).contains(criteria_list[i].description).should("exist")
      }
      cy.get(
        `div[data-cy=framework-criteria-card-${i}] [data-cy=weight]`)
        .contains(criteria_list[i].weight)
        .should("exist")
    }
  }
)
Cypress.Commands.add(
  "addScorecards",
  (report_name, framework_name, criteria_list) => {
    cy.goToItem(report_name)

    cy.get("[data-cy=add-scorecard]").click()
    cy.get("[data-cy=scorecard-framework-search] [data-cy=searchbox-search]").type(framework_name)
    cy.get("[data-cy=scorecard-framework-search] ul li").contains(framework_name).click()
    cy.get("[data-cy=add-scorecard-from-modal]").click()

    var count = 0;
    criteria_list.map((criteria, index) => {
      if (criteria.skipped) {
        cy.get(`[data-cy=scorecard-criteria-${count}] [data-cy=skip]`).click()
      } else {
        cy.get(`[data-cy=scorecard-criteria-slider-${count}] input`).invoke('val', criteria.score).trigger('change').click({force:true})
      }
      cy.get(`[data-cy=scorecard-criteria-comment-${count}] textarea`).clear().type(criteria.comment)

      count += 1;
    })
    cy.get("[data-cy='save-scorecard']").click()
    cy.get("[data-cy='save-scorecard'].saving").should('not.exist')
    criteria_list.map((criteria, index) => {
      if (criteria.skipped) {
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains("Skipped").should('exist')
      } else {
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score).should('exist')
      }
      cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment).should('exist')
    })

  }
)

Cypress.Commands.add(
  "editScorecards",
  (report_name, framework_name, criteria_list) => {
    cy.goToItem(report_name)
    cy.get("[data-cy=tab-scorecards]").click()
    cy.get("[data-cy=scorecards]:first [data-cy=toggle-open-expand]:first").click()
    cy.get("[data-cy=scorecards]:first [data-cy=view-scores]").should('exist')
    cy.get("[data-cy=scorecards]:first [data-cy=edit-scores]").should('not.exist')
    cy.get("[data-cy=edit-scorecard]:first").click()
    cy.get("[data-cy=scorecards]:first [data-cy=view-scores]").should('not.exist')
    cy.get("[data-cy=scorecards]:first [data-cy=edit-scores]").should('exist')

    var count = 0;
    criteria_list.map((criteria, index) => {
      if (criteria.skipped) {
        cy.get(`[data-cy=scorecard-criteria-${count}] [data-cy=skip]`).click()
      } else {
        cy.get(`[data-cy=scorecard-criteria-slider-${count}] input`).invoke('val', criteria.score).trigger('change').click({force:true})
      }
      cy.get(`[data-cy=scorecard-criteria-comment-${count}] textarea`).clear().type(criteria.comment)
      count += 1;
    })

    cy.get("[data-cy='save-scorecard']").click()
    cy.get("[data-cy='save-scorecard'].saving").should('not.exist')
    criteria_list.map((criteria, index) => {
      cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score).should('exist')
      cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment).should('exist')
    })
  }
)

Cypress.Commands.add("addTags", (data_name, tag_names) => {
  cy.goToLibrary()
  cy.get("[data-cy=item-name]").contains(data_name).should("exist").click()

  // loop through list of tags and add them all
  cy.get("[data-cy=add-tag]").should("exist").click()
  for (var i = 0; i < tag_names.length; i++) {
    // cy.get(".tags .tag").should("not.contain", )
    cy.get("[data-cy=tag-search]").click().type(tag_names[i]).type("{enter}")
    cy.wait(500)
    cy.get(".tags .tag [data-cy=tag-name]").contains(tag_names[i]).should("exist")
  }
  cy.get("body").click(0, 0)
})

Cypress.Commands.add("removeTags", (data_name, tag_names) => {
  cy.goToLibrary()
  cy.get("[data-cy=item-name]").contains(data_name).should("exist").click()

  // loop through and remove selected
  for (var i = 0; i < tag_names.length; i++) {
    cy.get(".tags .tag [data-cy=tag-name]")
      .contains(`${tag_names[i]}`)
      .next("[data-cy=delete-tag]")
      .should("exist")
      .click()

    // this is needed for data to come through from the API and populate the app
    cy.wait(1000)

    // check that tagas have been deleted
    cy.get("span").should("not.contain", )
  }
})
Cypress.Commands.add("addSourceToReport", (report_name, source_name) => {
  cy.goToItem(report_name)
  cy.get("[data-cy=tab-sources]").click()
  cy.get("[data-cy=source-list]").contains(source_name).should('not.exist')
  cy.get("[data-cy=add-source]").click()
  cy.get("[data-cy=add-source-modal] [data-cy=searchbox-search]").clear().type(source_name)
  cy.get("[data-cy=add-source-modal] [data-cy=searchbox-option-0]").contains(source_name).click()
  cy.get("[data-cy=add-source-modal] [data-cy=add-source-button]").click()
  cy.get("[data-cy=add-source-modal] [data-cy=add-source-button].saving").should('not.exist')
  cy.get("[data-cy=source-list] [data-cy=name]").contains(source_name).should('exist')
})

Cypress.Commands.add("goToDashboard", () => {
  cy.get("[data-cy=nav-dashboard]").click()
  cy.get("[data-cy=dashboard]").should("be.visible")
  cy.get("[data-cy=framework-title]").should("be.visible")
  
})

Cypress.Commands.add("addComment", (comment) => {
  cy.get("[data-cy=new-comment] textarea").clear().type(comment)
  cy.get("[data-cy=save-comment]").click()
  cy.get("[data-cy=save-comment].saving").should("not.exist")
  cy.get("[data-cy=comment] [data-cy=body]").contains(comment).should("exist")

})
Cypress.Commands.add("editComment", (comment) => {
  cy.get("[data-cy=edit-comment]").click()
  cy.get("[data-cy=comment] textarea:first").clear().type(comment)
  cy.get("[data-cy=save-comment]:first").click()
  cy.get("[data-cy=save-comment]:first.saving").should("not.exist")
  cy.get("[data-cy=comment] [data-cy=body]").contains(comment).should("exist")
})
Cypress.Commands.add("addNotes", (comment) => {
  cy.get("[data-cy=add-notes]").click()
  cy.get("[data-cy=editing-notes] .ql-editor:first").clear().type(comment)
  cy.get("[data-cy=save-comment]:first").click()
  cy.get("[data-cy=save-comment]:first.saving").should("not.exist")
  cy.get("[data-cy=view-notes]").contains(comment).should("exist")
})
Cypress.Commands.add("editNotes", (comment) => {
  cy.get("[data-cy=edit-notes]").click()
  cy.get("[data-cy=editing-notes] .ql-editor:first").clear().type(comment)
  cy.get("[data-cy=save-comment]:first").click()
  cy.get("[data-cy=save-comment]:first.saving").should("not.exist")
  cy.get("[data-cy=view-notes]").contains(comment).should("exist")
})
Cypress.Commands.add("followDiscussion", (comment) => {
  cy.get("[data-cy=discussion] [data-cy=follow]").click()
  cy.get("[data-cy=discussion] [data-cy=follow]").should("not.exist")
  cy.get("[data-cy=discussion] [data-cy=unfollow]").should("exist")
})
Cypress.Commands.add("unfollowDiscussion", (comment) => {
  cy.get("[data-cy=discussion] [data-cy=unfollow]").click()
  cy.get("[data-cy=discussion] [data-cy=unfollow]").should("not.exist")
  cy.get("[data-cy=discussion] [data-cy=follow]").should("exist")
})

Cypress.Commands.add("endOfTestWait", () => {
  cy.wait(2000)
})

Cypress.Commands.add("clearLibrary", () => {
  var f = 0
  cy.goToLibrary()
  cy.get(`[data-cy=my-library-list]`)
    .then(($list) => {
      if ($list.find(`[data-cy=framework-list-item]`).length) {
        $list.find(`[data-cy=framework-list-item]`)
          .each((item) => {
            f = item.length
            while (f > 0) {
              cy.get("[data-cy=framework-list-item]:nth-child(1)").click()
              cy.get(`div[data-cy=framework-details-menu-button]`).click()
              cy.get("div").contains(`Delete Framework`).click()
              cy.on("window:alert", (txt) => {
                expect(txt).to.contains(
                  "Are you sure you want to delete this framework?"
                )
              })
              f -= 1
            }
          })
        }
      });


  var r = 0
  cy.goToLibrary()
  cy.get(`[data-cy=report-list]`)
    .then(($list) => {
      if ($list.find(`[data-cy=report-list-item]`).length) {
        $list.find(`[data-cy=report-list-item]`)
          .each((item) => {
            r = item.length
            while (r > 0) {
              cy.get("[data-cy=report-list-item]:nth-child(1)").click()
              cy.get(`div[data-cy=report-details-menu-button]`).click()
              cy.get("div").contains(`Delete Report`).click()
              cy.on("window:alert", (txt) => {
                expect(txt).to.contains(
                  "Are you sure you want to delete this report?"
                )
              })
              r -= 1
            }
          })
        }
      })


  var s = 0
  cy.goToLibrary()
  cy.get(`[data-cy=source-list]`)
    .then(($list) => {
      if ($list.find(`[data-cy=source-list-item]`).length) {
        $list.find(`[data-cy=source-list-item]`)
          .each((item) => {
            s = item.length
            while (s > 0) {
              cy.get("[data-cy=source-list-item]:nth-child(1)").click()
              cy.get(`div[data-cy=source-details-menu-button]`).click()
              cy.get("div").contains(`Delete Source`).click()
              cy.on("window:alert", (txt) => {
                expect(txt).to.contains(
                  "Are you sure you want to delete this source?"
                )
              })
              s -= 1
            }
          })
        }
      })
  });
