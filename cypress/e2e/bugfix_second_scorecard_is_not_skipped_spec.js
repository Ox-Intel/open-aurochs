var num_criteria = 10
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


describe("bugfix:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("adding a second scorecard doesn't make it skipped.", () => {
    var framework_list = []
    var word = chance.word()
    var report_name = "Report 1" + word
    let num_frameworks = 3

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
    cy.createReport(chance.word())
    cy.createReport(chance.word())

    // creates three frameworks
    for (let i=1; i<= num_frameworks; i++) {
      framework_list.map((framework) => {
        let fw_name = framework.name + ` ${i}`;
        cy.createFramework(fw_name)
        cy.addCriteriaToEmptyFramework(fw_name, framework.criteria)
      });
    };
    cy.goToItem(report_name)
    for (let i=1; i<= num_frameworks; i++) {
      framework_list.map((framework) => {
        let fw_name = framework.name + ` ${i}`;
        cy.get("[data-cy=add-scorecard]").click()
        cy.get("[data-cy=scorecard-framework-search] [data-cy=searchbox-search]").type(fw_name)
        cy.get("[data-cy=scorecard-framework-search] ul li").contains(fw_name).click()
        cy.get("[data-cy=add-scorecard-from-modal]").click()
        // cy.get("[data-cy=add-scorecard-from-modal].btn-disabled").should('not.exist')

        cy.get(`[data-cy=scorecard-${i-1}] [data-cy=save-scorecard]`).should('exist')
        cy.get(`[data-cy=scorecard-${i-1}] [data-cy=toggle-open-collapse]`).should('not.exist')

      })
    }
    cy.goToLibrary()
    cy.logOut()
  })
})
