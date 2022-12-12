from pydantic import BaseModel


class WTRankInfo(BaseModel):
    title: str
    img: str


class TelegramGroupCounters(BaseModel):
    chats: int | None
    channels: int | None
    conversations: int | None
    admin: int | None


class BumpSettings(BaseModel):
    canBumpItem: bool | None
    canBumpItemGlobally: bool | None
    errorPhrase: bool | None


class Reserve(BaseModel):
    reserve_user_id: int | None
    reserve_date: int | None


class Item(BaseModel):
    item_id: int | None
    item_state: str | None
    category_id: int | None
    published_date: int | None
    title: str | None
    description: str | None
    price: int | None
    update_stat_date: int | None
    refreshed_date: int | None
    view_count: int | None
    is_sticky: int | None
    item_origin: str | None
    extended_guarantee: int | None
    nsb: int | None
    allow_ask_discount: int | None
    title_en: str | None
    description_en: str | None
    email_type: str | None
    is_reserved: int | None
    item_domain: str | None
    isIgnored: bool | None
    canOpenItem: bool | None
    canCloseItem: bool | None
    canEditItem: bool | None
    canDeleteItem: bool | None
    canStickItem: bool | None
    canUnstickItem: bool | None
    bumpSettings: BumpSettings | None
    canBumpItem: bool | None
    canBuyItem: bool | None
    rub_price: int | None
    price_currency: str | None
    canValidateAccount: bool | None
    canResellItemAfterPurchase: bool | None
    canViewAccountLink: bool | None
    accountLink: str | None
    note_text: str | None
    tags: list | dict | None
    reserve: Reserve | None
    description_html: str | None
    description_html_en: str | None


class WarThunderItem(Item):
    wt_item_id: int | None
    wt_id: int | None
    wt_nick: str | None
    wt_reg_time_gaijin: int | None
    wt_reg_time_wt: int | None
    wt_last_play: int | None
    wt_email_verified: int | None
    wt_phone_verified: int | None
    wt_played: int | None
    wt_wins: int | None
    wt_exp: int | None
    wt_rank: int | None
    wt_eliteUnits: int | None
    wt_premium: int
    wt_gold: int | None
    wt_silver: int | None
    wt_win_count_percents: int | None
    wt_rank_info: WTRankInfo | None


class TelegramItem(Item):
    telegram_item_id: int | None
    telegram_country: str | None
    telegram_last_seen: int | None
    telegram_scam: int | None
    telegram_verified: int | str | None
    telegram_premium: int | None
    telegram_password: int | None
    telegram_premium_expires: int | None
    telegram_spam_block: int | None
    telegram_group_counters: TelegramGroupCounters | None
    telegram_admin_groups: list | None
