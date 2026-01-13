
before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("frameworks", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it(" with criteria that all have the same name.", () => {
    var framework_name = "Identical Criteria"
    var criteria_list = []
    for (var i = 0; i < 20; i++) {
      criteria_list.push({
        index: i,
        name: "Same",
        // description: "D " + i,
        weight: i%10 + 1,
      })
    }
    cy.createFramework(framework_name)

    // adds criteria
    cy.addCriteriaToEmptyFramework(framework_name, criteria_list)
    cy.setDarkMode()
    cy.setLightMode()
    cy.get("html").click()
    cy.viewport(1280, 720)
    cy.get("html").matchImageSnapshot("Same Name Criteria");

  })
})
