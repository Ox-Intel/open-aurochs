before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});

function testSorting(cy, list_type, list_suffix, library_feed) {

    // Updated
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=sort]").select("Updated Date")
    
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "B" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)

    // Alphabetical (Z -> A)
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=sort]").select("Name")
    
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "B" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)

    // Alphabetical (A -> Z)
    
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=up-arrow]").click()
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=down-arrow]").should("be.visible")

    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "B" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)

    // Created ⬇
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=sort]").select("Created Date")
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "B" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    

    // Created ⬆
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=down-arrow]").click()
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=up-arrow]").should("be.visible")
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "B" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)
    

    // Modifes "B" name so that it's the most recently modified item //
    cy.get(`[data-cy=${library_feed}-list]`)
      .get(`[data-cy=item-name]`)
      .contains("B" + list_suffix)
      .click()
    cy.get("[data-cy=edit]").click()
    cy.get(`[data-cy=input-${list_type}-name]`).type(" most recently modified")
    cy.get("[data-cy=save]").click()
    cy.get("[data-cy=save].saving").should('not.exist')
    cy.goToLibrary()
    // End data modification //

    

    // Updated
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=sort]").select("Updated Date")

    // Updated ⬆ by default    
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should(
      "have.text",
      "B" + list_suffix + " most recently modified"
    )
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)

    // Updated ⬇
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=up-arrow]").click()
    cy.get("[data-cy=" + library_feed + "-list] [data-cy=down-arrow]").should("be.visible")
    
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(1) [data-cy=item-name]"
    ).should("have.text", "A" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(2) [data-cy=item-name]"
    ).should("have.text", "C" + list_suffix)
    cy.get(
      "[data-cy=" + library_feed + "-list] [data-cy=library-feed-item]:nth-child(3) [data-cy=item-name]"
    ).should(
      "have.text",
      "B" + list_suffix + " most recently modified"
    )
};
function createDataAndTest(cy, object_type, library, orgName) {
    // Library Button should exist
    cy.get("a[data-cy=nav-library]").should("be.visible")

    // Check that library page hasn't always been visible
    cy.get("[data-cy=library]").should("not.exist")

    // When Library button is clicked
    cy.get("a[data-cy=nav-library]").click()

    // I should see a list of frameworks, reports, and sources page
    cy.get("[data-cy=library]").should("be.visible")

    // The selectors should now be visible
    cy.get("[data-cy=shared-library-list] [data-cy=sort]").should("be.visible")
    cy.get("[data-cy=my-library-list] [data-cy=sort]").should("be.visible")

    // I should see that the default dropdown sort option for each of report,
    // framework, and source list has text: "Updated ⬇")
    cy.get("[data-cy=shared-library-list] [data-cy=sort] option:selected").should(
      "have.text",
      "Created Date"
    )
    cy.get("[data-cy=shared-library-list] [data-cy=up-arrow]").should("be.visible")
    cy.get("[data-cy=my-library-list] [data-cy=sort] option:selected").should(
      "have.text",
      "Created Date"
    )
    cy.get("[data-cy=my-library-list] [data-cy=up-arrow]").should("be.visible")

    const obj_suffix = chance.sentence({ words: 2 })

    // FRAMEWORKS
    // Add framework test data
    cy[`create${object_type[0].toUpperCase() + object_type.substring(1)}`]("A" + obj_suffix, orgName)
    cy[`create${object_type[0].toUpperCase() + object_type.substring(1)}`]("B" + obj_suffix, orgName)
    cy[`create${object_type[0].toUpperCase() + object_type.substring(1)}`]("C" + obj_suffix, orgName)
    cy.goToLibrary()


    testSorting(cy, object_type, obj_suffix, library)
    cy.goToItem("A" + obj_suffix)
    
    cy.deleteObject("A" + obj_suffix)
    cy.goToItem("B" + obj_suffix)
    
    cy.deleteObject("B" + obj_suffix)
    cy.goToItem("C" + obj_suffix)
    
    cy.deleteObject("C" + obj_suffix)
}


