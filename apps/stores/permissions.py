from functools import partial

from core.permissions import IsOwner

IsStoreOwner = partial(IsOwner, owner_id_field="owner_id")
IsCategoryOwner = partial(IsOwner, owner_id_field="store.owner_id")
IsProductOwner = partial(IsOwner, owner_id_field="store.owner_id")
