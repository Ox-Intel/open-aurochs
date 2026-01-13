var reports = []
for (var j = 0; j < 2; j++) {
  reports.push("R" + j + "--" + chance.hash())
}
before(() => {
  cy.setupTestOrgAndUsers()
  cy.loginAsTestUser()
  cy.get("@orgName").then(orgName=> {
    var framework_name = chance.sentence({ words: 2 })
    cy.createFramework(framework_name, orgName)

    // Add a report
    for (var j = 0; j < reports.length; j++) {
      cy.createReport(reports[j], orgName);
      cy.addScorecards(
        reports[j],
        framework_name,
        []
      )
    }
  });
  cy.logOut();
});
after(() => {
  cy.tearDownTestOrg()
});

describe("Confirm report listing", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    cy.logOut()
  });

  it("normal user should see their appropriate reports.", () => {
    cy.loginAsTestUser()
    for (var j = 0; j < reports.length; j++) {
      cy.ensureReportIsVisible(reports[j])
    }
  })
  it("admin user should see the appropriate reports.", () => {
    cy.loginAsTestAdmin()
    for (var j = 0; j < reports.length; j++) {
      cy.ensureReportIsVisible(reports[j])
    }
  })

})
