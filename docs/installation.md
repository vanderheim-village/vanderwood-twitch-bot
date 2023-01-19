# Installation

## Requirements

* Ubuntu 20.04 or later
* Python 3.10 or later
* PostgreSQL 13 or later
* Nginx

## Installation Steps

1. Clone or download the repository.

1. Create a Python virtual environment and install the dependencies.

    <pre><code class="language-bash">python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    </code></pre>

1. Create a PostgreSQL database and user.

    <pre><code class="language-bash">sudo -u postgres psql
    CREATE DATABASE battleofmidgard;
    CREATE USER battleofmidgard WITH PASSWORD 'password';
    GRANT ALL PRIVILEGES ON DATABASE battleofmidgard TO battleofmidgard;
    </code></pre>

1. Make a copy of config.yml.example and rename it to config.yml.

    <pre><code class="language-bash">cp config.yml.example config.yml</code></pre>

1. Edit config.yml and add in the database credentials and details.

1. Edit config.yml and enter the twitch access token, client id and client secret.

1. Edit config.yml and enter the twitch channel name and id to connect to.

1. Edit config.yml and enter your callback URL.

1. Edit config.yml and fill out the other details.

1. Configure Nginx to proxy this application using the `example-nginx-virtualhost.conf` file.

1. Run the database migrations.

    <pre><code class="language-bash">aerich upgrade</code></pre>

1. Run the application.

    <pre><code class="language-bash">python3 bot.py</code></pre>

## Enabling as a Systemd Service

1. Copy the `vanderwood-twitch-bot.service` file to `/etc/systemd/system/`.

1. Edit the file and change the `WorkingDirectory` and `ExecStart` paths to match your installation.

1. Reload the systemd daemon.

    <pre><code class="language-bash">sudo systemctl daemon-reload</code></pre>

1. Enable the service.

    <pre><code class="language-bash">sudo systemctl enable vanderwood-twitch-bot.service</code></pre>

1. Start the service.

    <pre><code class="language-bash">sudo systemctl start vanderwood-twitch-bot.service</code></pre>

## Updating

1. Pull the latest changes from the repository.

1. Run the database migrations.

    <pre><code class="language-bash">aerich upgrade</code></pre>

1. Restart the application.

    <pre><code class="language-bash">sudo systemctl restart vanderwood-twitch-bot.service</code></pre>