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
  it("admin can do all the things.", () => {
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

        // Add permissions
        cy.goToItem(framework_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(report_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(source_name)
        cy.addPermissionsAdmin(name)

        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(framework_name)
        cy.get("[data-cy=framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=clone-framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=download-csv]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=delete]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=add-tag]").should("be.visible")

        cy.goToItem(report_name)
        cy.get("[data-cy=report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=download-report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=save-permissions]").should("be.visible")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=delete]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=add-tag]").should("be.visible")
        // Check tabs
        cy.get("[data-cy=report] [data-cy=tab-overview]").click()
        cy.get("[data-cy=report] [data-cy=overview-panel]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-permissions]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
        cy.get("[data-cy=report] [data-cy=scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=scorecards] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=no-permissions]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=tab-sources]").click()
        cy.get("[data-cy=report] [data-cy=source-list]").should("exist")
        cy.get("[data-cy=report] [data-cy=source-list] [data-cy=add-source]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=tab-discussion]").click()
        cy.get("[data-cy=report] [data-cy=discussion]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=discussion] [data-cy=save-comment]").should("be.visible")
        

        cy.goToItem(source_name)
        cy.get("[data-cy=source]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=delete]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=add-tag]").should("be.visible")
      });
    });
    cy.logOut()
  });
  it("edit allows scoring, viewing, and editing.", () => {
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

        // Add permissions
        cy.goToItem(framework_name)
        cy.addPermissionsWrite(name)
        cy.goToItem(report_name)
        cy.addPermissionsWrite(name)
        cy.goToItem(source_name)
        cy.addPermissionsWrite(name)

        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(framework_name)
        cy.get("[data-cy=framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=clone-framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=download-csv]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=framework] [data-cy=add-tag]").should("be.visible")

        cy.goToItem(report_name)
        cy.get("[data-cy=report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=download-report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-tag]").should("be.visible")

        // Check tabs
        cy.get("[data-cy=report] [data-cy=tab-overview]").click()
        cy.get("[data-cy=report] [data-cy=overview-panel]").should("exist")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-permissions]").should("not.exist")
        
        cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
        cy.get("[data-cy=report] [data-cy=scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=scorecards] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=no-permissions]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=tab-sources]").click()
        cy.get("[data-cy=report] [data-cy=source-list]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=source-list] [data-cy=add-source]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=tab-discussion]").click()
        cy.get("[data-cy=report] [data-cy=discussion]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=discussion] [data-cy=save-comment]").should("be.visible")
        
        cy.goToItem(source_name)
        cy.get("[data-cy=source]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=edit]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=source] [data-cy=add-tag]").should("be.visible")
      });
    });
    cy.logOut()
  }); 

  it("read only allows only view things.", () => {
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

        // Add permissions
        cy.goToItem(framework_name)
        cy.addPermissionsReadOnly(name)
        cy.goToItem(report_name)
        cy.addPermissionsReadNoScore(name)
        cy.goToItem(source_name)
        cy.addPermissionsReadOnly(name)

        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(framework_name)
        cy.get("[data-cy=framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=edit]").should("not.exist")
        cy.get("[data-cy=framework] [data-cy=clone-framework]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=download-csv]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=framework] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=framework] [data-cy=add-tag]").should("not.exist")

        cy.goToItem(report_name)
        cy.get("[data-cy=report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=edit]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-scorecard]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=download-report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-tag]").should("not.exist")

        // Check tabs
        cy.get("[data-cy=report] [data-cy=tab-overview]").click()
        cy.get("[data-cy=report] [data-cy=overview-panel]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-permissions]").should("not.exist")
        

        cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
        // cy.get("[data-cy=report] [data-cy=scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=no-permissions]").should("exist")
        cy.get("[data-cy=report] [data-cy=scorecards] [data-cy=add-scorecard]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=tab-sources]").click()
        cy.get("[data-cy=report] [data-cy=source-list]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=source-list] [data-cy=add-source]").should("not.exist")

        cy.get("[data-cy=report] [data-cy=tab-discussion]").click()
        cy.get("[data-cy=report] [data-cy=discussion]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=discussion] [data-cy=save-comment]").should("be.visible")
        
        cy.goToItem(source_name)
        cy.get("[data-cy=source]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=edit]").should("not.exist")
        cy.get("[data-cy=source] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=source] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=source] [data-cy=add-tag]").should("not.exist")
      });
      cy.logOut()
    });
  });
  it("score only for reports allows scoring for reports.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        // cy.createFramework(framework_name);
        cy.createReport(report_name);
        // cy.createSource(source_name);

        // Add permissions
        cy.goToItem(report_name)
        cy.addPermissionsScoreOnly(name)
        
        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(report_name)
        cy.get("[data-cy=report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=edit]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=download-report]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-tag]").should("not.exist")

        // Check tabs
        cy.get("[data-cy=report] [data-cy=tab-overview]").click()
        cy.get("[data-cy=report] [data-cy=overview-panel]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-permissions]").should("not.exist")
        
        cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
        cy.get("[data-cy=report] [data-cy=scorecards]").should("be.visible")
        // cy.get("[data-cy=report] [data-cy=no-permissions]").should("exist")
        cy.get("[data-cy=report] [data-cy=scorecards] [data-cy=add-scorecard]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=tab-sources]").click()
        cy.get("[data-cy=report] [data-cy=source-list]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=source-list] [data-cy=add-source]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=tab-discussion]").click()
        cy.get("[data-cy=report] [data-cy=discussion]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=discussion] [data-cy=save-comment]").should("be.visible")

      });
    });
    cy.logOut()
  }); 

  it("score and read for reports allows scoring for reports and source adding.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        // cy.createFramework(framework_name);
        cy.createReport(report_name);

        // Add permissions
        cy.goToItem(report_name)
        cy.addPermissionsReadOnly(name)
        
        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.createSource(source_name);
        cy.goToItem(report_name)
        cy.get("[data-cy=report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=edit]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-scorecard]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=download-report]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").should("not.exist")
        cy.get("[data-cy=permissions] [data-cy=read-only-permissions]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=delete]").should("not.exist")
        cy.get("[data-cy=report] [data-cy=add-tag]").should("not.exist")

        // Check tabs
        cy.get("[data-cy=report] [data-cy=tab-overview]").click()
        cy.get("[data-cy=report] [data-cy=overview-panel]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-scorecards]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=overview-panel] [data-cy=no-permissions]").should("not.exist")
        
        cy.get("[data-cy=report] [data-cy=tab-scorecards]").click()
        cy.get("[data-cy=report] [data-cy=scorecards]").should("be.visible")
        // cy.get("[data-cy=report] [data-cy=no-permissions]").should("exist")
        cy.get("[data-cy=report] [data-cy=scorecards] [data-cy=add-scorecard]").should("be.visible")

        cy.get("[data-cy=report] [data-cy=tab-sources]").click()
        cy.get("[data-cy=report] [data-cy=source-list]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=source-list] [data-cy=add-source]").should("be.visible")

        cy.addSourceToReport(report_name, source_name)


        cy.get("[data-cy=report] [data-cy=tab-discussion]").click()
        cy.get("[data-cy=report] [data-cy=discussion]").should("be.visible")
        cy.get("[data-cy=report] [data-cy=discussion] [data-cy=save-comment]").should("be.visible")

      });
    });
    cy.logOut()
  }); 
  it("score isn't an option for frameworks and sources.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        cy.createFramework(framework_name);
        cy.createSource(source_name);

        // Add permissions
        cy.goToItem(framework_name)
        cy.addPermissionsAdmin(name)
        cy.goToItem(source_name)
        cy.addPermissionsAdmin(name)

        // Admin should see all of these.
        cy.logOut()
        cy.loginAsTestAdmin()
        cy.goToItem(framework_name)
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=can-score]").should("not.exist")

        cy.goToItem(source_name)
        cy.get("[data-cy=tab-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=edit-permissions]").click()
        cy.get("[data-cy=permissions] [data-cy=can-score]").should("not.exist")

      });
    });
    cy.logOut()
  }); 


})
