import yaml

with open("config.yaml", "r") as stream:
    config_options = yaml.safe_load(stream)

database_config = config_options["APP"]["DATABASE"]

TORTOISE = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "host": database_config["DBHOST"],
                "port": database_config["DBPORT"],
                "user": database_config["DBUSER"],
                "password": database_config["DBPASS"],
                "database": database_config["DBNAME"],
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": True,
    "timezone": "UTC",
}
