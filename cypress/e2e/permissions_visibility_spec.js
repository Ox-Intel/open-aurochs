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
  it("adding and removing user permissions works.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        cy.createFramework(framework_name);
        cy.createReport(report_name);
        cy.createSource(source_name);
        cy.wait(20000)

        // Admin should not see any of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.itemDoesNotExist(framework_name)
        cy.itemDoesNotExist(report_name)
        cy.itemDoesNotExist(source_name)

        // // Add admin
        // cy.logOut()
        // cy.loginAsTestUser()
        // cy.goToItem(framework_name)
        // cy.addPermissionsReadWrite(name)
        // cy.goToItem(report_name)
        // cy.addPermissionsReadWrite(name)
        // cy.goToItem(source_name)
        // cy.addPermissionsReadWrite(name)

        // // Admin should see all of these.
        // cy.logOut()
        // cy.loginAsTestAdmin()
        // cy.goToItem(framework_name)
        // cy.get("[data-cy=framework]").should("be.visible")
        // cy.goToItem(report_name)
        // cy.get("[data-cy=report]").should("be.visible")
        // cy.goToItem(source_name)
        // cy.get("[data-cy=source]").should("be.visible")


        // // Remove admin
        // cy.logOut()
        // cy.loginAsTestUser()
        // cy.goToItem(framework_name)
        // cy.removeRoleFromPermissions(name)
        // cy.goToItem(report_name)
        // cy.removeRoleFromPermissions(name)
        // cy.goToItem(source_name)
        // cy.removeRoleFromPermissions(name)

        // // Admin should not see them anymore
        // cy.logOut()
        // cy.loginAsTestAdmin()
        // cy.itemDoesNotExist(framework_name)
        // cy.itemDoesNotExist(report_name)
        // cy.itemDoesNotExist(source_name)

      });
    });
  });
  // it("adding and removing org permissions works.", () => {
  //   cy.get("@orgName").then(orgName=> {
  //     cy.get("@orgAdminName").then(name=> {
  //       let word = chance.word();
  //       let teamName = `Team-${word}`;
  //       let framework_name = `framework-${word}`;
  //       let report_name = `report-${word}`;
  //       let source_name = `source-${word}`;
  //       cy.createFramework(framework_name);
  //       cy.createReport(report_name);
  //       cy.createSource(source_name);

  //       // Admin should not see any of these.
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.itemDoesNotExist(framework_name)
  //       cy.itemDoesNotExist(report_name)
  //       cy.itemDoesNotExist(source_name)

  //       // Add admin
  //       cy.logOut()
  //       cy.loginAsTestUser()
  //       cy.goToItem(framework_name)
  //       cy.addPermissionsReadWrite(orgName)
  //       cy.goToItem(report_name)
  //       cy.addPermissionsReadWrite(orgName)
  //       cy.goToItem(source_name)
  //       cy.addPermissionsReadWrite(orgName)

  //       // Admin should see all of these.
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.goToItem(framework_name)
  //       cy.get("[data-cy=framework]").should("be.visible")
  //       cy.goToItem(report_name)
  //       cy.get("[data-cy=report]").should("be.visible")
  //       cy.goToItem(source_name)
  //       cy.get("[data-cy=source]").should("be.visible")


  //       // Remove admin
  //       cy.logOut()
  //       cy.loginAsTestUser()
  //       cy.goToItem(framework_name)
  //       cy.removeRoleFromPermissions(orgName)
  //       cy.goToItem(report_name)
  //       cy.removeRoleFromPermissions(orgName)
  //       cy.goToItem(source_name)
  //       cy.removeRoleFromPermissions(orgName)

  //       // Admin should not see them anymore
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.itemDoesNotExist(framework_name)
  //       cy.itemDoesNotExist(report_name)
  //       cy.itemDoesNotExist(source_name)

  //     });
  //   });
  // });
  // it("adding and removing team permissions works.", () => {
  //   cy.get("@orgName").then(orgName=> {
  //     cy.get("@orgAdminName").then(name=> {
  //       let word = chance.word();
  //       let teamName = `Team-${word}`;
  //       let framework_name = `framework-${word}`;
  //       let report_name = `report-${word}`;
  //       let source_name = `source-${word}`;
  //       cy.createTeam(teamName)
  //       cy.addUserToTeam(teamName, name)

  //       cy.createFramework(framework_name);
  //       cy.createReport(report_name);
  //       cy.createSource(source_name);

  //       // Admin should not see any of these.
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.itemDoesNotExist(framework_name)
  //       cy.itemDoesNotExist(report_name)
  //       cy.itemDoesNotExist(source_name)

  //       // Add admin
  //       cy.logOut()
  //       cy.loginAsTestUser()
  //       cy.goToItem(framework_name)
  //       cy.addPermissionsReadWrite(teamName)
  //       cy.goToItem(report_name)
  //       cy.addPermissionsReadWrite(teamName)
  //       cy.goToItem(source_name)
  //       cy.addPermissionsReadWrite(teamName)

  //       // Admin should see all of these.
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.goToItem(framework_name)
  //       cy.get("[data-cy=framework]").should("be.visible")
  //       cy.goToItem(report_name)
  //       cy.get("[data-cy=report]").should("be.visible")
  //       cy.goToItem(source_name)
  //       cy.get("[data-cy=source]").should("be.visible")


  //       // Remove admin
  //       cy.logOut()
  //       cy.loginAsTestUser()
  //       cy.goToItem(framework_name)
  //       cy.removeRoleFromPermissions(teamName)
  //       cy.goToItem(report_name)
  //       cy.removeRoleFromPermissions(teamName)
  //       cy.goToItem(source_name)
  //       cy.removeRoleFromPermissions(teamName)

  //       // Admin should not see them anymore
  //       cy.logOut()
  //       cy.loginAsTestAdmin()
  //       cy.itemDoesNotExist(framework_name)
  //       cy.itemDoesNotExist(report_name)
  //       cy.itemDoesNotExist(source_name)

  //     });
  //   });
  // });
})
