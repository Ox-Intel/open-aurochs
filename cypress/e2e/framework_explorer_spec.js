var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("framework explorer", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("shows up with correct graphs", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report 1" + word

    for (var i = 0; i < num_framework; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var new_criteria_list = []
      var new_criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: "description",
          weight: chance.integer({ min: 1, max: 10 }),
          score: chance.integer({ min: 1, max: 10 }),
          comment: chance.sentence({words: 5}),
        })
        new_criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: "description",
          weight: criteria_list[j].weight,
          score: chance.integer({ min: 1, max: 10 }),
          comment: chance.sentence({words: 5}),
        })
        new_criteria_list2.push({
          name: `criteria-${j}-${word}`,
          description: "description",
          weight: criteria_list[j].weight,
          score: chance.integer({ min: 1, max: 10 }),
          comment: chance.sentence({words: 5}),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        new_criteria: new_criteria_list,
        new_criteria2: new_criteria_list2,
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
      cy.addScorecards(report_name, framework.name, framework.new_criteria)
      cy.addScorecards(report_name, framework.name, framework.new_criteria2)
      cy.goToItem(framework.name)

      // Make sure they're on the all scorecards page.
      cy.get("[data-cy=tab-explorer]").click()
      framework.criteria.map((criteria, index) => {
        cy.get(`[data-cy=explore-criteria-${index}]`).click()
        cy.get("[data-cy=criteria-name]").contains(criteria.name)
        cy.get("[data-cy=criteria-description]").contains(criteria.description)

        cy.get("[data-cy=report-0] [data-cy=report-name]").contains(report_name)

        // Graphs show on all reports and individual report.
        let avg = (Number(criteria.score) + Number(framework.new_criteria[index].score) + Number(framework.new_criteria2[index].score)) / 3;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg.toFixed(1)
        }
        avg_str = avg_str.replace(".", "_")
        let criteria_score_str = String(criteria.score.toFixed(1)).replace(".", "_")
        let criteria_2_score_str = String(framework.new_criteria[index].score.toFixed(1)).replace(".", "_")
        let criteria_22_score_str = String(framework.new_criteria2[index].score.toFixed(1)).replace(".", "_")
        cy.get(`[data-cy=report-all] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('exist')
        // Make sure the graph has all points.
        cy.get(`[data-cy=report-0] [data-cy=dot-plot] [data-cy=point-${criteria_score_str}]`).should('exist')
        cy.get(`[data-cy=report-0] [data-cy=dot-plot] [data-cy=point-${criteria_2_score_str}]`).should('exist')
        cy.get(`[data-cy=report-0] [data-cy=dot-plot] [data-cy=point-${criteria_22_score_str}]`).should('exist')
        cy.get(`[data-cy=report-0] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('exist')
        cy.get(`[data-cy=report-1]`).should('not.exist')

      })
    })
  })
  
})
