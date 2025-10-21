from alembic.config import Config
from alembic import command

cfg = Config("backend/alembic.ini")
cfg.set_main_option("script_location", "backend/migrations")
command.upgrade(cfg, "head")
