import logging

from api_app.analyzers_manager.classes import ObservableAnalyzer

# from api_app.exceptions import AnalyzerRunException
# from tests.mock_utils import if_mock_connections, patch

logger = logging.getLogger(__name__)


class chatgpt(ObservableAnalyzer):
    def run(self):
        from revChatGPT.ChatGPT import Chatbot

        chatbot = Chatbot(
            {"session_token": "<YOUR_TOKEN>"}, conversation_id=None, parent_id=None
        )  # You can start a custom conversation

        response = chatbot.ask(
            "Prompt", conversation_id=None, parent_id=None
        )  # You can specify custom conversation and parent ids.
        # Otherwise it uses the saved conversation

        print(response)
