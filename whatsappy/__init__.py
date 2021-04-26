from .error import (
    WhatsappyError,
    LoginError,
)
from .chat import (
    last_message,
    new_message,
    send,
    reply,
    last,
    send_file,
    reply_privately,
    reply_file_privately,
)
from .actions import (
    add_to_group,
    remove_from_group,
    make_group_admin,
    select_chat_by_number,
    select_chat_by_name,
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

last = last


class Whatsapp:

    login = login
    close = close

    add_to_group = add_to_group
    remove_from_group = remove_from_group
    make_group_admin = make_group_admin

    last_message = last_message
    new_message = new_message
    send = send
    send_file = send_file
    reply = reply
    reply_privately = reply_privately
    reply_file_privately = reply_file_privately
    select_chat_by_name = select_chat_by_name
    select_chat_by_number = select_chat_by_number

    get_pinned_chats = get_pinned_chats
    get_recent_chats = get_recent_chats
    get_group_invite_link = get_group_invite_link

    change_group_description = change_group_description
    change_group_name = change_group_name
    change_group_pfp = change_group_pfp
    leave_group = leave_group
    create_group = create_group


whatsapp = Whatsapp()
