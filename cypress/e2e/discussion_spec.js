

before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});


describe("discussions", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestAdmin()
  });
  
  it("should allow both normal users and admins to add comments", () => {
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
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))

      })
    })
  })
  it("should allow both normal users and admins to edit their comments", () => {
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
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          let editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.addComment(chance.sentence({words: 5}))
          editedComment = chance.sentence({words: 5})
          cy.editComment(editedComment)
          cy.get("[data-cy=comment] [data-cy=body]").contains(editedComment).should("be.visible")

      })
    })
  })

  it("should allow both normal users and admins to delete their comments", () => {
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
          cy.get("[data-cy=tab-discussion]").click()
          let comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-discussion]").click()
          comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          comment = chance.sentence({words: 5})
          cy.addComment(comment)
          cy.on('window:confirm', () => true);
          cy.get("[data-cy=delete-comment]").click()
          cy.get("[data-cy=comment]").contains(comment).should("not.exist")

      })
    })
  })
})
