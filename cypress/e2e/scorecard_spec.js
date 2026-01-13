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


describe("adding, deleting, editing scorecards generally works", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("checks that adding, deleting, editing scorecards works", () => {
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
      cy.editScorecards(report_name, framework.name, framework.new_criteria)

      // Make sure they're on the all scorecards page.
      cy.get("[data-cy=tab-scorecards]").click()
      framework.new_criteria.map((criteria, index) => {
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=weight]`).contains(criteria.weight).should('be.visible')
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=average-score]`).contains(criteria.score).should('be.visible')
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score).should('be.visible')
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment).should('be.visible')
      })
    })
    cy.logOut()
  })
  it("adding two scorecards works", () => {
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
    });
    framework_list.map((framework) => {
      // Make sure they're on the all scorecards page.
      cy.get("[data-cy=tab-scorecards]").click()
      cy.get("[data-cy=scorecards] [data-cy=toggle-open-expand]").click()
      framework.criteria.map((criteria, index) => {
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=weight]`).contains(criteria.weight)
        let avg = (Number(criteria.score) + Number(framework.new_criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=average-score]`).contains(avg_str)
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score)
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment)
      })
      framework.new_criteria.map((criteria, index) => {
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=weight]`).contains(criteria.weight)
        let avg = (Number(criteria.score) + Number(framework.criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        // cy.get(`[data-cy=scorecard-row-${index}] [data-cy=average-score]`).contains(avg_str)
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=score]`).contains(criteria.score)
        cy.get(`[data-cy=scorecard-row-${index}] [data-cy=comment]`).contains(criteria.comment)
      })

      // Make sure they're on the overview page.
      cy.get("[data-cy=tab-overview]").click()
      let sorted_criteria = [...framework.criteria]
      let sorted_new_criteria = [...framework.new_criteria]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_new_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_new_criteria[index].score)) / 2;
        let avg_str;
        if (avg % 1) {
          avg_str = avg.toFixed(1)
        } else {
          avg_str = avg
        }
        // Weight and average
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=average-score]`).contains(avg_str)

        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      })

      sorted_new_criteria.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
      })
    })
    cy.logOut()
  })
  it("checks that adding and editing scorecards works but you can't see more if you have score only permissions.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        cy.loginAsTestUser()
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
              comment: chance.sentence({words: 2}),
            })
            new_criteria_list.push({
              name: `criteria-${j}-${word}`,
              description: "description",
              weight: criteria_list[j].weight,
              score: chance.integer({ min: 1, max: 10 }),
              comment: chance.sentence({words: 2}),
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
          cy.goToItem(framework.name)
          cy.addPermissionsReadOnly(name)
          cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
          cy.createReport(report_name)
          cy.addScorecards(report_name, framework.name, framework.new_criteria)
          
          // adds report
          cy.goToItem(report_name)
          cy.addPermissionsScoreOnly(name)
        })

        
        cy.logOut()
        cy.loginAsTestAdmin()

        // creates frameworks from a list of frameworks with criteria and adds
        // them to the report
        framework_list.map((framework) => {
          cy.goToItem(report_name)
          cy.addScorecards(report_name, framework.name, framework.criteria)

          // Make sure they're not on the all scorecards page.
          cy.get("[data-cy=tab-scorecards]").click()
          // cy.get("[data-cy=scorecards] [data-cy=no-permissions]").should("exist")

          // Make sure they only see their scores on the overview page.
          cy.get("[data-cy=tab-overview]").click()
          let sorted_criteria = [...framework.criteria]
          sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

          sorted_criteria.map((criteria, index) => {
            let avg = Number(criteria.score);
            let avg_str;
            if (avg % 1) {
              avg_str = avg.toFixed(1)
            } else {
              avg_str = avg
            }
            // Weight and average
            // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
            cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=average-score]`).contains(avg_str)

            // Make sure the graph has all points.
            cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
            cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
          })
        })
      })
    })
  })
  it("checks that deleting scorecards works if you have edit, or score only but it's your scorecard.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        cy.loginAsTestUser()
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
              comment: chance.sentence({words: 2}),
            })
            new_criteria_list.push({
              name: `criteria-${j}-${word}`,
              description: "description",
              weight: criteria_list[j].weight,
              score: chance.integer({ min: 1, max: 10 }),
              comment: chance.sentence({words: 2}),
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
          cy.goToItem(framework.name)
          cy.addPermissionsReadOnly(name)
          cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
          cy.createReport(report_name)
          cy.addScorecards(report_name, framework.name, framework.new_criteria)
          
          // adds report
          cy.goToItem(report_name)
          cy.addPermissionsScoreOnly(name)
        })

        
        cy.logOut()
        cy.loginAsTestAdmin()

        // creates frameworks from a list of frameworks with criteria and adds
        // them to the report
        framework_list.map((framework) => {
          cy.goToItem(report_name)
          cy.addScorecards(report_name, framework.name, framework.criteria)

          // Make sure they're not on the all scorecards page.
          // cy.get("[data-cy=tab-scorecards]").click()
          // cy.get("[data-cy=scorecards] [data-cy=no-permissions]").should("exist")
          cy.get("[data-cy=tab-scorecards]").click()
          cy.get("[data-cy=scorecards] [data-cy=scorecard-row-0]").should("be.visible")
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=scorecards] [data-cy=delete-scorecard]:first").click()
          cy.get("[data-cy=scorecards] [data-cy=scorecard-row-0]").should("not.exist")

          // Make sure they only see their scores on the overview page.
        })
        cy.logOut()
        cy.loginAsTestUser()
        cy.goToItem(report_name)
        cy.get("[data-cy=tab-scorecards]").click()
        cy.get("[data-cy=scorecards] [data-cy=toggle-open-expand]").click()
        cy.get("[data-cy=scorecards] [data-cy=scorecard-row-0]").should("be.visible")
        cy.on('window:confirm', () => true);
        cy.get("[data-cy=scorecards] [data-cy=delete-scorecard]:first").click()
        cy.get("[data-cy=scorecards] [data-cy=scorecard-row-0]").should("not.exist")
        
      })
    })
    cy.logOut()
  })
})
