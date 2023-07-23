from notification.discord import DiscordClientWrapper
from notification.email import EmailNotification

class Notification:
    def __init__(self) -> None:
        self.email = EmailNotification
        self.discord = DiscordClientWrapper()
