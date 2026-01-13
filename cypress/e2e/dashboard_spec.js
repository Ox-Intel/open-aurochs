var word = chance.word()
var num_to_create = 6


before(() => {
  cy.setupTestOrgAndUsers()
});
after(() => {
  cy.tearDownTestOrg()
});
describe("The dashboard", () => {
  beforeEach(function() {
    cy.ensureOrgAndUsers(this)
    cy.loginAsTestUser()  // or cy.loginAsTestAdmin()
    // cy.logOut()
  });

  it("should display recent reports, frameworks, and stacks.", () => {
    cy.loginAsTestUser()
    cy.get("@orgName").then(orgName=> {
      
      // adds data
      let frameworks = []
      let reports = []
      let stacks = []
      for (let i=0; i<num_to_create; i++) {
        let framework_name = chance.sentence({words: 3})
        let report_name = chance.sentence({words: 3})
        let stack_name = chance.sentence({words: 3})

        cy.createFramework(framework_name)
        frameworks.push(framework_name)
        cy.createReport(report_name)
        reports.push(report_name)
        cy.createStack(stack_name)
        stacks.push(stack_name)
      }

      cy.goToDashboard()
      for (let i=1; i<=num_to_create; i++) {
        cy.goToDashboard()
        cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-${num_to_create - i}]`).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-${num_to_create - i}] [data-cy=item-name]`).contains(frameworks[i-1]).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-${num_to_create - i}]`).click();
        cy.get(`[data-cy=dashboard]`).should("not.exist");
        cy.get(`[data-cy=framework]`).should("be.visible");
        cy.get(`[data-cy=framework] h1`).contains(frameworks[i-1]).should('be.visible');

        cy.goToDashboard()
        cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-${num_to_create - i}]`).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-${num_to_create - i}] [data-cy=item-name]`).contains(reports[i-1]).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-${num_to_create - i}]`).click();
        cy.get(`[data-cy=dashboard]`).should("not.exist");
        cy.get(`[data-cy=report]`).should("be.visible");
        cy.get(`[data-cy=report] h1`).contains(reports[i-1]).should('be.visible');

        cy.goToDashboard()
        cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-${num_to_create - i}]`).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-${num_to_create - i}] [data-cy=item-name]`).contains(stacks[i-1]).should('exist');
        cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-${num_to_create - i}]`).click();
        cy.get(`[data-cy=dashboard]`).should("not.exist");
        cy.get(`[data-cy=stack]`).should("be.visible");
        cy.get(`[data-cy=stack] h1`).contains(stacks[i-1]).should('be.visible');
      }
    });
  })

  it("should allow pinning.", () => {
    cy.loginAsTestAdmin()
    cy.get("@orgName").then(orgName=> {
      
      // adds data
      let frameworks = []
      let reports = []
      let stacks = []
      for (let i=0; i<4; i++) {
        let framework_name = chance.sentence({words: 3})
        let report_name = chance.sentence({words: 3})
        let stack_name = chance.sentence({words: 3})

        cy.createFramework(framework_name)
        frameworks.push(framework_name)
        cy.createReport(report_name)
        reports.push(report_name)
        cy.createStack(stack_name)
        stacks.push(stack_name)
      }

      cy.goToDashboard()
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-pinned]`).should("not.exist")
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-2] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-pinned]`).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-pinned] [data-cy=item-name]`).contains(frameworks[1]).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-pinned] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=frameworks] [data-cy=ox-object-framework-pinned]`).should("not.exist")

      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-pinned]`).should("not.exist")
      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-2] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-pinned]`).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-pinned] [data-cy=item-name]`).contains(reports[1]).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-pinned] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=reports] [data-cy=ox-object-report-pinned]`).should("not.exist")

      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-pinned]`).should("not.exist")
      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-2] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-pinned]`).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-pinned] [data-cy=item-name]`).contains(stacks[1]).should("be.visible")
      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-pinned] [data-cy=pin]`).click()
      cy.get(`[data-cy=dashboard] [data-cy=stacks] [data-cy=ox-object-stack-pinned]`).should("not.exist")
    });
  })
  it("should allow new items to be created.", () => {
    let framework_name = chance.sentence({words: 3})
    let report_name = chance.sentence({words: 3})
    let stack_name = chance.sentence({words: 3})
    cy.loginAsTestUser()

    cy.goToDashboard()
    cy.get("[data-cy=dashboard] [data-cy=new-framework]").click()
    cy.get("[data-cy=input-framework-name]").clear().type(framework_name)
    cy.get("[data-cy=framework] [data-cy=save]").click()
    cy.get("[data-cy=framework] [data-cy=save].saving").should('not.exist')

    // Make sure it's there.
    cy.goToLibrary()
    cy.get("[data-cy=library-feed-item]")
      .contains(framework_name)
      .should("be.visible")

    cy.goToDashboard()
    cy.get("[data-cy=dashboard] [data-cy=new-report]").click()
    cy.get("[data-cy=input-report-name]").clear().type(report_name)
    cy.get("[data-cy=report] [data-cy=save]").click()
    cy.get("[data-cy=report] [data-cy=save].saving").should('not.exist')

    // Make sure it's there.
    cy.goToLibrary()
    cy.get("[data-cy=library-feed-item]")
      .contains(report_name)
      .should("be.visible")

    cy.goToDashboard()
    cy.get("[data-cy=dashboard] [data-cy=new-stack]").click()
    cy.get("[data-cy=input-stack-name]").clear().type(stack_name)
    cy.get("[data-cy=stack] [data-cy=save]").click()
    cy.get("[data-cy=stack] [data-cy=save].saving").should('not.exist')

    // Make sure it's there.
    cy.goToLibrary()
    cy.get("[data-cy=library-feed-item]")
      .contains(stack_name)
      .should("be.visible")
  })
})
