before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("My profile:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    // cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("editing my information works.", () => {
    cy.loginAsTestUser()
    cy.get("@orgNormalUsername").then(username=> {
      cy.get("@orgNormalName").then(full_name=> {
        cy.get("@orgNormalEmail").then(email=> {
          cy.get("@orgNormalPassword").then(password=> {
            cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
            cy.get("[data-cy=nav-profile]").should("be.visible").click()
            cy.get("[data-cy=first_name] input").should('have.value', full_name.split(" ")[0]).should("be.visible")
            cy.get("[data-cy=last_name] input").should('have.value', full_name.split(" ")[1]).should("be.visible")
            cy.get("[data-cy=email] input").should('have.value', email).should("be.visible")
            cy.get("[data-cy=username] input").should('have.value', username).should("be.visible")

            let new_first_name = chance.name()
            let new_last_name = chance.name()
            let new_email = chance.email()
            let new_username = chance.word()
            cy.get("[data-cy=first_name] input").clear().type(new_first_name)
            cy.get("[data-cy=last_name] input").clear().type(new_last_name)
            cy.get("[data-cy=email] input").clear().type(new_email)
            cy.get("[data-cy=username] input").clear().type(new_username)
            cy.get("[data-cy=save-profile]").click()
            cy.get("[data-cy=save-profile].saving").should('not.exist')

            // Make sure the menu is updated
            cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
            cy.get("[data-cy=menu-full-name]").contains(new_first_name)
            cy.get("[data-cy=menu-full-name]").contains(new_last_name)
            cy.get("[data-cy=menu-username]").contains(new_username)


            cy.logOut()
            cy.login(new_username, password)
            cy.get("[data-cy=nav-user-menu]").should("be.visible").click()
            cy.get("[data-cy=menu-full-name]").contains(new_first_name)
            cy.get("[data-cy=menu-full-name]").contains(new_last_name)
            cy.get("[data-cy=menu-username]").contains(new_username)

            cy.get("[data-cy=nav-profile]").should("be.visible").click()
            cy.get("[data-cy=first_name] input").should('have.value', new_first_name).should("be.visible")
            cy.get("[data-cy=last_name] input").should('have.value', new_last_name).should("be.visible")
            cy.get("[data-cy=email] input").should('have.value', new_email).should("be.visible")
            cy.get("[data-cy=username] input").should('have.value', new_username).should("be.visible")

          });
        });
      });
    });
    
  })
 
  it("changing my password works", () => {
    // Login as user
    cy.loginAsTestAdmin()
    let new_pass = chance.word()
    cy.changePassword(new_pass)
    cy.logOut()

    cy.get("@orgAdminUsername").then(username=> {
      // Login with new password
      cy.login(username, new_pass)
      cy.get("[data-cy=dashboard]").should('be.visible')
    })
  })
})
