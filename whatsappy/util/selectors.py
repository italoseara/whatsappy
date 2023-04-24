class Selectors:
    QR_CODE = 'div[data-testid="qrcode"]'

    ANIMATING = 'div.app-animating'
    
    SEARCH_BAR = 'div[data-testid="chat-list-search"]'
    SEARCH_BAR_CLEAR = 'button[aria-label="Cancel search"]'

    CHAT_HEADER = 'header[data-testid="conversation-header"]'
    CHAT_INFO_DRAWER = 'div[data-testid="chat-info-drawer"]'
    CHAT_INFO_TEXT = CHAT_INFO_DRAWER + ' span[dir="auto"].copyable-text.selectable-text'
    CHAT_INFO_PICTURE = CHAT_INFO_DRAWER + ' img'
    CHAT_DEFAULT_USER = CHAT_INFO_DRAWER + ' div[data-testid="default-user"]'

    GROUP_SUBJECT = CHAT_INFO_DRAWER + ' div[data-testid="group-info-drawer-subject-input"]'