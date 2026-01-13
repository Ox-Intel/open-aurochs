before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("Clone framework function should create a clone of a given framework", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  
  it("cloned framework should have the same criteria and weights with no associate reports", () => {

    // Create a framework that has to be cloned:
    var original_framework_name = chance.hash()
    var report_name = chance.hash()
    var num_criteria = 2
    var criteria_list = []
    var new_framework_name = "New Framework " + chance.sentence();

    for (var i = 0; i < num_criteria; i++) {
      criteria_list.push({
        name: chance.hash(),
        description: chance.hash(),
        weight: chance.integer({ min: 1, max: 10 }),
      })
    }

    // Add data
    cy.createFramework(original_framework_name)
    cy.addCriteriaToEmptyFramework(original_framework_name, criteria_list)
    cy.createReport(report_name)
    cy.addScorecards(report_name, original_framework_name, [])
    cy.goToItem(original_framework_name)
    cy.cloneFramework(original_framework_name, new_framework_name)

    // Check that default text with the new framework is, "Copy of ${name}"
    cy.get("[data-cy=nav-library]").click()
    cy.get("[data-cy='library-feed-item']").contains(new_framework_name).should("be.visible")
    cy.get("[data-cy='library-feed-item']").contains(new_framework_name).click()


    // Check that the new criteria got ported over to the cloned framework
    for (var i = 0; i < criteria_list.length; i++) {
      cy.get("div").contains(criteria_list[i].name).should("be.visible")
      cy.get("div").contains(criteria_list[i].description).should("be.visible")
      cy.get(`div[data-cy=framework-criteria-card-${i}`)
        .find("div")
        .contains(criteria_list[i].weight)
        .should("be.visible")
    }

    // Check that the new cloned framework has no associated reports
    cy.get("[data-cy=tab-reports]").click()
    cy.get("div").should("not.contain", )
  })
})
