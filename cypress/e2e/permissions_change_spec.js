before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

describe("User-based permissions features:", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("removing admin permission should immediately update the UI.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        let stack_name = `stack-${word}`;
        cy.createFramework(framework_name);
        cy.createReport(report_name);
        cy.createSource(source_name);
        cy.createStack(stack_name);

        // Add permissions
        cy.goToItem(framework_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(report_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(source_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(stack_name)
        cy.addPermissionsAdmin(name)

        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(framework_name)
        let user_slug = name.replace(" ", "_").toLowerCase()
        
        cy.get("[data-cy=framework] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get(`[data-cy=permissions] [data-cy=role-${user_slug}] [data-cy=can-admin]:first`).click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')

        cy.get("[data-cy=framework] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=framework] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()

        cy.get("[data-cy=permissions] [data-cy=save-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")
        
        
        cy.goToItem(report_name)
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get(`[data-cy=permissions] [data-cy=role-${user_slug}] [data-cy=can-admin]:first`).click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions]").click({})
        cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')

        cy.get("[data-cy=report] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()

        cy.get("[data-cy=permissions] [data-cy=save-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")
        
        cy.goToItem(source_name)
        cy.get("[data-cy=source] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get(`[data-cy=permissions] [data-cy=role-${user_slug}] [data-cy=can-admin]:first`).click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions]").click({})
        cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')

        cy.get("[data-cy=source] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=source] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()

        cy.get("[data-cy=permissions] [data-cy=save-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")

        cy.goToItem(stack_name)
        cy.get("[data-cy=stack] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get(`[data-cy=permissions] [data-cy=role-${user_slug}] [data-cy=can-admin]:first`).click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions]").click({})
        cy.get("[data-cy=permissions] [data-cy=save-permissions].saving").should('not.exist')

        cy.get("[data-cy=stack] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=stack] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=tab-permissions]").click()

        cy.get("[data-cy=permissions] [data-cy=save-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")
        
      });
    });
    cy.logOut()
  }); 


})
