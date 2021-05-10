from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool
    its_test: bool
    actual_db_url: str
    test_db_url: str
    secret_key: str
    access_token_expire_minutes: int = 60 * 24 * 8  # 60 minutes * 24 hours * 8 days = 8 days
    super_user_email: str
    super_user_password: str

    @property
    def sqlalchemy_url(self):
        return self.test_db_url if self.its_test else self.actual_db_url

    class Config:
        env_file = '.env'


settings = Settings()

