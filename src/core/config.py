from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Carrega variáveis de ambiente e expõe configurações tipadas.
    @property {str} database_url - URL de conexão com Postgres.
    @property {str} openai_api_key - Chave da OpenAI.
    """
    app_env: str = "development"
    secret_key: str = "change-me"
    database_url: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    class Config:
        env_file = ".env"

settings = Settings()
