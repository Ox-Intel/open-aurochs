from .framework import (
    CreateFrameworkHandler,
    GetFrameworkHandler,
    GetFrameworksHandler,
    UpdateFrameworkHandler,
    DeleteFrameworkHandler,
    CloneFrameworkHandler,
)
from .report import (
    CreateReportHandler,
    GetReportHandler,
    GetReportsHandler,
    UpdateReportHandler,
    DeleteReportHandler,
    AddSourceToReportHandler,
    RemoveSourceFromReportHandler,
)
from .source import (
    CreateSourceHandler,
    GetSourceHandler,
    GetSourcesHandler,
    UpdateSourceHandler,
    DeleteSourceHandler,
)
from .stack import (
    CreateStackHandler,
    GetStackHandler,
    GetStacksHandler,
    UpdateStackHandler,
    DeleteStackHandler,
    AddReportToStackHandler,
    RemoveReportFromStackHandler,
)
from .scorecard import (
    CreateScorecardHandler,
    UpdateScorecardHandler,
    DeleteScorecardHandler,
)
from .user import (
    ChangePasswordHandler,
    GetMyUserHandler,
    UpdateMyUserHandler,
    CreateUserHandler,
    CheckAvailableUsername,
    UpdateMyPinsHandler,
)

from .oxgpt import (
    GenerateFrameworkHandler,
    GenerateMoreCriteriaHandler,
    AnalyzeSubjectsHandler,
    AnalyzeFileHandler,
    GenerateSubjectsHandler,
    SaveResultsHandler,
    CreateAccountHandler,
    LogInHandler,
)
from .subscriptions import (
    SubscribeHandler,
    UnsubscribeHandler,
    MarkInboxItemDoneHandler,
    MarkInboxItemActiveHandler,
    MarkInboxItemReadHandler,
    MarkInboxItemUnreadHandler,
)
from .comments import (
    AddCommentHandler,
    UpdateCommentHandler,
    DeleteCommentHandler,
)
from .permissions import (
    UpdatePermissionsHandler,
)

from .organizations import (
    CreateOrganizationHandler,
    UpdateOrganizationHandler,
    DeleteOrganizationHandler,
    GetOrganizationHandler,
)
from .teams import (
    CreateTeamHandler,
    UpdateTeamHandler,
    DeleteTeamHandler,
    GetTeamHandler,
)


event_handlers = {
    "create_framework": CreateFrameworkHandler,
    "get_framework": GetFrameworkHandler,
    "get_frameworks": GetFrameworksHandler,
    "delete_framework": DeleteFrameworkHandler,
    "update_framework": UpdateFrameworkHandler,
    "clone_framework": CloneFrameworkHandler,
    "create_report": CreateReportHandler,
    "get_report": GetReportHandler,
    "get_reports": GetReportsHandler,
    "delete_report": DeleteReportHandler,
    "update_report": UpdateReportHandler,
    "create_source": CreateSourceHandler,
    "get_source": GetSourceHandler,
    "get_sources": GetSourcesHandler,
    "delete_source": DeleteSourceHandler,
    "update_source": UpdateSourceHandler,
    "create_stack": CreateStackHandler,
    "get_stack": GetStackHandler,
    "get_stacks": GetStacksHandler,
    "add_report_to_stack": AddReportToStackHandler,
    "remove_report_from_stack": RemoveReportFromStackHandler,
    "delete_stack": DeleteStackHandler,
    "update_stack": UpdateStackHandler,
    "add_source_to_report": AddSourceToReportHandler,
    "remove_source_from_report": RemoveSourceFromReportHandler,
    "create_scorecard": CreateScorecardHandler,
    "update_scorecard": UpdateScorecardHandler,
    "delete_scorecard": DeleteScorecardHandler,
    "change_password": ChangePasswordHandler,
    "get_my_user": GetMyUserHandler,
    "update_my_user": UpdateMyUserHandler,
    "create_user": CreateUserHandler,
    "check_username": CheckAvailableUsername,
    "update_my_pins": UpdateMyPinsHandler,
    "subscribe": SubscribeHandler,
    "unsubscribe": UnsubscribeHandler,
    "add_comment": AddCommentHandler,
    "update_comment": UpdateCommentHandler,
    "delete_comment": DeleteCommentHandler,
    "mark_inbox_item_done": MarkInboxItemDoneHandler,
    "mark_inbox_item_active": MarkInboxItemActiveHandler,
    "mark_inbox_item_read": MarkInboxItemReadHandler,
    "mark_inbox_item_unread": MarkInboxItemUnreadHandler,
    "update_permissions": UpdatePermissionsHandler,
    "create_organization": CreateOrganizationHandler,
    "update_organization": UpdateOrganizationHandler,
    "delete_organization": DeleteOrganizationHandler,
    "get_organization": GetOrganizationHandler,
    "create_team": CreateTeamHandler,
    "update_team": UpdateTeamHandler,
    "delete_team": DeleteTeamHandler,
    "get_team": GetTeamHandler,
    "oxgpt_generate_framework": GenerateFrameworkHandler,
    "oxgpt_generate_more_criteria": GenerateMoreCriteriaHandler,
    "oxgpt_analyze_subjects": AnalyzeSubjectsHandler,
    "oxgpt_analyze_file": AnalyzeFileHandler,
    "oxgpt_generate_subjects": GenerateSubjectsHandler,
    "oxgpt_save_results": SaveResultsHandler,
    "oxgpt_create_account": CreateAccountHandler,
    "oxgpt_log_in": LogInHandler,
}
