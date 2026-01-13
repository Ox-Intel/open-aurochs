var word = chance.word()
var private_data = `P-${word}`
var personal_team = `Per-${word}`
var organization_data = `O-${word}`
var team_data = `T-${word}`
var team_name = `Team-${word}`
var orgName = "";

before(() => {
  cy.setupTestOrgAndUsers()
  cy.loginAsSuper()
  cy.get("@orgNormalUsername").then(username=> {
    cy.get("@orgName").then(organization_name=> {
      cy.addTeam(username, team_name, organization_name)
      cy.addTeam(username, personal_team, organization_name)
      orgName = organization_name;
      // cy.addTeam(username, orgName, organization_name)
    });
  });
  cy.logOut()
});
after(() => {
  cy.tearDownTestOrg()
});


function testMyLibraryFilter(cy, list_name,) {

    // Library Button should exist
    cy.get("[data-cy=nav-library]").should("be.visible")

    // Check that library page hasn't always been visible
    cy.get("[data-cy=library]").should("not.exist")

    // When Library button is clicked
    cy.get("[data-cy=nav-library]").click()

    // I should see a list of frameworks, reports, sources, and stacks
    cy.get("[data-cy=library]").should("be.visible")

    // The selectors should now be visible
    cy.get("[data-cy=shared-library-list]").should("be.visible")
    cy.get("[data-cy=my-library-list]").should("be.visible")

    // I should see the default framework sort option for each of
    // framework, report, source lists. It should say,
    // "All <data type>" where <data type> is either framework,
    // report, or source.
    cy.get(
      `[data-cy=${list_name}] [data-cy=filter] option:selected`
    ).should("have.text", "All")
    cy.get(
      "[data-cy=my-library-list] [data-cy=filter] option:selected"
    ).should("have.text", "All")

    

    // FRAMEWORKS
    // Add framework test data

    cy.createFramework("frame-" + private_data)
    cy.createFramework("frame-" + organization_data)
    cy.goToItem("frame-" + organization_data)
    cy.addPermissionsReadOnly(orgName)
    cy.goToLibrary()

    // Add source test data
    cy.createSource("source-" + private_data)
    cy.createSource("source-" + organization_data)
    cy.goToItem("source-" + organization_data)
    cy.addPermissionsReadOnly(orgName)
    cy.goToLibrary()

    // Add Stack test data
    cy.createStack("stack-" + private_data)
    cy.createStack("stack-" + organization_data)
    cy.goToItem("stack-" + organization_data)
    cy.addPermissionsReadOnly(orgName)
    cy.goToLibrary()

    // Add report test data
    cy.createReport("report-" + private_data)
    cy.createReport("report-" + organization_data)
    cy.goToItem("report-" + organization_data)
    cy.addPermissionsReadOnly(orgName)
    cy.goToLibrary()

    // cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // all filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "frame-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text","frame-" +  private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Private")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "frame-" + private_data)

    // Team filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Shared")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "frame-" + organization_data)

    // // My Personal Team filter
    // cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
    //   "Mine"
    // )
    // cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    // cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    // cy.get(
    //   `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    // ).should("have.text", organization_data)

    // SOURCES
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    // cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "source-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Private")
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + private_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Shared")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + organization_data)

    // // My Personal Team filter
    // cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
    //   "Mine"
    // )
    // cy.get(
    //   `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    // ).should("have.text", organization_data)

    // // STACKS
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    // cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "stack-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Private")
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + private_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Shared")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + organization_data)

    // // My Personal Team filter
    // cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
    //   "Mine"
    // )
    // cy.get(
    //   `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    // ).should("have.text", organization_data)

    // REPORTS
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    // cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=my-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "report-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Private")
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + private_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select("Shared")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + organization_data)

    // // My Personal Team filter
    // cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
    //   "Mine"
    // )
    // cy.get(
    //   `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    // ).should("have.text", organization_data)
}


describe("Confirm library filter", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()
      // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("should correctly filter items in my library, ", () => {
    testMyLibraryFilter(cy, "my-library-list")
  })
})
