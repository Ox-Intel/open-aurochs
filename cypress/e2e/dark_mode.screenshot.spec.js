before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("Dark and light mode work:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("toggling via the menu works.", () => {
    cy.createFramework("Dark/Light mode test framework")
    cy.goToDashboard()

    cy.get("html[data-theme=dark]").should("not.exist")
    cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
    // Set Dark
    cy.get("[data-cy=nav-toggle-mode]").contains("Dark Mode").should("be.visible")
    cy.get("[data-cy=nav-toggle-mode]").should("be.visible").click()
    cy.get("html[data-theme=dark]").should("be.visible")
    cy.get("html").click()
    cy.get("html").matchImageSnapshot("Dark Mode Dashboard");
    cy.get("[data-cy=ox-object-framework-0]").matchImageSnapshot("Dark Mode Framework");

    // Set Auto
    cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
    cy.get("[data-cy=nav-toggle-mode]").contains("Auto Mode").should("be.visible")
    cy.get("[data-cy=nav-toggle-mode]").should("be.visible").click()
    cy.get("html[data-theme=light").should("not.exist")
    cy.get("html[data-theme=dark").should("not.exist")

    // Set Light
    cy.get("[data-cy=nav-toggle-mode]").contains("Light Mode").should("be.visible")
    cy.get("[data-cy=nav-toggle-mode]").should("be.visible").click()
    cy.get("html[data-theme=light").should("be.visible")
    cy.get("html").click()
    cy.get("html").matchImageSnapshot("Light Mode Dashboard");
    cy.get("[data-cy=ox-object-framework-0]").matchImageSnapshot("Light Mode Framework");
    
  })
  
})
