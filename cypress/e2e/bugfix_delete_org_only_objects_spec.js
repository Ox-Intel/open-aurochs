var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("deleting ", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("org-only reports works", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        var word = chance.word()
        var report_name = "Report " + word

        cy.loginAsTestAdmin()

        // adds report
        cy.createReport(report_name)
        cy.goToItem(report_name)
        cy.addPermissionsAdmin(orgName)
        cy.removeRoleFromPermissions(name)

        cy.goToItem(report_name)
        cy.deleteObject()
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        cy.visit(Cypress.env("APP_URL"))
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        
        // cy.get("[data-cy=item-name]").contains(report_name).should("not.exist");
      })
    })
  })
  it("org-only frameworks works", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        var word = chance.word()
        var framework_name = "framework " + word

        cy.loginAsTestAdmin()

        // adds framework
        cy.createFramework(framework_name)
        cy.goToItem(framework_name)
        cy.addPermissionsAdmin(orgName)
        cy.removeRoleFromPermissions(name)

        cy.goToItem(framework_name)
        cy.deleteObject()
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        cy.visit(Cypress.env("APP_URL"))
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        
        // cy.get("[data-cy=item-name]").contains(framework_name).should("not.exist");
      })
    })
  })
  it("team-only reports works", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        var word = chance.word()
        var report_name = "Report " + word
        var team_name = "Team " + word

        cy.loginAsTestAdmin()

        // adds report
        cy.createTeam(team_name,)
        // Creating a team adds you to it by default.
        // cy.addUserToTeam(team_name, name,)

        cy.createReport(report_name)
        cy.goToItem(report_name)
        cy.addPermissionsAdmin(team_name)
        cy.removeRoleFromPermissions(name)

        cy.goToItem(report_name)
        cy.deleteObject()
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        cy.visit(Cypress.env("APP_URL"))
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        
        // cy.get("[data-cy=item-name]").contains(report_name).should("not.exist");
      })
    })
  })
  it("team-only frameworks works", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        var word = chance.word()
        var framework_name = "framework " + word
        var team_name = "Team " + word

        cy.loginAsTestAdmin()

        // adds framework
        cy.createTeam(team_name,)
        // Creating a team adds you to it by default.
        // cy.addUserToTeam(team_name, name,)
        cy.createFramework(framework_name)
        cy.goToItem(framework_name)
        cy.addPermissionsAdmin(team_name)
        cy.removeRoleFromPermissions(name)

        cy.goToItem(framework_name)
        cy.deleteObject()
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        cy.visit(Cypress.env("APP_URL"))
        cy.goToLibrary()
        cy.get("[data-cy=item-name]").should("not.exist");

        
        // cy.get("[data-cy=item-name]").contains(framework_name).should("not.exist");
      })
    })
  })
})


