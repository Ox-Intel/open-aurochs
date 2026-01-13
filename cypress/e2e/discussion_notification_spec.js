

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

  it("should trigger inbox notifications as expected", () => {
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
          cy.unfollowDiscussion()
          cy.followDiscussion()

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.unfollowDiscussion()
          cy.followDiscussion()

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.unfollowDiscussion()
          cy.followDiscussion()

          // Add a comment as a normal user.
          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(framework_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(report_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.addComment(chance.sentence({words: 5}))

          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.addComment(chance.sentence({words: 5}))

          cy.logOut()
          cy.loginAsTestAdmin()
          cy.get("[data-cy=inbox-count]").contains("3").should('be.visible')
          cy.get("[data-cy=inbox-count]").click()

          // Make sure the inbox works

          // Test content
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')

          // Test links
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(framework_name).should('be.visible').click()
          cy.get("[data-cy=framework]").should('be.visible')
          cy.get("[data-cy=inbox-count]").contains("2").should('be.visible')
          cy.get("[data-cy=inbox-count]").click()

          // ensure read/unread works
          cy.get("[data-cy=inbox-item]:nth-child(3) [data-cy=read-dot]").should('be.visible').click()
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=read-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(2) [data-cy=read-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(3) [data-cy=read-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=unread-dot]").should('be.visible').click()
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=unread-dot]").should('be.visible')
          cy.get("[data-cy=inbox-item]:nth-child(2) [data-cy=unread-dot]").should('be.visible')
          cy.get("[data-cy=inbox-item]:nth-child(3) [data-cy=unread-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(3) [data-cy=read-dot]").should('be.visible')

          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(report_name).should('be.visible').click()
          cy.get("[data-cy=report]").should('be.visible')
          cy.get("[data-cy=inbox-count]").contains("1").should('be.visible')
          cy.get("[data-cy=inbox-count]").click()

          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(source_name).should('be.visible').click()
          cy.get("[data-cy=source]").should('be.visible')
          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.get("[data-cy=nav-inbox]").click()

          // Test active/inactive
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=mark-done]").click()
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(framework_name).should('not.exist')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(report_name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(source_name).should('be.visible')

          cy.get("[data-cy=tab-done").click()
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(framework_name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(report_name).should('not.exist')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(source_name).should('not.exist')
          
          // ensure read/unread works
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=read-dot]").should('be.visible').click()
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=read-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=unread-dot]").should('be.visible').click()
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=unread-dot]").should('not.exist')
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=read-dot]").should('be.visible')

          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=mark-active]").click()
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(framework_name).should('not.exist')

          cy.get("[data-cy=tab-active").click()
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(framework_name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(report_name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(source_name).should('be.visible')
          

          // Ensure unfollow works
          cy.get("[data-cy=inbox-item] [data-cy=initiator]").contains(name).should('be.visible')
          cy.get("[data-cy=inbox-item] [data-cy=name]").contains(source_name).click()
          cy.get("[data-cy=tab-discussion]").click()
          cy.unfollowDiscussion()
          cy.get("[data-cy=inbox-count]").should('not.exist')

          cy.logOut()
          cy.loginAsTestUser()
          cy.goToItem(source_name)
          cy.get("[data-cy=tab-discussion]").click()
          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.addComment(chance.sentence({words: 5}))
          cy.logOut()
          cy.loginAsTestAdmin()


          cy.get("[data-cy=inbox-count]").should('not.exist')
          cy.get("[data-cy=nav-inbox]").click()
          cy.get("[data-cy=inbox-item]:nth-child(1) [data-cy=read-dot]").should('be.visible')

      })
    })
  })
})
