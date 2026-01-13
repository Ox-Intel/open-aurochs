var num_criteria = 2
var num_frameworks = 1
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


describe("noise and ox suggestions:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("display low noise and no suggestions when scoring is close and weight is high", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report" + word

    for (var i = 0; i < num_frameworks; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: chance.integer({ min: 5, max: 10 }),
          score: chance.integer({ min: 5, max: 7 }),
          comment: chance.word(),
        })
        criteria_list2.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: criteria_list[j].weight,
          score: chance.integer({ min: 5, max: 7 }),
          comment: chance.word(),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        criteria2: criteria_list2
      })
    }

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    cy.loginAsTestAdmin()
    cy.createReport(report_name)
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.criteria2)
    });
    framework_list.map((framework) => {
      // Make sure they're on the overview page.
      cy.get("[data-cy=tab-overview]").click()
      let sorted_criteria = [...framework.criteria]
      let sorted_criteria2 = [...framework.criteria2]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_criteria2.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_criteria2[index].score)) / 2;
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
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      })

      sorted_criteria2.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        
        // Make sure ox suggestions shows properly.
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "").should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('not.exist')

        // Make sure noise shows properly
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=noise].low`).should('exist')
      })
    });
  });
  it("display no or ox suggestions when there is only one score", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report" + word

    for (var i = 0; i < num_frameworks; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: chance.integer({ min: 1, max: 10 }),
          score: chance.integer({ min: 5, max: 7 }),
          comment: chance.word(),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
      })
    }

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    cy.loginAsTestAdmin()
    cy.createReport(report_name)
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
    });
    framework_list.map((framework) => {
      // Make sure they're on the overview page.
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
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=weight]`).contains(criteria.weight)
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=average-score]`).contains(avg_str)

        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      
        // Make sure ox suggestions shows properly.
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "").should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('not.exist')

        // Make sure noise shows properly
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=noise].none`).should('not.exist')
        
      })
    });
  });
  it("display low noise and ox suggestions when scoring is close and importance is low", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report" + word

    for (var i = 0; i < num_frameworks; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: chance.integer({ min: 1, max: 3 }),
          score: chance.integer({ min: 5, max: 7 }),
          comment: chance.word(),
        })
        criteria_list2.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: criteria_list[j].weight,
          score: chance.integer({ min: 5, max: 7 }),
          comment: chance.word(),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        criteria2: criteria_list2
      })
    }

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    cy.loginAsTestAdmin()
    cy.createReport(report_name)
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.criteria2)
    });
    framework_list.map((framework) => {
      // Make sure they're on the overview page.
      cy.get("[data-cy=tab-overview]").click()
      let sorted_criteria = [...framework.criteria]
      let sorted_criteria2 = [...framework.criteria2]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_criteria2.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_criteria2[index].score)) / 2;
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
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      })

      sorted_criteria2.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        
        // Make sure ox suggestions shows properly.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('be.visible')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "low level of scoring noise")
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('be.visible')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "Ox recommends reviewing the importance of this criterion in the framework.")
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('not.exist')

        // Make sure noise shows properly
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=noise].low`).should('be.visible')
      })
    });
  });
  it("display high noise and ox suggestions when scoring is far", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report" + word

    for (var i = 0; i < num_frameworks; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: chance.integer({ min: 1, max: 10 }),
          score: chance.integer({ min: 1, max: 3 }),
          comment: chance.word(),
        })
        criteria_list2.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: criteria_list[j].weight,
          score: chance.integer({ min: 8, max: 10 }),
          comment: chance.word(),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        criteria2: criteria_list2
      })
    }

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    cy.loginAsTestAdmin()
    cy.createReport(report_name)
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.criteria2)
    });
    framework_list.map((framework) => {
      // Make sure they're on the overview page.
      cy.get("[data-cy=tab-overview]").click()
      let sorted_criteria = [...framework.criteria]
      let sorted_criteria2 = [...framework.criteria2]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_criteria2.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_criteria2[index].score)) / 2;
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
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      })

      sorted_criteria2.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        
        // Make sure ox suggestions shows properly.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('be.visible')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "appears to result in noisy judgments")
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('not.exist')

        // Make sure noise shows properly
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=noise].high`).should('be.visible')
      })
    });
  });
  it("display medium noise and no suggestions when scoring is medium", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report" + word

    for (var i = 0; i < num_frameworks; i++) {
      // Generate criteria list for each framework
      var criteria_list = []
      var criteria_list2 = []
      for (var j = 0; j < num_criteria; j++) {
        criteria_list.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: chance.integer({ min: 1, max: 10 }),
          score: chance.integer({ min: 2, max: 3 }),
          comment: chance.word(),
        })
        criteria_list2.push({
          name: `criteria-${j}-${word}`,
          description: chance.word(),
          weight: criteria_list[j].weight,
          score: criteria_list[j].score + 3,
          comment: chance.word(),
        })
      }

      framework_list.push({
        name: `framework-${i}-${word}`,
        criteria: criteria_list,
        criteria2: criteria_list2
      })
    }

    // creates frameworks from a list of frameworks with criteria and adds
    // them to the report
    cy.loginAsTestAdmin()
    cy.createReport(report_name)
    framework_list.map((framework) => {
      cy.createFramework(framework.name)
      cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
      cy.goToItem(report_name)
      cy.addScorecards(report_name, framework.name, framework.criteria)
      cy.addScorecards(report_name, framework.name, framework.criteria2)
    });
    framework_list.map((framework) => {
      // Make sure they're on the overview page.
      cy.get("[data-cy=tab-overview]").click()
      let sorted_criteria = [...framework.criteria]
      let sorted_criteria2 = [...framework.criteria2]
      sorted_criteria.sort((a, b) => (a.weight > b.weight) ? -1 : 1)
      sorted_criteria2.sort((a, b) => (a.weight > b.weight) ? -1 : 1)

      sorted_criteria.map((criteria, index) => {
        let avg = (Number(criteria.score) + Number(sorted_criteria2[index].score)) / 2;
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
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-average-${normalize_to_score_data_cy(avg_str)}`).should('exist')
      })

      sorted_criteria2.map((criteria, index) => {
        // Make sure the graph has all points.
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=dot-plot] [data-cy=point-${normalize_to_score_data_cy(criteria.score)}`).should('exist')
        
        // Make sure ox suggestions shows properly.
        // cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should("have.attr", "data-tip").and("contain", "").should('exist')
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=ox-suggestions]`).should('not.exist')

        // Make sure noise shows properly
        cy.get(`[data-cy=framework-0] [data-cy=criteria-${index}] [data-cy=noise].medium`).should('be.visible')
      })
    });
  })
})
