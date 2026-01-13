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
  it("navigating to a non-existent object should give the not found message.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(name=> {
        let word = chance.word();
        cy.visit(Cypress.env("APP_URL") + `/report/${word}`)
        cy.get("[data-cy=not-found]").should("be.visible");

        cy.visit(Cypress.env("APP_URL") + `/framework/${word}`)
        cy.get("[data-cy=not-found]").should("be.visible");

        cy.visit(Cypress.env("APP_URL") + `/source/${word}`)
        cy.get("[data-cy=not-found]").should("be.visible");

        cy.visit(Cypress.env("APP_URL") + `/stack/${word}`)
        cy.get("[data-cy=not-found]").should("be.visible");
      })
    })
  })

  it("navigating to an object I don't have permissions to should tell it doesn't exist.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgNormalName").then(name=> {
        let word = chance.word();
        let teamName = `Team-${word}`;
        let framework_name = `framework-${word}`;
        let report_name = `report-${word}`;
        let source_name = `source-${word}`;
        let stack_name = `stack-${word}`;
        cy.createFramework(framework_name);
        cy.createReport(report_name);
        cy.createSource(source_name);
        cy.createStack(stack_name);

        // Add permissions
        cy.goToItem(framework_name)
        let url_framework = ""
        cy.location().then((loc) => {
          cy.log(loc.href.toString())
          url_framework = loc.href.toString()
          cy.log(url_framework)
          cy.goToItem(report_name)
          let url_report = ""
          cy.location().then((loc) => {
            cy.log(loc.href.toString())
            url_report = loc.href.toString()
            cy.log(url_report)
            cy.goToItem(source_name)
            let url_source = ""
            cy.location().then((loc) => {
              cy.log(loc.href.toString())
              url_source = loc.href.toString()
              cy.log(url_source)
              cy.goToItem(stack_name)
              let url_stack = ""
              cy.location().then((loc) => {
                cy.log(loc.href.toString())
                url_stack = loc.href.toString()

                cy.log(url_stack) 

                // Admin should see all of these.
                cy.logOut()
                cy.loginAsTestAdmin()

                cy.log(url_report)
                cy.visit(url_report)
                cy.get("[data-cy=not-found]").should("be.visible");

                cy.visit(url_framework)
                cy.get("[data-cy=not-found]").should("be.visible");

                cy.visit(url_source)
                cy.get("[data-cy=not-found]").should("be.visible");

                cy.visit(url_stack)
                cy.get("[data-cy=not-found]").should("be.visible");
                
              })



            })
          })
        })
      });
    });
  }); 

  it("navigating to an report or framework I don't have permissions but can see the stack to should tell me and list the admin.", () => {
    cy.get("@orgName").then(orgName=> {
      cy.get("@orgAdminName").then(adminName=> {
        cy.get("@orgNormalName").then(name=> {
          let word = chance.word();
          let teamName = `Team-${word}`;
          let framework_name = `framework-${word}`;
          let report_name = `report-${word}`;
          let source_name = `source-${word}`;
          let stack_name = `stack-${word}`;
          cy.createReport(report_name);

          // Add framework, scorecards
          let num_criteria = 2
          let num_framework = 1
          let framework_list = []

          for (var i = 0; i < num_framework; i++) {
            // Generate criteria list for each framework
            var criteria_list = []
            var start_score;
            for (var j = 0; j < num_criteria; j++) {
              if (criteria_list.length < 1) {
                start_score = 1;
              } else {
                start_score = criteria_list[criteria_list.length - 1].score;
              }
              criteria_list.push({
                name: `criteria-${j}-${word}`,
                subtitle: "subtitle",
                weight: start_score * num_criteria,
                score: start_score + chance.integer({ min: 1, max: num_criteria }),
                comment: chance.sentence({words: 5}),
              })
            }

            framework_list.push({
              name: `framework-${i}-${word}`,
              criteria: criteria_list,
            })
          }

          framework_list.map((framework) => {
            cy.createFramework(framework.name)
            cy.addCriteriaToEmptyFramework(framework.name, framework.criteria)
            cy.goToItem(report_name)
            cy.addScorecards(report_name, framework.name, framework.criteria)
          })

          cy.createStack(stack_name);
          cy.addReportToStack(stack_name, report_name,)
          cy.goToItem(stack_name)
          cy.addPermissionsReadWrite(adminName)

          // Add permissions
          cy.goToItem(framework_list[0].name)
          let url_framework = ""
          cy.location().then((loc) => {
            cy.log(loc.href.toString())
            url_framework = loc.href.toString()
            cy.log(url_framework)
            cy.goToItem(report_name)
            let url_report = ""
            cy.location().then((loc) => {
              cy.log(loc.href.toString())
              url_report = loc.href.toString()
              cy.log(url_report)
            
              cy.goToItem(stack_name)
              let url_stack = ""
              cy.location().then((loc) => {
                cy.log(loc.href.toString())
                url_stack = loc.href.toString()

                cy.log(url_stack) 

                // Admin should see all of these.
                cy.logOut()
                cy.loginAsTestAdmin()

                cy.log(url_report)
                cy.visit(url_report)
                cy.get("[data-cy=not-found]").should("be.visible");
                cy.get("[data-cy=not-found]").contains(name).should("be.visible");

                cy.visit(url_framework)
                cy.get("[data-cy=not-found]").should("be.visible");
                cy.get("[data-cy=not-found]").contains(name).should("be.visible");


                cy.visit(url_stack)
                cy.get("[data-cy=not-found]").should("not.exist");

                cy.get("[data-cy=report-0] [data-cy=name]").click()
                cy.get("[data-cy=not-found]").should("be.visible");
                cy.get("[data-cy=not-found]").contains(name).should("be.visible");                
                
              })
            })
          })
        });
      });
    });
  }); 

})
