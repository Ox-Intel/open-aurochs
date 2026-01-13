var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

function normalize_to_score_data_cy(score) {
  return String(Number(score).toFixed(1)).replace(".", "_")  
}
function ensureCommentsAreAllThere(cy, framework) {
  framework.criteria.map((criteria, index) => {
    cy.get(`[data-cy=criteria-${index}] [data-cy=comment]`).should('not.exist')
    cy.get(`[data-cy=criteria-comments-${index}-0]`).should('not.exist')
    cy.get(`[data-cy=criteria-${index}] [data-cy=dot-plot]`).click()
    cy.get(`[data-cy=criteria-comments-${index}-0] [data-cy=comment]`).contains(criteria.comment).should('be.visible')
  })
  // Toggle all open
  cy.get("[data-cy=toggle-all-comments]").click()
  framework.criteria.map((criteria, index) => {
    cy.get(`[data-cy=criteria-comments-${index}-0] [data-cy=comment]`).contains(criteria.comment).should('exist')
  })
  // Toggle all closed
  cy.get("[data-cy=toggle-all-comments]").click()
  framework.criteria.map((criteria, index) => {
    cy.get(`[data-cy=criteria-${index}] [data-cy=comment]`).should('not.exist')
  })

}


describe("score comments ", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it(" show on the overview page", () => {
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
        new_criteria: new_criteria_list
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
      

      // Make sure they're on the all scorecards page.
      cy.get("[data-cy=tab-scorecards]").click()
      framework.criteria.map((criteria, index) => {
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score).should('be.visible')
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment).should('be.visible')
      })
      
      cy.get("[data-cy=tab-overview]").click()
      ensureCommentsAreAllThere(cy, framework)

    })
    cy.logOut()
  })

  it(" show on stacks", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report 1" + word
    var stack_name = "Stack - " + word

    var subtitle = chance.sentence()

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
        new_criteria: new_criteria_list
      })
    }

    cy.loginAsTestAdmin()

    // adds report
    cy.createStack(stack_name, null, subtitle)
    cy.goToItem(stack_name)
    cy.createReport(report_name)
    cy.addReportToStack(stack_name, report_name,)

    cy.goToItem(report_name)

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      
      cy.goToItem(stack_name)

      // Make sure they're on the frameworks by report page.
      cy.get("[data-cy=tab-frameworks]").click()
      ensureCommentsAreAllThere(cy, framework)
      
      // Make sure they're on the frameworks by scorecard page.
      cy.get("[data-cy=tab-reports]").click()
      cy.get("[data-cy=tab-frameworks]").click()
      cy.get("[data-cy=toggle-individual-scores]").click()
      ensureCommentsAreAllThere(cy, framework)
      
      // Make sure they're on the reports page
      cy.get("[data-cy=tab-reports]").click()
      cy.get("[data-cy=toggle-open]").click()
      ensureCommentsAreAllThere(cy, framework)

    })
    cy.logOut()
  })

})
