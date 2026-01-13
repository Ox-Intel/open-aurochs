var num_criteria = 2
var num_framework = 1

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("Scorecards that I don't have permissions for:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("should not be shown.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
      var framework_list = []
      var word = chance.word()
      var report_name = "Report 1" + word

      for (var i = 0; i < num_framework; i++) {
        // Generate criteria list for each framework
        var criteria_list = []
        var new_criteria_list = []
        for (var j = 0; j < num_criteria; j++) {
          criteria_list.push({
            name: `criteria-${j}-${word}`,
            description: "description",
            weight: 10-j,
            score: 10-j,
            comment: chance.sentence({words: 5}),
          })
        }

        framework_list.push({
          name: `framework-${i}-${word}`,
          criteria: criteria_list,
        })
      }


      // adds report
      cy.createReport(report_name)
      cy.goToItem(report_name)
      cy.addPermissionsScoreOnly(name)

      // creates frameworks from a list of frameworks with criteria and adds
      // them to the report
      framework_list.map((framework) => {
        cy.createFramework(framework.name)
        cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
        cy.goToItem(report_name)
        cy.addScorecards(report_name, framework.name, framework.criteria)
      })

      // I should see the scores
      cy.goToItem(report_name)
      cy.get("[data-cy=report] [data-cy=no-scorecards]").should("not.exist")
      cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
      cy.get("[data-cy=report] [data-cy=hidden-scorecards]").should("not.exist")

      cy.logOut()
      cy.loginAsTestAdmin()

      cy.goToItem(report_name)
      cy.get("[data-cy=report] [data-cy=no-scorecards]").should("be.visible")
      cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
      cy.get("[data-cy=report] [data-cy=hidden-scorecards]").should("be.visible")

      // Make sure it also works when admin has frameworks
      cy.createFramework(chance.word())
      cy.goToItem(report_name)
      cy.get("[data-cy=report] [data-cy=no-scorecards]").should("be.visible")
      cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
      cy.get("[data-cy=report] [data-cy=hidden-scorecards]").should("be.visible")

      })
    })
  })

})
