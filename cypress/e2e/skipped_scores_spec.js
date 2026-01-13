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


describe("skipped scores ", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it(" bubble up to ox scores", () => {
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
          skipped: j == 1,
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
    cy.get("[data-cy=report] [data-cy=average-ox-score] [data-cy=star]").should('not.exist')
    cy.get("[data-cy=report] [data-cy=scorecard] [data-cy=star]").should('not.exist')

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
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=weight]`).contains(criteria.weight).should('be.visible')
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=average-score]`).contains(criteria.score).should('be.visible')
        if (criteria.skipped) {
          cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains("Skipped").should('be.visible')
        } else {
          cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score).should('be.visible')
        }
      })
      cy.get("[data-cy=report] [data-cy=scorecard] [data-cy=star]").should('be.visible')
      cy.get("[data-cy=report] [data-cy=average-ox-score] [data-cy=star]").should('be.visible')
    })
    cy.logOut()
  })
  it("and are averaged correctly", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report 1" + word
    let stack_name = "Stack " + word

    for (var i = 0; i < num_framework; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var new_criteria_list = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: "description",
          weight: 5,
          score: 5,
          comment: chance.sentence({words: 5}),
          skipped: false,
        })
        new_criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: "description",
          weight: 5,
          score: null,
          comment: chance.sentence({words: 5}),
          skipped: true,
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
    cy.createStack(stack_name)
    cy.createReport(report_name)
    cy.addReportToStack(stack_name, report_name)
    cy.get("[data-cy=report] [data-cy=average-ox-score] [data-cy=star]").should('not.exist')
    cy.get("[data-cy=report] [data-cy=scorecard] [data-cy=star]").should('not.exist')

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    let count = 0;
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.new_criteria)      

      // Make sure they're on the all scorecards page.
      cy.get(`[data-cy=report] [data-cy=tab-overview]`).click()
      cy.get(`[data-cy=report] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("5").should('be.visible')
      cy.get(`[data-cy=report] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("2.5").should('not.exist')
      count ++;
    })
    
    count = 0;
    // Make sure they're correct on stack too.
    cy.goToItem(stack_name)
    framework_list.map((framework) => {
      cy.get(`[data-cy=stack] [data-cy=tab-frameworks]`).click()
      cy.get(`[data-cy=stack] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("5").should('be.visible')
      cy.get(`[data-cy=stack] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("2.5").should('not.exist')
      cy.get("[data-cy=stack] [data-cy=toggleByReportOrScorecard]").click()
      cy.get(`[data-cy=stack] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("5").should('be.visible')
      cy.get(`[data-cy=stack] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("2.5").should('not.exist')
      cy.get(`[data-cy=stack] [data-cy=tab-reports]`).click()
      cy.get(`[data-cy=stack] [data-cy=reports] [data-cy=toggle-open]`).click()
      cy.get(`[data-cy=stack] [data-cy=reports] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("5").should('be.visible')
      cy.get(`[data-cy=stack] [data-cy=reports] [data-cy=criteria-${count}] [data-cy=average-score]`).contains("2.5").should('not.exist')
      count ++;
    })

  })


})
