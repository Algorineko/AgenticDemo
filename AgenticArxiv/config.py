# AgenticArxiv/config.py
from dataclasses import dataclass
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # 也可以直接在终端 export 环境变量
    pass


@dataclass(frozen=True)
class LLMModels:
    agent_model: str = "gemini-3-pro-preview"
    translate_model: str = "tab_flash_lite_preview"


@dataclass(frozen=True)
class Settings:
    antigravity_base_url: str = os.getenv("LLM_BASE_URL", "https://antigravity.byssted.cn")
    antigravity_api_key: str = os.getenv("LLM_API_KEY", "no-token-here")
    models: LLMModels = LLMModels()


settings = Settings()
