from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_DB: str
    REDIS_HOST: str
    REDIS_PORT: str
    AI_SERVICE_KEY: str
    SWAGGER_USERNAME: str
    SWAGGER_PASSWORD: str
    MONGO_INITDB_ROOT_PORT: str
    MONGO_INITDB_ROOT_HOST: str
    MONGO_INITDB_ROOT_DBNAME: str
    MONGO_INITDB_ROOT_USERNAME: str
    MONGO_INITDB_ROOT_PASSWORD: str

    @property
    def database_url(self) -> str:
        return (
            f"mongodb://{self.MONGO_INITDB_ROOT_USERNAME}:"
            f"{self.MONGO_INITDB_ROOT_PASSWORD}@"
            f"{self.MONGO_INITDB_ROOT_HOST}:"
            f"{self.MONGO_INITDB_ROOT_PORT}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