describe("Library sorting works", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });
  it("for frameworks in my library", () => {
    cy.get("@orgName").then(orgName=> {
      // createDataAndTest(cy, 'framework', 'my-library', orgName)
      createDataAndTest(cy, 'framework', 'my-library')
    });
  });
  it("for reports in my library", () => {
    cy.get("@orgName").then(orgName=> {
      // createDataAndTest(cy, 'report', 'my-library', orgName)
      createDataAndTest(cy, 'report', 'my-library')
    });
  });
  it("for sources in my library", () => {
    cy.get("@orgName").then(orgName=> {
      // createDataAndTest(cy, 'source', 'my-library', orgName)
      createDataAndTest(cy, 'source', 'my-library')
    });
  });
  it("for stacks in my library", () => {
    cy.get("@orgName").then(orgName=> {
      // createDataAndTest(cy, 'stack', 'my-library', orgName)
      createDataAndTest(cy, 'stack', 'my-library')
    });
  });
  // it("in the shared library", () => {
  //   cy.get("@orgName").then(orgName=> {
  //     // Create as user

  //     // Library Button should exist
  //     cy.get("a[data-cy=nav-library]").should("be.visible")

  //     // Check that library page hasn't always been visible
  //     cy.get("[data-cy=library]").should("not.exist")

  //     // When Library button is clicked
  //     cy.get("a[data-cy=nav-library]").click()

  //     // I should see a list of frameworks, reports, and sources page
  //     cy.get("[data-cy=library]").should("be.visible")

  //     // The selectors should now be visible
  //     cy.get("[data-cy=shared-library-list] [data-cy=sort]").should("be.visible")
  //     cy.get("[data-cy=my-library-list] [data-cy=sort]").should("be.visible")

  //     // I should see that the default dropdown sort option for each of report,
  //     // framework, and source list has text: "Updated ⬇")
  //     cy.get("[data-cy=shared-library-list] [data-cy=sort] option:selected").should(
  //       "have.text",
  //       "Created Date"
  //     )
  //     cy.get("[data-cy=shared-library-list] [data-cy=up-arrow]").should("be.visible")
  //     cy.get("[data-cy=my-library-list] [data-cy=sort] option:selected").should(
  //       "have.text",
  //       "Created Date"
  //     )
  //     cy.get("[data-cy=my-library-list] [data-cy=up-arrow]").should("be.visible")

  //     const framework_suffix = chance.sentence({ words: 2 })
  //     const source_suffix = chance.sentence({ words: 2 })
  //     const report_suffix = chance.sentence({ words: 2 })
  //     const stack_suffix = chance.sentence({ words: 2 })

  //     // FRAMEWORKS
  //     // Add framework test data
  //     cy.createFramework("A" + framework_suffix, orgName)
  //     cy.createFramework("B" + framework_suffix, orgName)
  //     cy.createFramework("C" + framework_suffix, orgName)
  //     cy.goToLibrary()


  //     testSorting(cy, 'framework', framework_suffix, 'shared-library')

  //     // SOURCES
  //     // Add source test data
  //     cy.createSource("A" + source_suffix, "oldest", orgName)
  //     cy.createSource("B" + source_suffix, "middle", orgName)
  //     cy.createSource("C" + source_suffix, "newest", orgName)
  //     cy.goToLibrary()
      
  //     testSorting(cy, 'source', source_suffix, 'shared-library')

  //     // REPORTS
  //     // Add report test data
  //     cy.createReport("A" + report_suffix, orgName)
  //     cy.createReport("B" + report_suffix, orgName)
  //     cy.createReport("C" + report_suffix, orgName)
  //     cy.goToLibrary()

  //     testSorting(cy, 'report', report_suffix, 'shared-library')

  //     // STACKS
  //     // Add stack test data
  //     cy.createStack("A" + stack_suffix, orgName)
  //     cy.createStack("B" + stack_suffix, orgName)
  //     cy.createStack("C" + stack_suffix, orgName)
  //     cy.goToLibrary()

  //     testSorting(cy, 'stack', stack_suffix, 'shared-library')

  //     cy.logOut()
  //     // Check as admin
  //     cy.loginAsTestAdmin()
  //     testSorting(cy, 'framework', framework_suffix, 'shared-library')
  //     testSorting(cy, 'source', source_suffix, 'shared-library')
  //     testSorting(cy, 'report', report_suffix, 'shared-library')
  //     testSorting(cy, 'stack', stack_suffix, 'shared-library')
  //   });
  // });
})