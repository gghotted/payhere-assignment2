from functools import partial

from core.permissions import IsOwner

IsStoreOwner = partial(IsOwner, owner_field="owner")
