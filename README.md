<h1 align="center">
    <a href="https://github.com/LagrangeH/chat-bot-telegram/actions/workflows/test_and_lint.yml"><img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/LagrangeH/chat-bot-telegram/test_and_lint.yml"></a>
    <a href="https://github.com/LagrangeH/chat-bot-telegram"><img alt="GitHub repo file count" src="https://img.shields.io/github/directory-file-count/LagrangeH/chat-bot-telegram"></a>
    <a href="https://www.python.org/"><img alt="Python 3.10" src="https://img.shields.io/badge/python3.10-blue.svg"></a>
</h1>

This is a simple chatbot for Telegram. It is written in Python and uses the [aiogram](https://aiogram.dev/). Try it out [here](https://t.me/chat_bot_lagrange_bot)

## Features

* The bot can send a random picture with a cute cat. The `/cat` command is used for this (by [TheCatAPI](https://thecatapi.com/))
* Currency conversion is available using the `/convert` command (by [Exchange Rates API.io](https://exchangeratesapi.io/))
* Using the `/weather` command, you can find out the weather in any city (by [OpenWeatherMap](https://openweathermap.org/))
* The `/poll` command allows you to create a poll
* All commands are also available in the Telegram groups
* Throttling is used to save resources and API requests

## Installation

1. Install [Python 3.10](https://www.python.org/)
2. Install [Poetry](https://python-poetry.org/docs/#installation) and add it to the PATH
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```

3. Check that Poetry is installed correctly
    ```bash
    poetry --version
    ```

4. Clone the repository
    ```bash
   git clone https://github.com/LagrangeH/chat-bot-telegram.git
    ```

5. Go to the project directory
    ```bash
    cd chat-bot-telegram
    ```

6. Create a virtual environment
    ```bash
    poetry env use python3.10
    ```

7. Install dependencies
    ```bash
    poetry install
    ```

8. Create `.env` file (copy [`.env.dist`](/.env.dist) and rename it to `.env`)
    ```bash
    cp .env.dist .env
    ```

9. Fill in the `.env` file
    ```dotenv
    DEBUG=False
    # https://t.me/botfather
    BOT_TOKEN=
    # https://thecatapi.com/ (Optional)
    CAT_API_KEY=
    # https://openweathermap.org/home/sign_up
    WEATHER_API_KEY=
    # https://exchangeratesapi.io/
    EXCHANGE_API_KEY=
    ```

## Usage

1. Run the bot
    ```bash
    poetry run python bot.py
    ```

2. Send a message to the bot in Telegram
3. Use the `/help` command to see all available commands

## Testing

The [pytest](https://docs.pytest.org/) framework is used for testing. Some unit-tests require parameters to be passed in.

* Parameters can be optionally passed in command line mode:

   ```bash
   poetry run pytest /tests --cat-api-key="..." --weather-api-key="..." --exchange-api-key="..."
   ```

If some parameters were not passed in command line mode, they will be taken from the .env file, otherwise, tests that require these parameters will be skipped.

* To run tests with parameters passed from .env or without passing parameters, the following command is sufficient:

   ```bash
   poetry run pytest /tests
   ```