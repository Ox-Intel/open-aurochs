before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("Release notes work:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("they show and can be closed.", () => {
  
    cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
    cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
    cy.get("[data-cy=nav-release-notes]").should("be.visible").click()
    cy.get("[data-cy=release-notes]").should("exist")
    cy.get("[data-cy=release-notes] [data-cy=close]").should("be.visible").click()
    cy.get("[data-cy=release-notes] [data-cy=close]").should("not.be.visible")

  })
  
})
