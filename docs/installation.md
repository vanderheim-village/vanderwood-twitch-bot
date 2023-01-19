# Installation

## Requirements

* Ubuntu 20.04 or later
* Python 3.10 or later
* PostgreSQL 13 or later
* Nginx

## Installation Steps

1. Clone or download the repository.

2. Create a Python virtual environment and install the dependencies.

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Create a PostgreSQL database and user.

    ```bash
    sudo -u postgres psql
    CREATE DATABASE battleofmidgard;
    CREATE USER battleofmidgard WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE battleofmidgard TO battleofmidgard;
    ```

4. Make a copy of config.yml.example and rename it to config.yml.

    ```bash
    cp config.yml.example config.yml
    ```

5. Edit config.yml and add in the database credentials and details.

6. Edit config.yml and enter the twitch access token, client id and client secret.

7. Edit config.yml and enter the twitch channel name and id to connect to.

9. Edit config.yml and enter your callback URL.

8. Edit config.yml and fill out the other details.

9. Configure Nginx to proxy this application using the `example-nginx-virtualhost.conf` file.

10. Run the database migrations.

    ```bash
    aerich upgrade
    ```

11. Run the application.

    ```bash
    python3 bot.py
    ```

## Enabling as a Systemd Service

1. Copy the `vanderwood-twitch-bot.service` file to `/etc/systemd/system/`.

2. Edit the file and change the `WorkingDirectory` and `ExecStart` paths to match your installation.

3. Reload the systemd daemon.

    ```bash
    sudo systemctl daemon-reload
    ```

4. Enable the service.

    ```bash
    sudo systemctl enable vanderwood-twitch-bot.service
    ```

5. Start the service.

    ```bash
    sudo systemctl start vanderwood-twitch-bot.service
    ```

## Updating

1. Pull the latest changes from the repository.

2. Run the database migrations.

    ```bash
    aerich upgrade
    ```

3. Restart the application.

    ```bash
    sudo systemctl restart vanderwood-twitch-bot.service
    ```