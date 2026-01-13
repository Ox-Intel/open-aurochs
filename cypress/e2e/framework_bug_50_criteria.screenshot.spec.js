
before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("frameworks with many, many criteria,", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("like 50 of them, should still work.", () => {
    var framework_name = "50 Criteria Framework"
    var criteria_list = []
    for (var i = 0; i <= 50; i++) {
      criteria_list.push({
        index: i,
        name: "Criteria " + i,
        // description: "D " + i,
        weight: i%10 + 1,
      })
    }
    cy.createFramework(framework_name)

    // adds criteria
    cy.addCriteriaToEmptyFramework(framework_name, criteria_list)

    // TODO: Add automated testing - right now we're just doing this visually.
    cy.get("[data-cy=framework] [data-cy=edit]").click()
    cy.get("[data-cy=framework] [data-cy=cancel]").click()
    cy.setDarkMode()
    cy.setLightMode()
    cy.get("html").click()
    cy.viewport(1280, 720)
    cy.get("html").matchImageSnapshot("50 criteria");
  })

})
