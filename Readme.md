# Discord Bot :)

This project is a Discord bot designed to manage schedules on a Discord server. The bot sends schedules at specified times and responds to user messages.

## Features

- Sends schedules at specified times
- Responds to user messages
- Displays emojis based on reservation status

## Environment Variables

The following environment variables need to be set in a `.env` file:

- `DISCORD_TOKEN`: The token for the Discord bot
- `SCHEDULE_URL`: The URL to fetch schedules from
- `INSTRUCTORS_URL`: The URL to fetch instructor information from
- `CHANNEL_ID`: The ID of the channel to send messages to

## Setup

1. Clone the repository.

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required dependencies.
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file and set the necessary environment variables.

4. Start the bot.

    ```sh
    python src/main.py
    ```

## Testing

To run the tests, use the following command:

    ```sh
    python -m unittest discover -s src -p "test_main.py"
    ```

## Docker
To run the bot using Docker, follow these steps:

Build the Docker image.

    ```sh
    docker build -t discord-bot .
    ```

Run the Docker container.

    ```sh
    docker run --env-file .env discord-bot
    ```

## Continuous Integration

This project uses GitHub Actions for continuous integration. The workflows are defined in the .github/workflows/ directory.

`lint.yml`: Runs flake8 to lint the code.
`test.yml`: Runs the unit tests.


Continuous Integration
This project uses GitHub Actions for continuous integration. The workflows are defined in the .github/workflows/ directory.

lint.yml: Runs flake8 to lint the code.
test.yml: Runs the unit tests.
