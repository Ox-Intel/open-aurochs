before(() => {
  cy.setupTestOrgAndUsers()
  cy.get("@orgName").then(organization_name=> {
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()

    var framework_name = chance.sentence({ words: 2 })
    cy.createFramework(framework_name, organization_name)

    // Add a report
    cy.createReport("R1")
    cy.addScorecards("R1", framework_name, [])
    cy.createReport("R2", organization_name)
    cy.addScorecards("R2", framework_name, [])
    cy.logOut()
    cy.loginAsTestAdmin()
    cy.createReport("R3")
    cy.addScorecards("R3", framework_name, [])
    cy.createReport("R4", organization_name)
    cy.addScorecards("R4", framework_name, [])
    cy.logOut()
  });
  cy.setupTestOrgAndUsers("2")
});
after(() => {
  cy.tearDownTestOrg()
  cy.tearDownTestOrg("2")
});

describe("Org admin report list bug fixed by user orgs:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.ensureOrgAndUsers(this, "2")
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("Org 1 normal user should see the appropriate reports.", () => {
    // user should see:
    // R1, R2, R4
    cy.loginAsTestUser()
    cy.ensureReportIsVisible("R1")
    cy.ensureReportIsVisible("R2")
    cy.ensureReportIsVisible("R4")
    cy.ensureReportIsNotVisible("R3")
    cy.logOut()
  })
  it("Org 1 admin user should see the appropriate reports.", () => {
    // admin should see:3
    //  R2, R3, R4
    cy.loginAsTestAdmin()
    cy.ensureReportIsVisible("R2")
    cy.ensureReportIsVisible("R3")
    cy.ensureReportIsVisible("R4")
    cy.ensureReportIsNotVisible("R1")
    cy.logOut()
  })
  it("Org 2 normal user should see no reports.", () => {
    // user should not see:
    // R1, R2, R3, R4
    cy.loginAsTestUser("2")
    cy.ensureReportIsNotVisible("R1")
    cy.ensureReportIsNotVisible("R2")
    cy.ensureReportIsNotVisible("R3")
    cy.ensureReportIsNotVisible("R4")
    cy.logOut()
  })
  it("Org 2 admin user should see no reports.", () => {
    // admin should not see:
    //  R1, R2, R3, R4
    cy.loginAsTestAdmin("2")
    cy.ensureReportIsNotVisible("R1")
    cy.ensureReportIsNotVisible("R2")
    cy.ensureReportIsNotVisible("R3")
    cy.ensureReportIsNotVisible("R4")
    cy.logOut()
  })
})
