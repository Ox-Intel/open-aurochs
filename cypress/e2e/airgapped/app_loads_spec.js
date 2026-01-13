before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});
describe("Basic app smoketest", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("the home page loads", () => {
    cy.visit(Cypress.env("APP_URL"))
    cy.get("input[name=username]").should("be.visible")
    // Ensure video is complete
    cy.wait(2000)
  })

  it("the login page loads", () => {
    cy.visit(Cypress.env("APP_URL") + "/accounts/login")
    cy.get("input[name=username]").should("be.visible")
    // Ensure video is complete
    cy.wait(2000)
  })

  it("the dashboard loads", () => {
    cy.visit(Cypress.env("APP_URL"))
    cy.get("input[name=username]").should("be.visible")
    cy.loginAsTestUser()
    cy.get("[data-cy=dashboard]").should("be.visible")
    // Ensure video is complete
    cy.wait(2000)
  })
})
