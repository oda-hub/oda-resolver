from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TNR",
    settings_files=['settings.toml', '.secrets.toml'],
    load_dotenv=True,
)