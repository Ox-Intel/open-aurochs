var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("making new things from a current thing", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("works for reports", () => {
    var framework_list = []
    var word = chance.word()

    cy.loginAsTestAdmin()

    // In view mode
    cy.createReport(`report 1: ${word}`)
    cy.goToItem(`report 1: ${word}`)
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-report]").click({'force': true})
    
    cy.get("[data-cy=input-report-name]").should("be.visible")
    cy.get("[data-cy=input-report-name]").should("have.value", "New Report")

    // In Edit mode
    cy.goToItem(`report 1: ${word}`)
    cy.get("[data-cy=edit]").click()
    cy.get("[data-cy=input-report-name]").should("be.visible")
    cy.get("[data-cy=input-report-name]").should("have.value", `report 1: ${word}`)
    
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-report]").click({'force': true})
    
    cy.get("[data-cy=input-report-name]").should("be.visible")
    cy.get("[data-cy=input-report-name]").should("have.value", "New Report")
  })
  it("works for frameworks", () => {
    var framework_list = []
    var word = chance.word()

    cy.loginAsTestAdmin()

    // In view mode
    cy.createFramework(`framework 1: ${word}`)
    cy.goToItem(`framework 1: ${word}`)
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-framework]").click({'force': true})
    
    cy.get("[data-cy=input-framework-name]").should("be.visible")
    cy.get("[data-cy=input-framework-name]").should("have.value", "New Framework")

    // In Edit mode
    cy.goToItem(`framework 1: ${word}`)
    cy.get("[data-cy=edit]").click()
    cy.get("[data-cy=input-framework-name]").should("be.visible")
    cy.get("[data-cy=input-framework-name]").should("have.value", `framework 1: ${word}`)
    
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-framework]").click({'force': true})
    
    cy.get("[data-cy=input-framework-name]").should("be.visible")
    cy.get("[data-cy=input-framework-name]").should("have.value", "New Framework")
  })

  it("works for sources", () => {
    var framework_list = []
    var word = chance.word()

    cy.loginAsTestAdmin()

    // In view mode
    cy.createSource(`source 1: ${word}`)
    cy.goToItem(`source 1: ${word}`)
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-source]").click({'force': true})
    
    cy.get("[data-cy=input-source-name]").should("be.visible")
    cy.get("[data-cy=input-source-name]").should("have.value", "New Source")

    // In Edit mode
    cy.goToItem(`source 1: ${word}`)
    cy.get("[data-cy=edit]").click()
    cy.get("[data-cy=input-source-name]").should("be.visible")
    cy.get("[data-cy=input-source-name]").should("have.value", `source 1: ${word}`)
    
    cy.get("[data-cy=nav-new]").should("be.visible").trigger('mouseenter').trigger('mouseover')
    cy.get("[data-cy=nav-new-source]").click({'force': true})
    
    cy.get("[data-cy=input-source-name]").should("be.visible")
    cy.get("[data-cy=input-source-name]").should("have.value", "New Source")
  })
  
})
