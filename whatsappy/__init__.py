from .chat import (
    last_message,
    new_message,
    send,
)
from .actions import (
    add_to_group,
    remove_from_group,
    make_group_admin,
    select_chat,
    create_group,
)
from .group import (
    change_group_description,
    change_group_name,
    change_group_pfp,
    leave_group,
)
from .get import get_pinned_chats, get_recent_chats, get_group_invite_link
from .login import login, close


class Whatsapp:

    login = login
    close = close

    add_to_group = add_to_group
    remove_from_group = remove_from_group
    make_group_admin = make_group_admin

    last_message = last_message
    new_message = new_message
    send = send
    select_chat = select_chat

    get_pinned_chats = get_pinned_chats
    get_recent_chats = get_recent_chats
    get_group_invite_link = get_group_invite_link

    change_group_description = change_group_description
    change_group_name = change_group_name
    change_group_pfp = change_group_pfp
    leave_group = leave_group
    create_group = create_group

whatsapp = Whatsapp()