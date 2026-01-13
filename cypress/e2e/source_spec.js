var num_criteria = 2
var num_framework = 1
// Generate framework list

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("sources", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("can be created and edited", () => {
    var word = chance.word()
    var source_name = "Source - " + word
    var subtitle = chance.sentence()
    cy.createSource(source_name, null, subtitle)
    cy.goToItem(source_name)

    var new_source_name = "Source - " + word
    var new_subtitle = chance.sentence()

    cy.get("[data-cy=edit]").click()
    cy.get("[data-cy=input-source-name]").clear()
    cy.wait(5)
    cy.get("[data-cy=input-source-name]").type(new_source_name)
    cy.get("[data-cy=input-source-subtitle]").clear()
    cy.wait(5)
    cy.get("[data-cy=input-source-subtitle]").type(new_subtitle)
    cy.get("[data-cy=save]").click()
    cy.get("[data-cy=save].saving").should('not.exist')

    cy.goToLibrary()
    cy.get("[data-cy=library-feed-item]").contains(new_source_name).should("be.visible")

    cy.goToItem(new_source_name)
    cy.get("[data-cy=source] [data-cy=name]").contains(new_source_name).should('be.visible')
    cy.get("[data-cy=source] [data-cy=subtitle]").contains(new_subtitle).should('be.visible');
  });
  it("lists the right reports", () => {
    var word = chance.word()
    var source_name = "Source - " + word
    var report_name = "Report - " + word
    var report2_name = "Report2 - " + word
    var subtitle = chance.sentence()
    cy.createSource(source_name, null, subtitle)
    cy.goToItem(source_name)
    cy.createReport(report_name)
    cy.addSourceToReport(report_name, source_name)
    cy.get("[data-cy=report] [data-cy=source-list] [data-cy=name]").contains(source_name).should("be.visible")
    cy.on('window:confirm', () => true);
    cy.get("[data-cy=remove-source]").click()

    cy.get("[data-cy=report] [data-cy=source-list] [data-cy=name]").should("not.exist")
    cy.addSourceToReport(report_name, source_name)
    cy.get("[data-cy=report] [data-cy=source-list] [data-cy=name]").contains(source_name).should("be.visible")


    cy.goToItem(source_name)
    cy.get("[data-cy=source] [data-cy=tab-reports]").click()
    cy.get("[data-cy=source] [data-cy=report-list] [data-cy=name]").contains(report_name).should("be.visible").click()

    cy.get("[data-cy=report] [data-cy=tab-sources]").click()
    cy.get("[data-cy=report] [data-cy=source-list] [data-cy=name]").contains(source_name).should("be.visible")
  })
  
})
