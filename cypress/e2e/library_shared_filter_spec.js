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

function testSharedLibraryFilter(cy, list_name, orgName) {

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
    cy.createFramework("framework-" + private_data, personal_team)
    cy.createFramework("framework-" + organization_data, orgName)
    cy.createFramework("framework-" + team_data, team_name)
    cy.goToLibrary()

    // SOURCES
    // Add source test data
    cy.createSource("source-" + private_data, personal_team)
    cy.createSource("source-" + organization_data, orgName)
    cy.createSource("source-" + team_data, team_name)

    // Add Stack test data
    cy.createStack("stack-" + private_data, personal_team)
    cy.createStack("stack-" + organization_data, orgName)
    cy.createStack("stack-" + team_data, team_name)

    // Add report test data
    cy.createReport("report-" + private_data, personal_team)
    cy.createReport("report-" + organization_data, orgName)
    cy.createReport("report-" + team_data, team_name)


    cy.goToLibrary()
    // cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // all filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "framework-" + team_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "framework-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]`
    ).should("have.text", "framework-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
      orgName
    )
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "framework-" + organization_data)

    // Team filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(team_name)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "framework-" + team_data)


    // SOURCE
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    // cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()
    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + team_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "source-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]`
    ).should("have.text", "source-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(orgName)
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + organization_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(team_name)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "source-" + team_data)


    // // STACKS
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    // cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + team_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "stack-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]`
    ).should("have.text", "stack-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(orgName)
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + organization_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(team_name)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "stack-" + team_data)


    // REPORTS
    cy.goToDashboard()
    cy.goToLibrary()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-framework]").click()
    // cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-report]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-stack]").click()
    cy.get("[data-cy=shared-library-list] [data-cy=library-filter] [data-cy=filter-source]").click()

    // All filter
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + team_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]`
    ).should("have.text", "report-" + organization_data)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]`
    ).should("have.text", "report-" + private_data)

    // Organization filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(
      orgName
    )
    cy.get(`[data-cy=${list_name}] [data-cy=up-arrow]`).click()
    cy.get(`[data-cy=${list_name}] [data-cy=down-arrow]`).should("be.visible")
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + organization_data)

    // Team A filter
    cy.get(`[data-cy=${list_name}] [data-cy=filter]`).select(team_name)
    cy.get(
      `[data-cy=${list_name}] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]`
    ).should("have.text", "report-" + team_data)

}


describe("Confirm library filter", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()
      // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("should correctly filter items in the shared library, ", () => {
    cy.get("@orgName").then(orgName=> {
      testSharedLibraryFilter(cy, "shared-library-list", orgName);
    })
  })
})
