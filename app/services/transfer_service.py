from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from .account import Account
from .transaction import Transaction
from .user import User
from .transfer import TransferRequest

class TransferService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def transfer(self, sender_id: int, receiver_id: int, request: TransferRequest) -> None:
        sender = await self.db.execute(select(Account).where(Account.id == sender_id))
        receiver = await self.db.execute(select(Account).where(Account.id == receiver_id))
        sender_account = sender.scalar_one_or_none()
        receiver_account = receiver.scalar_one_or_none()

        if not sender_account or not receiver_account:
            raise ValueError('Cuentas no encontradas')

        if sender_account.balance < request.amount:
            raise ValueError('Saldo insuficiente')

        sender_account.balance -= request.amount
        receiver_account.balance += request.amount

        transaction = Transaction(
            amount=request.amount,
            currency=request.currency,
            account_id=sender_id
        )

        self.db.add(transaction)
        await self.db.commit()
        await self.db.refresh(transaction)
