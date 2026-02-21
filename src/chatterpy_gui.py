# -----------------------------------------------------------------------------
# Copyright (c) 2026 Salvatore D'Angelo, Code4Projects
# Licensed under the MIT License. See LICENSE.md for details.
# -----------------------------------------------------------------------------
from core import LoggerManager, chatterpy_config, setup_logging
from dotenv import load_dotenv
from gui import ChatBotPage, Page

# Load environment variables
load_dotenv()

# Initialize logging first
setup_logging(
    level=chatterpy_config.log.level,
    console=chatterpy_config.log.console,
    file=chatterpy_config.log.file,
    rotation=chatterpy_config.log.rotation,
    retention=chatterpy_config.log.retention,
    compression=chatterpy_config.log.compression,
)

# Create a main logger
logger = LoggerManager.get_logger(name="main")


# Decorator to implement the Singleton design pattern.
# A singleton ensures that there is only one instance of a specific class
# and provides a global access point to this instance.
def singleton(cls):
    instances = {}

    # Function to get the singleton instance.
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


# This class is responsible for managing the Streamlit application
# and navigation between different pages. It initializes the initial page, handles page selection,
# and serves as the entry point for running the application.
@singleton
class ChatBotApp:
    # The constructor load all the activities in the gpx folder of the logged in user.
    def __init__(self):
        self.current_page: Page | None = None

    # Runs the TrainingApp and initializes the first page as ActivityOverviewPage.
    def run(self):
        self.select_page(ChatBotPage())

    # Selects and renders the current page based on user navigation logic.
    def select_page(self, page: Page):
        # Here you can add logic for navigating between different pages.
        # For example, if you want to show the ActivityOverviewPage as the initial page:
        self.current_page = page
        self.current_page.render()


if __name__ == "__main__":
    app: ChatBotApp = ChatBotApp()
    app.run()
