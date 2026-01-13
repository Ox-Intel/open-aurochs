before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("Login and logout work.", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("We're redirected if not logged in.", () => {

    cy.visit(Cypress.env("APP_URL") + "/dashboard")
    cy.get("#id_username").should("be.visible")
    cy.get("#id_password").should("be.visible")
    cy.get("[data-cy=nav-user-menu]").should("not.exist")

    // We don't currently redirect the URL.
    // cy.url().should("eq", Cypress.env("APP_URL") + "")
    cy.url().should("eq", Cypress.env("APP_URL") + "/accounts/login/?next=/dashboard")
  })
  it("Logging in with an incorrect login shows an error.", () => {
    cy.visit(Cypress.env("APP_URL"))
    // Login page loads and looks OK
    cy.get("#id_username").should("be.visible")
    cy.get("#id_password").should("be.visible")

    // Fill in bogus username and password.
    cy.get("#id_username").type("alkdfjadslf")
    cy.get("#id_password").type("alkdjflkadsf")
    cy.get("#id_submit").click()

    // See login failed message.
    cy.get(".errorlist")
      .contains(
        "Please enter a correct username and password. Note that both fields may be case-sensitive."
      )
      .should("be.visible")
  })
  it("Logging in works.", () => {
    // Enter credentials and log in.
    cy.loginAsTestUser()

    // No errrors
    cy.get("[data-cy=nav-user-menu]").should("be.visible")
    cy.get(".errorlist").should("not.exist")
    cy.logOut()


  })
  it("Confirms that special characters, emojis, and spaces in passwords work", () => {
    // Login as user
    cy.loginAsTestUser()
    // Change password to "          "
    cy.changePassword("          ")
    cy.logOut()

    cy.get("@orgNormalUsername").then(username=> {
      cy.log("username")
      cy.log(username)
      // Login with new password
      cy.login(username, "          ")
      // Change password to "✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️"
      cy.changePassword("✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️")
      cy.logOut()

      // Login with new password
      cy.login(username, "✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️✅🔴⬜️")
      // Change password to "™℠®©™℠®©™℠®©"
      cy.changePassword("™℠®©™℠®©™℠®©")
      cy.logOut()

      cy.login(username, "™℠®©™℠®©™℠®©")
      cy.logOut()
    })
  })
})
