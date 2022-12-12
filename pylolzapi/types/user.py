from pydantic import BaseModel


class Links(BaseModel):
    permalink: str
    detail: str
    avatar: str
    avatar_big: str
    avatar_small: str
    followers: str
    followings: str
    ignore: str
    timeline: str


class Permissions(BaseModel):
    edit: bool
    follow: bool
    ignore: bool
    profile_post: bool


class Field(BaseModel):
    id: str | int | None
    title: str | None
    description: str | None
    position: str | None
    is_required: bool | None
    value: str | None
    is_multi_choice: bool | None


class Group(BaseModel):
    user_group_id: int
    user_group_title: str
    is_primary_group: bool


class SelfPermissions(BaseModel):
    create_conversation: bool | None
    upload_attachment_conversation: bool | None


class EditPermissions(BaseModel):
    password: bool | None
    user_email: bool | None
    username: bool | None
    user_title: bool | None
    primary_group_id: bool | None
    secondary_group_ids: bool | None
    user_dob_day: bool | None
    user_dob_month: bool | None
    user_dob_year: bool | None
    fields: bool | None


class User(BaseModel):
    user_id: int
    username: str
    user_message_count: int
    user_register_date: int
    user_like_count: int
    short_link: str
    user_email: str
    user_unread_notification_count: int
    user_dob_day: int
    user_dob_month: int
    user_dob_year: int
    user_title: str
    user_is_valid: bool
    user_is_verified: bool
    user_is_followed: bool
    user_last_seen_date: int
    links: Links
    permissions: Permissions
    user_is_ignored: bool
    user_is_visitor: bool
    user_timezone_offset: int
    user_has_password: bool
    fields: list[Field]
    user_groups: list[Group]
    self_permissions: SelfPermissions
    edit_permissions: EditPermissions
