var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});
function slugify(name) {
  return name.toLowerCase().replaceAll(' ', '_').replaceAll('"', "'")
}

describe("stacks graphs", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("update their initials when going between tabs", () => {
    cy.get("@orgNormalName").then(full_name=> {
      var framework_list = []
      var word = chance.word()
      var report_name = "Report 1" + word
      var stack_name = "Stack 1" + word
      let initials = full_name.split(" ")[0][0] + full_name.split(" ")[1][0]

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
          new_criteria_list.push({
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
          new_criteria: new_criteria_list
        })
      }

      // adds report
      cy.createReport(report_name)
      cy.createStack(stack_name)
      cy.addReportToStack(stack_name, report_name)

      // creates frameworks from a list of frameworks with criteria and adds
      // them to the report
      framework_list.map((framework) => {
        cy.createFramework(framework.name)
        cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
        cy.goToItem(report_name)
        cy.addScorecards(report_name, framework.name, framework.criteria)
        cy.addScorecards(report_name, framework.name, framework.new_criteria)
        cy.goToItem(framework.name)

        // Make sure they're on the frameworks page
        cy.goToItem(stack_name)
        cy.get("[data-cy=tab-frameworks]").click()
        let sorted_criteria = [...framework.criteria]
        let new_sorted_criteria = [...framework.new_criteria]
        sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
        new_sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

        sorted_criteria.map((criteria, index) => {

          // Graphs show on all reports and individual report.
          let avg = (Number(criteria.score) + Number(new_sorted_criteria[index].score)) / 2;
          let avg_str;
          if (avg % 1) {
            avg_str = avg.toFixed(1)
          } else {
            avg_str = avg.toFixed(1)
          }
          avg_str = avg_str.replace(".", "_")
          let criteria_score_str = String(criteria.score.toFixed(1)).replace(".", "_")
          let criteria2_score_str = String(new_sorted_criteria[index].score.toFixed(1)).replace(".", "_")
          let report_name_slugify = slugify(report_name)
          
          cy.get("[data-cy=tab-frameworks]").click()
          // Make sure the graph has just average points
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('exist')
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${avg_str}]`).should('exist')
          // Correct labels
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${avg_str}`).contains(report_name.slice(0,2)).should('be.visible')

          // Make sure the graph has all points
          cy.get("[data-cy=toggle-individual-scores]").click()
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('be.visible')
          // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${avg_str}]`).contains(initials).should('not.exist')
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria_score_str}]`).contains(initials.slice(0,1)).should('exist')
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria2_score_str}]`).contains(initials.slice(0,1)).should('exist')

          cy.get("[data-cy=toggle-individual-scores]").click()
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('be.visible')
          cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${avg_str}`).contains(report_name.slice(0,2)).should('be.visible')
          if (avg_str != criteria_score_str) {
            cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria_score_str}]`).should('not.exist')
          }
          if (avg_str != criteria2_score_str) {
            cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria2_score_str}]`).should('not.exist')
          }
          // Make sure the report graph initials are right.
          cy.get("[data-cy=tab-reports]").click()
          cy.get(`[data-cy=report-${report_name_slugify}] [data-cy=toggle-open]`).click()
          cy.get(`[data-cy=report-${report_name_slugify}] [data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${avg_str}`).should('be.visible')
          cy.get(`[data-cy=report-${report_name_slugify}] [data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria_score_str}]`).contains(initials.slice(0, 1)).should('exist')
          cy.get(`[data-cy=report-${report_name_slugify}] [data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${criteria2_score_str}]`).contains(initials.slice(0, 1)).should('exist')


        })
      })

    })
  })
  
})
