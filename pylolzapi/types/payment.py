from pydantic import BaseModel, validator


class Data(BaseModel):
    user_id: int | None
    username: str | None
    includeFee: bool | None
    finishAmount: int | None
    status: str | None
    comment: str | None
    is_banned: int | None
    display_style_group_id: int | None
    uniq_username_css: str | None
    avatar_date: int | None
    user_group_id: int | None
    secondary_group_ids: int | str | None
    bool_status: bool | None


class Label(BaseModel):
    title: str


class User(BaseModel):
    user_id: int | None
    user_balance: int | None
    user_hold: int | None
    user_balance_with_hold: int | None


class Operation(BaseModel):
    operation_id: int
    operation_date: int
    operation_type: str
    outgoing_sum: int
    incoming_sum: int
    item_id: int
    wallet: str
    is_finished: int
    is_hold: int
    payment_system: str
    data: bool | Data | None
    hold_end_date: int
    api: int
    originalWallet: str | None
    payment_status: str
    supportLink: str | None
    canCancelBalanceTransfer: bool
    canCancelBalancePayout: bool
    canFinishBalanceTransfer: bool
    canFinishBalancePayout: bool
    label: Label
    user: User

    @validator("data", pre=True)
    def verify_is_boolean(cls, value):
        if isinstance(value, bool):
            return Data()
