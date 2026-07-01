"""
TranslatorConfig - Cấu hình các engine dịch

Quản lý:
- Thông tin các engine dịch (Google, DeepL, OpenAI, LibreTranslate)
- API keys
- Cài đặt dành riêng cho từng engine
- Lựa chọn engine mặc định
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
from enum import Enum


class TranslatorEngine(str, Enum):
    """
    Các engine dịch được hỗ trợ.
    """
    GOOGLE = "google"
    DEEPL = "deepl"
    OPENAI = "openai"
    LIBRE_TRANSLATE = "libre_translate"
    MICROSOFT = "microsoft"


@dataclass
class GoogleTranslateConfig:
    """
    Cấu hình Google Translate.
    
    Attributes:
        enabled: Bật/tắt engine
        api_key: API key (không bắt buộc, có thể sử dụng free)
        region: Vùng (default, us, eu)
    """
    enabled: bool = True
    api_key: str = ""
    region: str = "default"


@dataclass
class DeepLConfig:
    """
    Cấu hình DeepL Translator.
    
    Attributes:
        enabled: Bật/tắt engine
        api_key: API key (bắt buộc)
        api_type: Loại API (free hoặc pro)
        server_url: URL server (tuỳ chỉnh nếu cần)
    """
    enabled: bool = False
    api_key: str = ""
    api_type: str = "free"  # "free" hoặc "pro"
    server_url: str = ""


@dataclass
class OpenAIConfig:
    """
    Cấu hình OpenAI API.
    
    Attributes:
        enabled: Bật/tắt engine
        api_key: API key (bắt buộc)
        model: Model (gpt-3.5-turbo, gpt-4, v.v.)
        temperature: Độ sáng tạo (0.0 - 1.0)
        max_tokens: Số token tối đa
    """
    enabled: bool = False
    api_key: str = ""
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.3
    max_tokens: int = 500


@dataclass
class LibreTranslateConfig:
    """
    Cấu hình LibreTranslate.
    
    Attributes:
        enabled: Bật/tắt engine
        api_url: URL API server
        api_key: API key (nếu cần)
    """
    enabled: bool = False
    api_url: str = "https://libretranslate.de"
    api_key: str = ""


@dataclass
class MicrosoftTranslatorConfig:
    """
    Cấu hình Microsoft Translator.
    
    Attributes:
        enabled: Bật/tắt engine
        api_key: API key (bắt buộc)
        region: Vùng (bắt buộc)
        endpoint: Endpoint API
    """
    enabled: bool = False
    api_key: str = ""
    region: str = ""
    endpoint: str = "https://api.cognitive.microsofttranslator.com"


@dataclass
class TranslatorConfig:
    """
    Cấu hình chính cho tất cả các engine dịch.
    
    Quản lý:
    - Cấu hình cho từng engine
    - Engine mặc định
    - Cài đặt chung
    """
    
    # Engine mặc định
    default_engine: TranslatorEngine = TranslatorEngine.GOOGLE
    
    # Fallback engines nếu engine chính thất bại
    fallback_engines: list[TranslatorEngine] = field(default_factory=lambda: [
        TranslatorEngine.DEEPL,
        TranslatorEngine.LIBRE_TRANSLATE,
    ])
    
    # Cấu hình từng engine
    google: GoogleTranslateConfig = field(default_factory=GoogleTranslateConfig)
    deepl: DeepLConfig = field(default_factory=DeepLConfig)
    openai: OpenAIConfig = field(default_factory=OpenAIConfig)
    libre_translate: LibreTranslateConfig = field(default_factory=LibreTranslateConfig)
    microsoft: MicrosoftTranslatorConfig = field(default_factory=MicrosoftTranslatorConfig)
    
    # Cài đặt chung
    timeout: int = 10  # seconds
    retry_count: int = 3
    retry_delay: int = 1  # seconds
    cache_translations: bool = True
    
    def get_engine_config(self, engine: TranslatorEngine) -> Optional[Dict[str, Any]]:
        """
        Lấy cấu hình của một engine cụ thể.
        
        Args:
            engine: Engine cần lấy cấu hình
            
        Returns:
            Dict[str, Any]: Dictionary chứa cấu hình engine, hoặc None nếu engine không tồn tại
        """
        config_map = {
            TranslatorEngine.GOOGLE: self.google,
            TranslatorEngine.DEEPL: self.deepl,
            TranslatorEngine.OPENAI: self.openai,
            TranslatorEngine.LIBRE_TRANSLATE: self.libre_translate,
            TranslatorEngine.MICROSOFT: self.microsoft,
        }
        
        config = config_map.get(engine)
        if config:
            return asdict(config)
        return None
    
    def is_engine_available(self, engine: TranslatorEngine) -> bool:
        """
        Kiểm tra xem engine có sẵn dùng không.
        
        Một engine được coi là sẵn dùng nếu:
        - Được kích hoạt (enabled = True)
        - Có đủ thông tin cấu hình (API key nếu cần)
        
        Args:
            engine: Engine cần kiểm tra
            
        Returns:
            bool: True nếu engine sẵn dùng, False nếu không
        """
        config_map = {
            TranslatorEngine.GOOGLE: self.google,
            TranslatorEngine.DEEPL: self.deepl,
            TranslatorEngine.OPENAI: self.openai,
            TranslatorEngine.LIBRE_TRANSLATE: self.libre_translate,
            TranslatorEngine.MICROSOFT: self.microsoft,
        }
        
        config = config_map.get(engine)
        if not config or not config.enabled:
            return False
        
        # Kiểm tra API key nếu cần
        if engine in [TranslatorEngine.DEEPL, TranslatorEngine.OPENAI, TranslatorEngine.MICROSOFT]:
            return bool(config.api_key)
        
        return True
    
    def get_available_engines(self) -> list[TranslatorEngine]:
        """
        Lấy danh sách tất cả các engine sẵn dùng.
        
        Returns:
            list[TranslatorEngine]: Danh sách các engine có sẵn
        """
        available = []
        for engine in TranslatorEngine:
            if self.is_engine_available(engine):
                available.append(engine)
        return available
    
    def set_default_engine(self, engine: TranslatorEngine) -> bool:
        """
        Đặt engine mặc định.
        
        Args:
            engine: Engine được chọn làm mặc định
            
        Returns:
            bool: True nếu engine có sẵn, False nếu engine không sẵn dùng
        """
        if self.is_engine_available(engine):
            self.default_engine = engine
            return True
        return False
    
    def update_engine_config(self, engine: TranslatorEngine, **kwargs: Any) -> bool:
        """
        Cập nhật cấu hình của một engine.
        
        Args:
            engine: Engine cần cập nhật
            **kwargs: Các tham số cần cập nhật
            
        Returns:
            bool: True nếu cập nhật thành công, False nếu engine không tồn tại
        """
        config_map = {
            TranslatorEngine.GOOGLE: self.google,
            TranslatorEngine.DEEPL: self.deepl,
            TranslatorEngine.OPENAI: self.openai,
            TranslatorEngine.LIBRE_TRANSLATE: self.libre_translate,
            TranslatorEngine.MICROSOFT: self.microsoft,
        }
        
        config = config_map.get(engine)
        if config:
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi cấu hình thành dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary chứa toàn bộ cấu hình
        """
        return asdict(self)
    
    def __repr__(self) -> str:
        """
        Biểu diễn chuỗi của cấu hình.
        
        Returns:
            str: Chuỗi biểu diễn
        """
        return f"TranslatorConfig(default_engine={self.default_engine}, available={self.get_available_engines()})"
