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

  // TODO: TEMP_NO_PUBLIC disabled.
  // it("the home page loads", () => {
  //   cy.visit(Cypress.env("APP_URL"))
  //   cy.get("div.ox-page").should("be.visible")
  //   cy.get("html").contains("Home:").should("be.visible")
  //   cy.get("div.ox-page").contains("Home!").should("be.visible")
  // })

  it("the login page loads", () => {
    cy.visit(Cypress.env("APP_URL") + "/accounts/login")
    cy.get("input[name=username]").should("be.visible")
  })

  it("the dashboard loads", () => {
    cy.visit(Cypress.env("APP_URL") + "/accounts/login")
    cy.get("input[name=username]").should("be.visible")
    cy.loginAsTestUser()
    cy.get("[data-cy=dashboard]").should("be.visible")
  })
})
