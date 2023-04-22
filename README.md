<h1 align="center">
    <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/LagrangeH/chat-bot-telegram/test_and_lint.yml">
    <img alt="GitHub repo file count" src="https://img.shields.io/github/directory-file-count/LagrangeH/chat-bot-telegram">
    <img alt="Python 3.10" src="https://img.shields.io/badge/python3.10-blue.svg">
</h1>

This is a simple chatbot for Telegram. It is written in Python and uses the [aiogram](https://aiogram.dev/).

## Features

* The bot can send a random picture with a cute cat. The `/cat` command is used for this (by [TheCatAPI](https://thecatapi.com/))
* Currency conversion is available using the `/convert` command (by [Exchange Rates API.io](https://exchangeratesapi.io/))
* Using the `/weather` command, you can find out the weather in any city (by [OpenWeatherMap](https://openweathermap.org/))
* The `/poll` command allows you to create a poll
* All commands are also available in the Telegram groups

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
    poetry use python3.10
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
   