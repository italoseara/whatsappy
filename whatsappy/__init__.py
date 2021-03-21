from .cmds.actions import add_to_group, remove_from_group, make_group_admin
from .cmds.chat import select_chat, last_message, new_message, send, reply, send_file
from .cmds.get import get_pinned_chats, get_recent_chats
from .cmds.group import change_group_description, change_group_name, leave_group
from .cmds.login import get_qrcode, login, exit

class Whatsapp:

    login                       = login
    get_qrcode                  = get_qrcode
    exit                        = exit
    add_to_group                = add_to_group
    remove_from_group           = remove_from_group
    make_group_admin            = make_group_admin
    select_chat                 = select_chat
    last_message                = last_message
    new_message                 = new_message
    send                        = send
    reply                       = reply
    send_file                   = send_file
    get_pinned_chats            = get_pinned_chats
    get_recent_chats            = get_recent_chats
    change_group_description    = change_group_description
    change_group_name           = change_group_name
    leave_group                 = leave_group

    # TODO: get group invite link

    # TODO: invite by number

    # TODO: private answer

    # TODO: Get group info (maybe turn it into a class)

    # TODO: Decent error message

    # TODO: Create group

whatsapp = Whatsapp()