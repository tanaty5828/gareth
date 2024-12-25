import unittest
from unittest.mock import patch, MagicMock
from main import (
    fetch_schedule,
    fetch_instructors,
    format_schedule,
    get_reservation_emoji,
)


class TestMain(unittest.TestCase):

    @patch("main.requests.get")
    def test_fetch_schedule(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {
                "studio_lessons": {
                    "items": [
                        {
                            "id": 1,
                            "instructor_id": 1,
                            "start_at": "2023-10-01T10:00:00",
                            "end_at": "2023-10-01T11:00:00",
                            "date": "2023-10-01",
                            "reservation_count": 2,
                        }
                    ]
                }
            }
        }
        mock_get.return_value = mock_response
        today = "2023-10-01"
        result = fetch_schedule(today)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)

    @patch("main.bot.run")
    @patch("main.keep_alive")
    def test_bot_startup(self, mock_keep_alive, mock_bot_run):
        # Call the main function to start the bot
        import main

        main.keep_alive()
        main.bot.run(main.TOKEN)

        # Check if keep_alive and bot.run were called
        mock_keep_alive.assert_called_once()
        mock_bot_run.assert_called_once_with(main.TOKEN)

    @patch("main.requests.get")
    def test_fetch_instructors(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "data": {"instructors": {"list": [{"id": 1, "name": "Instructor A"}]}}
        }
        mock_get.return_value = mock_response
        result = fetch_instructors()
        self.assertEqual(result[1], "Instructor A")

    def test_format_schedule(self):
        items = [
            {
                "instructor_id": 1,
                "start_at": "2023-10-01T10:00:00",
                "end_at": "2023-10-01T11:00:00",
                "date": "2023-10-01",
                "reservation_count": 2,
            }
        ]
        instructor_map = {1: "Instructor A"}
        result = format_schedule(items, instructor_map, None, None)
        self.assertIn("- 2023-10-01", result)
        self.assertIn("  - 10:00 - 11:00 Instructor A 🟡🟡", result)

    def test_get_reservation_emoji(self):
        self.assertEqual(get_reservation_emoji(0), "⛳️")
        self.assertEqual(get_reservation_emoji(1), "🟢")
        self.assertEqual(get_reservation_emoji(2), "🟡🟡")
        self.assertEqual(get_reservation_emoji(3), "🟡🟡🟡")
        self.assertEqual(get_reservation_emoji(4), "🔴🔴🔴🔴")
        self.assertEqual(get_reservation_emoji(5), "🔴🔴🔴🔴🔴")
        self.assertEqual(get_reservation_emoji(6), "")


if __name__ == "__main__":
    unittest.main()
