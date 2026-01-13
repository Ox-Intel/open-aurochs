

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("notess", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestAdmin()
  });
  
  it("should allow both normal users and admins to add notes", () => {
    cy.get('@orgNormalName').then(name => {
        cy.get('@orgAdminUsername').then(admin_username => {
          var word = chance.word({ length: 15 })

          var framework_name = "F" + word
          var report_name = "R" + word
          var source_name = "S" + word

          // Add Objects
          cy.createFramework(framework_name)
          cy.goToItem(framework_name)
          cy.addPermissionsAdmin(name)
          cy.createReport(report_name)
          cy.goToItem(report_name)
          cy.addPermissionsAdmin(name)
          cy.createSource(source_name)
          cy.goToItem(source_name)
          cy.addPermissionsAdmin(name)

          // Add a comment as an admin.
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.editNotes(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.editNotes(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.editNotes(chance.sentence({words: 5}))

      })
    })
  })
  it("should prevent me from adding notes if I can't edit or admin.", () => {
    cy.get('@orgNormalName').then(name => {
        cy.get('@orgAdminUsername').then(admin_username => {
          var word = chance.word({ length: 15 })

          var framework_name = "F" + word
          var report_name = "R" + word
          var source_name = "S" + word

          // Add Objects
          cy.createFramework(framework_name)
          cy.goToItem(framework_name)
          cy.addPermissionsReadOnly(name)
          cy.createReport(report_name)
          cy.goToItem(report_name)
          cy.addPermissionsReadOnly(name)
          cy.createSource(source_name)
          cy.goToItem(source_name)
          cy.addPermissionsReadOnly(name)

          // Add a comment as an admin.
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.addNotes(chance.sentence({words: 5}))

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.get("[data-cy=add-notes]").should("not.exist")
          cy.get("[data-cy=edit-notes]").should("not.exist")
          cy.get("[data-cy=editing-notes] .ql-editor").should("not.exist")
          cy.get("[data-cy=view-notes] .ql-editor").should("be.visible")

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.get("[data-cy=add-notes]").should("not.exist")
          cy.get("[data-cy=edit-notes]").should("not.exist")
          cy.get("[data-cy=editing-notes] .ql-editor").should("not.exist")
          cy.get("[data-cy=view-notes] .ql-editor").should("be.visible")

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-notes]").click()
          cy.get("[data-cy=add-notes]").should("not.exist")
          cy.get("[data-cy=edit-notes]").should("not.exist")
          cy.get("[data-cy=editing-notes] .ql-editor").should("not.exist")
          cy.get("[data-cy=view-notes] .ql-editor").should("be.visible")

      })
    })
  })

})
