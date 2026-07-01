"""
Config Module - Quản lý cấu hình ứng dụng Screen Translate Pro

Module này chứa:
- AppConfig: Cấu hình chính của ứng dụng
- TranslatorConfig: Cấu hình các engine dịch
- OCRConfig: Cấu hình OCR
- OverlayConfig: Cấu hình overlay
- HotkeyConfig: Cấu hình hotkey
"""

from .app_config import AppConfig
from .translator_config import TranslatorConfig
from .ocr_config import OCRConfig
from .overlay_config import OverlayConfig
from .hotkey_config import HotkeyConfig

__all__ = [
    'AppConfig',
    'TranslatorConfig',
    'OCRConfig',
    'OverlayConfig',
    'HotkeyConfig',
]
