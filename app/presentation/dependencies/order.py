from dishka import Provider, Scope, provide

from app.application.interactions.draft_order.add_comment import AddCommentToDraftOrderInteraction
from app.application.interactions.draft_order.add_point import AddPointToDraftOrderInteraction
from app.application.interactions.draft_order.confirm_draft_order import ConfirmDraftOrderInteraction
from app.application.interactions.draft_order.create_order import CreateDraftOrderInteraction
from app.application.interactions.draft_order.delete import DeleteDraftOrderInteraction
from app.application.interactions.draft_order.get_draft_order import GetDraftOrderInteraction
from app.application.interactions.order.cancel_order import CancelOrderInteraction
from app.application.interactions.order.get_order import GetOrderInteraction
from app.application.interactions.order.get_orders import GetOrdersInteraction
from app.application.interactions.order.process_order import ProcessOrderInteraction
from app.application.interactions.order.update_status import UpdateStatusInteraction


class DraftOrdersInteractions(Provider):
    # QUERY
    get_draft_order_interactor = provide(GetDraftOrderInteraction, scope=Scope.REQUEST)
    get_orders_list_interactor = provide(GetOrdersInteraction, scope=Scope.REQUEST)
    get_order_interactor = provide(GetOrderInteraction, scope=Scope.REQUEST)
    
    # COMMANDS
    create_order_interactor = provide(CreateDraftOrderInteraction, scope=Scope.REQUEST)
    add_point_to_draft_order_interactor = provide(AddPointToDraftOrderInteraction, scope=Scope.REQUEST)
    add_comment_to_draft_order_interactor = provide(AddCommentToDraftOrderInteraction, scope=Scope.REQUEST)
    confirm_draft_order_interactor = provide(ConfirmDraftOrderInteraction, scope=Scope.REQUEST)
    delete_draft_order_interactor = provide(DeleteDraftOrderInteraction, scope=Scope.REQUEST)
    cancel_order_interactor = provide(CancelOrderInteraction, scope=Scope.REQUEST)
    update_order_status_interactor = provide(UpdateStatusInteraction, scope=Scope.REQUEST)
    process_order_interactor = provide(ProcessOrderInteraction, scope=Scope.REQUEST)
