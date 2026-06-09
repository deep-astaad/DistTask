from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "disttask"
    postgres_user: str = "disttask"
    postgres_password: str = "disttask"

    redis_host: str = "redis"
    redis_port: int = 6379

    worker_concurrency: int = 4
    visibility_timeout: int = 60

    default_queue: str = "default"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def postgres_url(self):
        return (
            f"postgresql+psycopg://"
            f"{self.postgres_user}:"
            f"{self.postgres_password}@"
            f"{self.postgres_host}:"
            f"{self.postgres_port}/"
            f"{self.postgres_db}"
        )


settings = Settings()
