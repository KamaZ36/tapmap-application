from uuid import UUID


def order_key(order_id: UUID) -> str:
    return f"draft_order:{str(order_id)}"

def user_index_key(user_id: UUID) -> str:
        return f"draft_order:user_id:{str(user_id)}"
