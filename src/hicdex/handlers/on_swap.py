import hicdex.models as models
from hicdex.types.hen_minter.parameter.swap import SwapParameter
from hicdex.types.hen_minter.storage import HenMinterStorage
from dipdup.models import OperationHandlerContext, TransactionContext


async def on_swap(
    ctx: OperationHandlerContext,
    swap: TransactionContext[SwapParameter, HenMinterStorage],
) -> None:
    holder, _ = await models.Holder.get_or_create(address=swap.data.sender_address)
    token = await models.Token.filter(id=int(swap.parameter.objkt_id)).get()
    swap_model = models.Swap(
        id=int(swap.storage.swap_id) - 1,  # type: ignore
        creator=holder,
        token=token,
        price=swap.parameter.xtz_per_objkt,
        amount=swap.parameter.objkt_amount,
        amount_left=swap.parameter.objkt_amount,
        status=models.SwapStatus.ACTIVE,
        level=swap.data.level,
        timestamp=swap.data.timestamp,
    )
    await swap_model.save()