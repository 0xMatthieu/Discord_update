import unittest
from unittest.mock import patch, MagicMock
from ai_agent import summarize_channel_messages
from discord_bot import display_channel_messages

class TestAIAgent(unittest.TestCase):

    @patch('ai_agent.sqlite3.connect')
    def test_summarize_channel_messages(self, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock database return values
        mock_cursor.fetchall.return_value = [('Message 1',), ('Message 2',), ('Message 3',)]

        # Mock OpenAI API response
        with patch('ai_agent.openai.Completion.create') as mock_openai:
            mock_openai.return_value.choices = [MagicMock(text="Summary of messages")]

            # Call the function
            response = summarize_channel_messages('test_channel_id')

            # Assertions
            self.assertEqual(response.channel_id, 'test_channel_id')
            self.assertEqual(response.summary, 'Summary of messages')

    @patch('discord_bot.sqlite3.connect')
    def test_display_channel_messages(self, mock_connect):
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Mock database return values
        mock_cursor.fetchall.return_value = [('Message 1',), ('Message 2',), ('Message 3',)]

        # Capture print output
        with patch('builtins.print') as mock_print:
            display_channel_messages('test_channel_id', 3)

            # Assertions
            mock_print.assert_any_call('Message 1')
            mock_print.assert_any_call('Message 2')
            mock_print.assert_any_call('Message 3')

if __name__ == '__main__':
    unittest.main()
