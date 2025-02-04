from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key"
    ALLOWED_HOSTS: list = ["*"]
    DATABASE_URL: str = "sqlite:///./genomescript.db"
    
    # AI Model settings
    MODEL_PATH: str = "models/genomic_model.h5"
    
    # Blockchain settings
    ETH_NODE_URL: str = "http://localhost:8545"
    CONTRACT_ADDRESS: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings() 