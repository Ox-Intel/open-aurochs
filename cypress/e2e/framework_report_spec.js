var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("framework reports", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("lists the right reports", () => {
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
          weight: chance.integer({ min: 1, max: 10 }),
          score: chance.integer({ min: 1, max: 10 }),
          comment: chance.sentence({words: 5}),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
      })
    }

    cy.loginAsTestAdmin()

    // adds report
    cy.createReport(report_name)

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.goToItem(framework.name)

      // Make sure they're on the all scorecards page.
      cy.get("[data-cy=tab-reports]").click()
      cy.get("[data-cy=report-list] [data-cy=ox-object-report-0] [data-cy=item-name]").contains(report_name)
      cy.get("[data-cy=report-list] [data-cy=ox-object-report-0] [data-cy=item-name]").click()
      cy.get("[data-cy=report-list] [data-cy=ox-object-report-0]").should('not.exist')
      cy.get("[data-cy=report]").should('be.visible')
      cy.get("[data-cy=report] [data-cy=name").contains(report_name).should('be.visible')

    })
  })
  
})
