var framework_name = chance.sentence({words: 3})
var report_name = chance.sentence({words: 4})
var criteria_list = []
for (var i = 0; i < 3; i++) {
  criteria_list.push({
    index: i,
    name: chance.sentence({words: 5}),
    description: chance.sentence(),
    weight: chance.integer({ min: 1, max: 10 }),
  })
}
before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("framework creation works and scorecard and visualization also works", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("should support new criteria creation, modification, and deletion", () => {
    cy.createFramework(framework_name)

    // adds criteria
    cy.addCriteriaToEmptyFramework(framework_name, criteria_list)

    // edits criteria
    cy.get("div").contains("Edit Criteria").click()

    for (var i = 0; i < criteria_list.length; i++) {
      cy.get(`[data-cy=name-edit-${i}]`)
        .clear()
        .type(`Edited name ${i}`)
      cy.get(`[data-cy=description-edit-${i}]`)
        .clear()
        .type(`Edited description ${i}`)
    }

    // adds some new criteria
    cy.get("[data-cy=new-criteria]").click()
    cy.get(`[data-cy=name-edit-${i}]`)
      .type(`Edited name ${i}`)
    cy.get(`[data-cy=description-edit-${i}] textarea`)
      .type(`Edited description ${i}`)
    cy.get(`[data-cy=criteria-weight-${i}] input`).invoke('val', chance.integer({ min: 1, max: 10 })).trigger('change').click({force:true})

    cy.get("div").contains("Save").click()
    cy.get("div").contains(`Edited name ${i}`).should("exist")
    for (var i = 0; i < criteria_list.length; i++) {
      cy.get("div").should("not.contain", )
      cy.get("div").should("not.contain", )
      cy.get("div").contains(`Edited name ${i}`).should("exist")
      cy.get("div").contains(`Edited description ${i}`).should("exist")
    }

    // removes criteria except for newest one
    cy.get("div").contains("Edit Criteria").click()
    for (var j = criteria_list.length - 1; j >= 0; j--) {
      cy.get(`[data-cy=delete-criteria-${j}]`).click()
      cy.get("div").should("not.contain", )
      cy.get("div").should("not.contain", )
    }
    cy.get("div").contains("Save").click()
    cy.get("div").contains(`Edited name ${i}`).should("exist")
  })
})
