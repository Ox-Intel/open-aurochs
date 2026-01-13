before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("User data", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("is updated immediately when changes are made in the admin", () => {
    cy.get('@orgNormalName').then(fullName => {
      cy.get('@orgNormalUsername').then(username => {
        cy.get('@orgNormalPassword').then(password => {
          cy.get('@orgNormalEmail').then(email => {
            // Library Button should exist
            cy.get("[data-cy=dashboard]").should("be.visible");
            cy.get("[data-cy=nav-library]").should("be.visible");

            // // Go to user profile
            cy.get("[data-cy='nav-user-menu']").click()
            cy.get("[data-cy='nav-profile']").click()


            cy.get("[data-cy='first_name'] input").should('have.value', fullName.split(" ")[0]);
            cy.get("[data-cy='last_name'] input").should('have.value', fullName.split(" ")[1]);
            cy.get("[data-cy='email'] input").should('have.value', email);
            cy.get("[data-cy='username'] input").should('have.value', username);


            cy.logOut();
            cy.loginAsSuper()
            cy.visit(Cypress.env("APP_URL") + "/administration/organizations/user/")
            cy.get("#changelist-search #searchbar").type(username)
            cy.get("#changelist-search input[type='submit']").click()

            cy.get("a").contains(username).click()
            cy.get("#id_username").clear().type(username + "-changed");
            cy.get("#id_email").clear().type(email + "-changed");
            cy.get("#id_first_name").clear() .type(fullName.split(" ")[0] + "-changed");
            cy.get("#id_last_name").clear() .type(fullName.split(" ")[1] + "-changed");
            cy.get("input[name='_continue']").click()
            cy.wait(250)

            cy.get("#logout-form button").click()
            cy.login(username + "-changed", password);
            cy.get("[data-cy=dashboard]").should("be.visible");
            cy.get("[data-cy=nav-library]").should("be.visible");

            // // Go to user profile
            cy.get("[data-cy='nav-user-menu']").click()
            cy.get("[data-cy='nav-profile']").click()

            cy.get("[data-cy='first_name'] input").should('have.value', fullName.split(" ")[0] + "-changed");
            cy.get("[data-cy='last_name'] input").should('have.value', fullName.split(" ")[1] + "-changed");
            cy.get("[data-cy='email'] input").should('have.value', email + "-changed");
            cy.get("[data-cy='username'] input").should('have.value', username + "-changed");
            cy.logOut();
          });
        });
      });
    });

  });
})
