import yaml

with open("config.yaml", "r") as stream:
    config_options = yaml.safe_load(stream)

if config_options["APP"]["MODE"] == "TEST":
    database_config = config_options["APP"]["TEST_DATABASE"]
elif config_options["APP"]["MODE"] == "PROD":
    database_config = config_options["APP"]["DATABASE"]
else:
    print("Invalid mode, please set to either TEST or PROD.")
    exit(1)

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
