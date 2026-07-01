"""
AppConfig - Cấu hình chính của ứng dụng Screen Translate Pro

Quản lý:
- Thông tin ứng dụng (phiên bản, tên, v.v.)
- Đường dẫn các thư mục
- Cài đặt chung
- Đọc/ghi cấu hình từ file JSON
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict


@dataclass
class AppConfig:
    """
    Cấu hình chính của ứng dụng.
    
    Attributes:
        app_name: Tên ứng dụng
        version: Phiên bản ứng dụng
        author: Tác giả
        description: Mô tả ứng dụng
        debug: Chế độ debug
        min_interval: Khoảng thời gian tối thiểu giữa các lần OCR (ms)
        enable_cache: Bật cache
        cache_size: Kích thước cache (MB)
        auto_startup: Tự động khởi động cùng Windows
        language: Ngôn ngữ mặc định
    """
    
    app_name: str = "Screen Translate Pro"
    version: str = "1.0.0"
    author: str = "Screen Translate Team"
    description: str = "Real-time screen translation for Windows"
    debug: bool = False
    min_interval: int = 100  # milliseconds
    enable_cache: bool = True
    cache_size: int = 100  # MB
    auto_startup: bool = False
    language: str = "vi"
    
    # Đường dẫn
    _base_path: Optional[Path] = None
    
    @classmethod
    def get_base_path(cls) -> Path:
        """
        Lấy đường dẫn cơ sở của ứng dụng.
        
        Returns:
            Path: Đường dẫn thư mục gốc của ứng dụng
        """
        if cls._base_path is None:
            if getattr(cls, '_is_frozen', False):
                # Chạy từ PyInstaller
                cls._base_path = Path(os.sys.executable).parent
            else:
                # Chạy từ source
                cls._base_path = Path(__file__).parent.parent
        return cls._base_path
    
    @classmethod
    def get_config_dir(cls) -> Path:
        """
        Lấy đường dẫn thư mục cấu hình.
        
        Returns:
            Path: Đường dẫn thư mục config
        """
        config_dir = cls.get_base_path() / "config"
        config_dir.mkdir(exist_ok=True)
        return config_dir
    
    @classmethod
    def get_logs_dir(cls) -> Path:
        """
        Lấy đường dẫn thư mục logs.
        
        Returns:
            Path: Đường dẫn thư mục logs
        """
        logs_dir = cls.get_base_path() / "logs"
        logs_dir.mkdir(exist_ok=True)
        return logs_dir
    
    @classmethod
    def get_database_dir(cls) -> Path:
        """
        Lấy đường dẫn thư mục database.
        
        Returns:
            Path: Đường dẫn thư mục database
        """
        db_dir = cls.get_base_path() / "database"
        db_dir.mkdir(exist_ok=True)
        return db_dir
    
    @classmethod
    def get_cache_dir(cls) -> Path:
        """
        Lấy đường dẫn thư mục cache.
        
        Returns:
            Path: Đường dẫn thư mục cache
        """
        cache_dir = cls.get_base_path() / "cache"
        cache_dir.mkdir(exist_ok=True)
        return cache_dir
    
    @classmethod
    def get_assets_dir(cls) -> Path:
        """
        Lấy đường dẫn thư mục assets.
        
        Returns:
            Path: Đường dẫn thư mục assets
        """
        assets_dir = cls.get_base_path() / "assets"
        assets_dir.mkdir(exist_ok=True)
        return assets_dir
    
    @classmethod
    def get_config_file_path(cls) -> Path:
        """
        Lấy đường dẫn file cấu hình JSON.
        
        Returns:
            Path: Đường dẫn file config.json
        """
        return cls.get_config_dir() / "app_config.json"
    
    @classmethod
    def load_from_file(cls) -> "AppConfig":
        """
        Tải cấu hình từ file JSON.
        
        Nếu file không tồn tại, sẽ trả về cấu hình mặc định.
        
        Returns:
            AppConfig: Đối tượng cấu hình đã tải
        """
        config_file = cls.get_config_file_path()
        
        if not config_file.exists():
            return cls()
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Loại bỏ các key không hợp lệ
            valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
            data = {k: v for k, v in data.items() if k in valid_keys and k != '_base_path'}
            
            return cls(**data)
        except (json.JSONDecodeError, TypeError) as e:
            if cls.debug:
                print(f"Error loading config: {e}")
            return cls()
    
    def save_to_file(self) -> bool:
        """
        Lưu cấu hình vào file JSON.
        
        Returns:
            bool: True nếu lưu thành công, False nếu thất bại
        """
        config_file = self.get_config_file_path()
        
        try:
            # Chuyển đổi dataclass thành dict
            data = asdict(self)
            # Loại bỏ _base_path vì nó không cần lưu
            data.pop('_base_path', None)
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            
            return True
        except (IOError, TypeError) as e:
            if self.debug:
                print(f"Error saving config: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi cấu hình thành dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary chứa cấu hình
        """
        data = asdict(self)
        data.pop('_base_path', None)
        return data
    
    def update(self, **kwargs: Any) -> None:
        """
        Cập nhật cấu hình với các giá trị mới.
        
        Args:
            **kwargs: Các cặp khóa-giá trị cần cập nhật
        """
        for key, value in kwargs.items():
            if hasattr(self, key) and key != '_base_path':
                setattr(self, key, value)
    
    def __repr__(self) -> str:
        """
        Biểu diễn chuỗi của đối tượng cấu hình.
        
        Returns:
            str: Chuỗi biểu diễn
        """
        data = self.to_dict()
        return f"AppConfig({data})"
