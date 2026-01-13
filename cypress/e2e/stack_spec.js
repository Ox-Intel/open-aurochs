var num_criteria = 2
var num_framework = 1
// Generate framework list
function normalize_to_score_data_cy(score) {
  return String(Number(score).toFixed(1)).replace(".", "_")  
}
function slugify(name) {
  return name.toLowerCase().replaceAll(' ', '_').replaceAll('"', "'")
}

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("stacks", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("can be created and edited", () => {
    var word = chance.word()
    var stack_name = "Stack - " + word
    var subtitle = chance.sentence()
    cy.createStack(stack_name, null, subtitle)
    cy.goToItem(stack_name)

    var new_stack_name = "Stack - " + word
    var new_subtitle = chance.sentence()

    cy.get("[data-cy=edit]").click()
    cy.get("[data-cy=input-stack-name]").clear()
    cy.wait(5)
    cy.get("[data-cy=input-stack-name]").type(new_stack_name)
    cy.get("[data-cy=input-stack-subtitle]").clear()
    cy.wait(5)
    cy.get("[data-cy=input-stack-subtitle]").type(new_subtitle)
    cy.get("[data-cy=save]").click()
    cy.get("[data-cy=save].saving").should('not.exist')

    cy.goToLibrary()
    cy.get("[data-cy=library-feed-item]").contains(new_stack_name).should("be.visible")

    cy.goToItem(new_stack_name)
    cy.get("[data-cy=stack] [data-cy=name]").contains(new_stack_name).should('be.visible')
    cy.get("[data-cy=stack] [data-cy=subtitle]").contains(new_subtitle).should('be.visible');
  });
  it("can have reports added and removed", () => {
    var word = chance.word()
    var stack_name = "Stack - " + word
    var report_name = "Report - " + word
    var report2_name = "Report2 - " + word
    var subtitle = chance.sentence()
    cy.createStack(stack_name, null, subtitle)
    cy.goToItem(stack_name)
    cy.createReport(report_name)
    cy.addReportToStack(stack_name, report_name,)
    cy.goToItem(report_name)
    
    cy.get("[data-cy=report] [data-cy=stack-" + slugify(stack_name) + "]").contains(stack_name).should("be.visible").click()
    
    cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "]").contains(report_name)
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "] [data-cy=remove]").click()
    cy.on('window:confirm', () => true);

    
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "]").should("not.exist")
    cy.goToItem(report_name)
    cy.get("[data-cy=report] .stack-badge").should("not.exist")

    // Add from report
    cy.goToItem(report_name)
    cy.addStackToReport(stack_name, report_name)
    cy.get("[data-cy=report] .stack-badge").contains(stack_name).should("be.visible")


    cy.goToItem(stack_name)
    cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=name]").contains(report_name).should("be.visible").click()

    
    cy.get("[data-cy=report] [data-cy=stack-" + slugify(stack_name) + "]").contains(stack_name).should("be.visible").click()
    
    cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "]").contains(report_name)
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "] [data-cy=remove]").click()
  })

  it("show the correct summary graphs", () => {
    var word = chance.word()
    var stack_name = "Stack - " + word
    var report_name = "Report - " + word
    var report2_name = "Report2 - " + word
    var subtitle = chance.sentence()
    cy.createStack(stack_name, null, subtitle)
    cy.goToItem(stack_name)
    cy.createReport(report_name)

    // Add framework, scorecards
    let num_criteria = 2
    let num_framework = 1
    let framework_list = []

    for (var i = 0; i < num_framework; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var new_criteria_list = []
      var start_score;
      for (var j = 0; j < num_criteria; j++) {
        if (criteria_list.length < 1) {
          start_score = 1;
        } else {
          start_score = criteria_list[criteria_list.length - 1].score;
        }
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          subtitle: "subtitle",
          weight: start_score * num_criteria,
          score: start_score + chance.integer({ min: 1, max: num_criteria }),
          comment: chance.sentence({words: 5}),
        })
        new_criteria_list.push({
          name: `criteria-${j}-${word}`,
          subtitle: "subtitle",
          weight: start_score,
          score: start_score + chance.integer({ min: 1, max: num_criteria }),
          comment: chance.sentence({words: 5}),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        new_criteria: new_criteria_list
      })
    }

    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.new_criteria)
    })

    cy.addReportToStack(stack_name, report_name,)
    cy.goToItem(report_name)
    
    cy.get("[data-cy=report] [data-cy=stack-" + slugify(stack_name) + "]").contains(stack_name).should("be.visible").click()
    
    cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "]").contains(report_name)
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "] [data-cy=remove]").click()
    cy.on('window:confirm', () => true);

    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=report-" + slugify(report_name) + "]").should("not.exist")
    cy.goToItem(report_name)
    cy.get("[data-cy=report] .stack-badge").should("not.exist")

    // Add from report
    cy.goToItem(report_name)
    cy.addStackToReport(stack_name, report_name)
    cy.get("[data-cy=report] .stack-badge").contains(stack_name).should("be.visible")


    cy.goToItem(stack_name)
    cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
    cy.get("[data-cy=stack] [data-cy=report-list] [data-cy=name]").contains(report_name).should("be.visible")

    // Make sure report, ox score, and scorecards are on the overviewp page.
    cy.get("[data-cy=stack] [data-cy=tab-overview]").click()
    cy.get("[data-cy=stack] [data-cy=overview] [data-cy=report-0] [data-cy=name]").contains(report_name).should("be.visible")
    cy.get("[data-cy=stack] [data-cy=overview] [data-cy=report-0] [data-cy=scorecard-count]").contains("2").should("be.visible")
    cy.get("[data-cy=stack] [data-cy=overview] [data-cy=report-0] [data-cy=ox-bar]").should("be.visible")

    framework_list.map((framework) => {
      let sorted_criteria = [...framework.criteria]
      let sorted_new_criteria = [...framework.new_criteria]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_new_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      // Make sure graphs are there
      cy.get("[data-cy=stack] [data-cy=tab-frameworks]").click()
      sorted_criteria.map((criteria, index) => {
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
        let avg = (Number(criteria.score) + Number(sorted_new_criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(avg_str)}]`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}]`).should('exist')
      })


      // Make sure toggle by scorecard shows all scorecards
      cy.get("[data-cy=stack] [data-cy=tab-frameworks]").click()
      cy.get("[data-cy=stack] [data-cy=toggle-individual-scores]").click()

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_new_criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        // Weight and average
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=average-score]`).contains(avg_str)

        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}]`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}]`).should('exist')
      })

      sorted_new_criteria.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}]`).should('exist')
      })

      // Make sure reports page shows all points.
      cy.get("[data-cy=stack] [data-cy=tab-reports]").click()
      cy.get("[data-cy=stack] [data-cy=framework-0]").click()

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_new_criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        // Weight and average
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=average-score]`).contains(avg_str)

        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}]`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}]`).should('exist')
      })

      sorted_new_criteria.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}]`).should('exist')
      })

    })
  });
})
