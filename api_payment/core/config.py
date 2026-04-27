from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NAME_DB: str
    USERNAME_DB: str
    PASSWORD_DB: str
    HOST_DB: str
    PORT_DB: int

    class Config:
        env_file = ".env"

    @property
    def SYNC_LINK_PG(self):
        return f'postgresql+psycopg2://{self.USERNAME_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}'

    @property
    def ASYNC_LINK_PG(self):
        return f'postgresql+asyncpg://{self.USERNAME_DB}:{self.PASSWORD_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}'

settings = Settings()