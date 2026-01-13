var word = chance.word({ length: 15 })

var framework_name = "F" + word
var report_name = "R" + word
var source_name = "S" + word

var framework_tag = "FT" + word
var report_tag = "RT" + word
var source_tag = "ST" + word


before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("tags can be added to frameworks, reports, and sources and link to library objects properly", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestAdmin()
  });
  
  it("should correctly display tags and click tags should show a filtered list of objects with that tag", () => {
    
    // Add Tags
    cy.createFramework(framework_name)
    cy.addTags(framework_name, [framework_tag])

    cy.createReport(report_name)
    cy.addTags(report_name, [framework_tag, report_tag])

    cy.createSource(source_name)
    cy.addTags(source_name, [framework_tag, report_tag, source_tag])

    // Remove Tags and check that clicking on removed tag makes the source object not appear
    cy.removeTags(source_name, [framework_tag])

    cy.goToDashboard()
    cy.get("[data-cy=nav-search-box]")
      .type(framework_tag)
    cy.get("[data-cy=nav-search-results]")
      .find("div")
      .contains(source_name)
      .should("not.exist")
  })
})
