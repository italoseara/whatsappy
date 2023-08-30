class Selectors:
    CLOSE = 'span[data-icon="x"]'
    
    QR_CODE = 'div[data-ref]:has(canvas)'

    ANIMATING = 'div.app-animating'

    MEDIA_CAPTION = '#app > div > div > div:nth-child(3) div[role="textbox"]'
    SEARCH_RESULT = '#pane-side div[role="grid"] > div > div:has(div[tabindex="-1"])'
    SEND_BUTTON = 'span[data-icon="send"]'

    SEARCH_BAR = 'div.lexical-rich-text-input > div[role="textbox"]'
    SEARCH_BAR_CLEAR = 'button[aria-label="Cancel search"]'

    NO_CONTACTS_FOUND = 'div[aria-live="polite"]'

    INFO_DRAWER = '#app > div > div > div:nth-child(6)'
    INFO_DRAWER_BODY = f'{INFO_DRAWER} section'

    CONVERSATION_HEADER = 'header:has(div[title="Profile Details"])'
    CONVERSATION_CURRENT = f'{CONVERSATION_HEADER} > div:nth-child(2) > div > div > span'
    CONVERSATION_MESSAGES = 'div.message-in'
    CONVERSATION_MENU = f'{CONVERSATION_HEADER} div[role="button"]:has(span[data-icon="menu"])'
    CONVERSATION_MUTED = f'{INFO_DRAWER} > div:nth-child(5) > div:nth-child(1) div[aria-label]'

    MENU_DROPDOWN = 'div[role="application"] > ul'

    POPUP = 'div[data-animate-modal-popup="true"]'
    POPUP_CONFIRM = f'{POPUP} button:last-child'

    MENU_MUTE = f'{MENU_DROPDOWN} li > div[aria-label="Mute notifications"]'
    MUTE_TIME_OPTIONS = f'{POPUP} label'

    MENU_CLEAR = f'{MENU_DROPDOWN} li > div[aria-label="Clear messages"]'
    KEEP_STARRED = f'{POPUP} #menu-icon-clear-chat'

    MENU_PIN = f'{MENU_DROPDOWN} li > div[aria-label="Pin chat"]'
    PIN_ICON = f'{SEARCH_RESULT} span[data-icon="pinned2"]'
    
    MESSAGE_CONTAINER = 'div'
    MESSAGE_INFO = 'div.copyable-text[data-pre-plain-text]'
    MESSAGE_AUTHOR = 'div > span[aria-label]'
    MESSAGE_CONTENT = 'span.selectable-text'
    MESSAGE_META = f'div:nth-child(3) > div> div > div:last-child'
    MESSAGE_FORWARDED = 'span[data-icon="forwarded"]'
    MESSAGE_QUOTE = 'div[aria-label="Quoted Message"]'
    MESSAGE_LINK_PLACEHOLDER = 'span[data-icon="link-placeholder-dark"], span[data-icon="link-placeholder-light"]'

    CHAT_INPUT = '#main div.lexical-rich-text-input > div[role="textbox"]'
    CHAT_INFO_TEXT = f'{INFO_DRAWER} span[dir="auto"].copyable-text.selectable-text'
    CHAT_INFO_PIC = f'{INFO_DRAWER_BODY} > div img'
    CHAT_DEFAULT_PIC = f'{INFO_DRAWER} span[data-icon="default-user"]'

    CHAT_DELETE = f'{INFO_DRAWER} div[title="Delete chat"]'
    CHAT_BLOCK = f'{INFO_DRAWER} div[title="Block "]'
    CHAT_UNBLOCK = f'{INFO_DRAWER} div[title="Unblock "]'

    GROUP_INFO_HEADER = 'div[title="Group info"]'
    GROUP_SUBJECT = f'{INFO_DRAWER} span.selectable-text.copyable-text > span[dir="ltr"]'
    GROUP_PARTICIPANTS = f'{INFO_DRAWER} span.selectable-text.copyable-text > span[aria-label=""] > button'
    GROUP_INFO_PIC = CHAT_INFO_PIC
    GROUP_DEFAULT_PIC = f'{INFO_DRAWER} span[data-icon="default-group"]'
    GROUP_DESCRIPTION = f'{INFO_DRAWER_BODY} > div:nth-child(2) span'
    GROUP_READ_MORE = f'{GROUP_DESCRIPTION} + button'

    GROUP_LEAVE = f'{INFO_DRAWER} div[title="Exit group"]'

    GROUP_SEARCH = f'{INFO_DRAWER_BODY} > div:nth-child(6) span[data-icon="search"]'
    GROUP_SEARCH_INPUT = f'{POPUP} div.lexical-rich-text-input > div[role="textbox"]'
    GROUP_SEARCH_RESULT = f'{POPUP} div:has(header) div[role="listitem"]:has(div[tabindex="-1"])'

    GROUP_ADMIN_BADGE = 'div[role="gridcell"][aria-colindex="2"] div:nth-child(2)'

    GROUP_PROMOTE_ADMIN = 'li > div[aria-label="Make group admin"]'
    GROUP_DEMOTE_ADMIN = 'li > div[aria-label="Dismiss as admin"]'

    UNREAD_BADGE = 'span[aria-label="Unread"]'
    UNREAD_TITLE = 'span[title]'
    UNREAD_LAST_MESSAGE = 'div[role="gridcell"] + div span[title]'
    UNREAD_CONVERSATIONS = 'div[aria-label="Chat list"] div[role="listitem"]:has(span[aria-label="Unread"])'

    MY_PROFILE_PAGE = '#app > div > div > div:nth-child(4)'
    MY_PROFILE_TEXT = f'{MY_PROFILE_PAGE} span.selectable-text.copyable-text > span[dir="ltr"]'
    MY_PROFILE_PIC = f'{MY_PROFILE_PAGE} div[title="Photo"] img'
    MY_PROFILE_DEFAULT_PIC = f'{MY_PROFILE_PAGE} div[title="Add profile photo"] span[data-icon="default-user"]'

    MESSAGE_BOX = '#main div[title="Type a message"]'

    ATTATCHMENT_MENU = 'div[aria-label="Attach"]'
    ATTATCHMENT_ITEMS = 'li[data-animate-dropdown-item="true"]'
    INPUT_DOCUMENTS = f'{ATTATCHMENT_ITEMS}:nth-child(1)'
    INPUT_MIDIA = f'{ATTATCHMENT_ITEMS}:nth-child(2)'
    INPUT_CONTACTS = f'{ATTATCHMENT_ITEMS}:nth-child(4)'
