from .database.models import Password
from .utils import unfold_pg_array, validate_decor, compose_message, Status


@validate_decor
def proc_leaked(**json_data):
    """Processing request from client"""
    stub = json_data["hash"]
    data = []
    sel = Password.select().where(Password.password_hash.startswith(stub))
    if sel.count() < 1:
        return compose_message(Status.no_query)
    else:
        for (
            item
        ) in sel.iterator():  # pewee select object provides nice `iterator()` method
            data.append(
                {
                    "hash": item.password_hash,
                    "count": item.count,
                    "sources": unfold_pg_array(item.password_source),
                }
            )
        return compose_message(Status.success, data)
