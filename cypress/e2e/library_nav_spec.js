before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("Confirm library button", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("should bring up the library page.", () => {
    // Library Button should exist
    cy.get("[data-cy=nav-library]").should("be.visible")

    // Check that library page hasn't always been visible
    cy.get("[data-cy=library]").should("not.exist")

    // When Library button is clicked
    cy.get("[data-cy=nav-library]").click()

    // I should see the Library Page
    cy.get("[data-cy=library]").should("be.visible")
  })
})
