class Selectors:
    QR_CODE = 'div[data-testid="qrcode"]'

    ANIMATING = 'div.app-animating'

    MESSAGE_BOX = 'div[data-testid="conversation-compose-box-input"]'
    SEND_BUTTON = 'div[aria-label="Send"]'

    SEARCH_BAR = 'div[data-testid="chat-list-search"]'
    SEARCH_BAR_CLEAR = 'button[aria-label="Cancel search"]'

    INFO_DRAWER = 'div[data-testid="chat-info-drawer"]'
    INFO_DRAWER_BODY = f'{INFO_DRAWER} section'
    CURRENT_CHAT = 'span[data-testid="conversation-info-header-chat-title"]'

    CONVERSATION_HEADER = 'header[data-testid="conversation-header"]'
    CONVERSATION_MESSAGES = 'div.message-in'
    CONVERSATION_MENU = 'div[data-testid="conversation-menu-button"] > div[role="button"]'
    CONVERSATION_MUTED = f'{INFO_DRAWER} div[data-testid="block-mute"] > div > div > div:nth-child(2) > div'

    MENU_DROPDOWN = 'div[role="application"] > ul'

    POPUP = 'div[data-testid="confirm-popup"]'
    POPUP_CONFIRM = f'{POPUP} button[data-testid="popup-controls-ok"]'

    MENU_MUTE = f'{MENU_DROPDOWN} li[data-testid="mi-mute"]'
    MUTE_POPUP = 'div[data-testid="mute-popup"]'
    MUTE_TIME_OPTIONS = f'{MUTE_POPUP} form > ol > li'
    MUTE_POPUP_CONFIRM = f'{MUTE_POPUP} button[data-testid="popup-controls-ok"]'

    MENU_CLEAR = f'{MENU_DROPDOWN} li[data-testid="mi-clear"]'
    KEEP_STARRED = f'{POPUP} div[data-testid="visual-checkbox"]'
    
    MESSAGE_CONTAINER = 'div[data-testid="msg-container"]'
    MESSAGE_INFO = 'div.copyable-text'
    MESSAGE_AUTHOR = 'div > span[aria-label]'
    MESSAGE_CONTENT = 'span.selectable-text'
    MESSAGE_META = 'div[data-testid="msg-meta"] > span'
    MESSAGE_FORWARDED = 'span[data-testid="forwarded"]'
    MESSAGE_QUOTE = 'div[data-testid="quoted-message"]'

    CHAT_INPUT = 'div[data-testid="conversation-compose-box-input"]'
    CHAT_INFO_TEXT = f'{INFO_DRAWER} span[dir="auto"].copyable-text.selectable-text'
    CHAT_INFO_PIC = f'{INFO_DRAWER} section > div img'
    CHAT_DEFAULT_PIC = f'{INFO_DRAWER} span[data-testid="default-user"]'
    CHAT_DELETE = f'{INFO_DRAWER} div[data-testid="li-delete-chat"]'
    
    CHAT_BLOCK = f'{INFO_DRAWER} div[data-testid="li-block"]'
    CHAT_UNBLOCK = f'{INFO_DRAWER} div[data-testid="li-unblock"]'

    GROUP_INFO_HEADER = 'div[data-testid="group-info-header"]'
    GROUP_SUBJECT = f'{INFO_DRAWER} span[data-testid="group-info-drawer-subject-input-read-only"]'
    GROUP_PARTICIPANTS = f'{INFO_DRAWER} div[data-testid="group-info-top-card-subtitle"] > span > span > button'
    GROUP_INFO_PIC = CHAT_INFO_PIC
    GROUP_DEFAULT_PIC = f'{INFO_DRAWER} span[data-testid="default-group"]'
    GROUP_DESCRIPTION = f'{INFO_DRAWER} span[data-testid="group-info-drawer-description-title-input-read-only"]'
    GROUP_READ_MORE = f'{GROUP_DESCRIPTION} + button'

    GROUP_LEAVE = f'{INFO_DRAWER} div[data-testid="li-delete-group"]'

    UNREAD_BADGE = 'span[data-testid="icon-unread-count"]'
    UNREAD_TITLE = 'div[data-testid="cell-frame-title"] > span'
    UNREAD_LAST_MESSAGE = 'span[data-testid="last-msg-status"]'
    UNREAD_CONVERSATIONS_XPATH = '//span[@data-testid="icon-unread-count"]/ancestor::div[@data-testid="cell-frame-container"]'

    MY_PROFILE_TEXT = 'div[data-testid="drawer-left"] span[data-testid="col-main-profile-input-read-only"]'
    MY_PROFILE_PIC = 'div[data-testid="profile-pic-picker"] img'
    MY_PROFILE_DEFAULT_PIC = 'div[data-testid="profile-pic-picker"] span[data-testid="default-user"]'

    MEDIA_CAPTION = 'div[data-testid="media-caption-input-container"]'

    ATTATCHMENT_MENU = 'div[data-testid="conversation-clip"] > div'
    INPUT_DOCUMENTS = 'span[data-testid="attach-document"] + input'
    INPUT_MIDIA = 'span[data-testid="attach-image"] + input'
