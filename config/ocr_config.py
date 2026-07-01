"""
OCRConfig - Cấu hình cho OCR Engine (PaddleOCR)

Quản lý:
- Các ngôn ngữ được hỗ trợ
- Model settings
- GPU/CPU configuration
- Performance tuning
"""

from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional
from enum import Enum


class OCRLanguage(str, Enum):
    """
    Các ngôn ngữ được hỗ trợ bởi PaddleOCR.
    """
    ENGLISH = "en"
    CHINESE_SIMPLIFIED = "ch"  # Tiếng Trung Quốc Giản Thể
    CHINESE_TRADITIONAL = "zh"  # Tiếng Trung Quốc Phồn Thể
    JAPANESE = "ja"
    KOREAN = "ko"
    RUSSIAN = "ru"
    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
    PORTUGUESE = "pt"
    ARABIC = "ar"
    CYRILLIC = "cyrillic"
    DEVANAGARI = "devanagari"


@dataclass
class OCRConfig:
    """
    Cấu hình cho PaddleOCR.
    
    Attributes:
        enabled: Bật/tắt OCR
        use_gpu: Sử dụng GPU (CUDA)
        gpu_id: ID của GPU cần sử dụng (0, 1, 2, ...)
        model_dir: Thư mục lưu model
        lang_list: Danh sách các ngôn ngữ cần nhận diện
        auto_lang_detect: Tự động nhận diện ngôn ngữ
        confidence_threshold: Ngưỡng tin cậy tối thiểu (0.0 - 1.0)
        text_threshold: Ngưỡng văn bản (0.0 - 1.0)
        nms_threshold: NMS threshold
        max_batch_size: Kích thước batch tối đa
        rec_image_shape: Kích thước ảnh nhận diện (width, height)
        det_db_thresh: DB thresh parameter
        det_db_box_thresh: DB box thresh parameter
        det_db_unclip_ratio: DB unclip ratio
        enable_mkldnn: Sử dụng MKL-DNN (tối ưu CPU)
        thread_num: Số threads (cho CPU)
        timeout: Timeout cho mỗi lần OCR (milliseconds)
        enable_cache: Bật cache cho các kết quả OCR
    """
    
    enabled: bool = True
    use_gpu: bool = True
    gpu_id: int = 0
    model_dir: Optional[str] = None
    
    # Ngôn ngữ
    lang_list: list[OCRLanguage] = field(default_factory=lambda: [
        OCRLanguage.ENGLISH,
        OCRLanguage.CHINESE_SIMPLIFIED,
        OCRLanguage.JAPANESE,
        OCRLanguage.KOREAN,
    ])
    auto_lang_detect: bool = True
    
    # Thresholds
    confidence_threshold: float = 0.5
    text_threshold: float = 0.5
    nms_threshold: float = 0.3
    
    # Batch processing
    max_batch_size: int = 10
    
    # Model parameters
    rec_image_shape: tuple[int, int, int] = (3, 32, 320)  # (channels, height, width)
    det_db_thresh: float = 0.3
    det_db_box_thresh: float = 0.5
    det_db_unclip_ratio: float = 1.6
    
    # CPU optimization
    enable_mkldnn: bool = True
    thread_num: int = 4
    
    # Performance
    timeout: int = 5000  # milliseconds
    enable_cache: bool = True
    cache_max_size: int = 1000  # số lần OCR tối đa được cache
    
    def get_lang_list_str(self) -> str:
        """
        Lấy danh sách ngôn ngữ dưới dạng chuỗi.
        
        PaddleOCR sử dụng format "en,ch,ja,ko" cho lang_list.
        
        Returns:
            str: Chuỗi danh sách ngôn ngữ
        """
        return ",".join([lang.value for lang in self.lang_list])
    
    def add_language(self, lang: OCRLanguage) -> None:
        """
        Thêm một ngôn ngữ vào danh sách.
        
        Args:
            lang: Ngôn ngữ cần thêm
        """
        if lang not in self.lang_list:
            self.lang_list.append(lang)
    
    def remove_language(self, lang: OCRLanguage) -> None:
        """
        Xoá một ngôn ngữ khỏi danh sách.
        
        Args:
            lang: Ngôn ngữ cần xoá
        """
        if lang in self.lang_list and len(self.lang_list) > 1:
            self.lang_list.remove(lang)
    
    def is_language_supported(self, lang: OCRLanguage) -> bool:
        """
        Kiểm tra xem ngôn ngữ có được hỗ trợ không.
        
        Args:
            lang: Ngôn ngữ cần kiểm tra
            
        Returns:
            bool: True nếu ngôn ngữ được hỗ trợ, False nếu không
        """
        return lang in self.lang_list
    
    def get_ocr_kwargs(self) -> Dict[str, Any]:
        """
        Lấy dictionary các tham số để truyền vào PaddleOCR.
        
        Returns:
            Dict[str, Any]: Dictionary chứa các tham số OCR
        """
        kwargs = {
            'use_gpu': self.use_gpu,
            'gpu_mem': 500,  # MB
            'lang': self.get_lang_list_str(),
            'det_db_thresh': self.det_db_thresh,
            'det_db_box_thresh': self.det_db_box_thresh,
            'det_db_unclip_ratio': self.det_db_unclip_ratio,
            'rec_image_shape': self.rec_image_shape,
            'enable_mkldnn': self.enable_mkldnn,
            'thread_num': self.thread_num,
        }
        
        if self.model_dir:
            kwargs['model_storage_directory'] = self.model_dir
        
        if self.use_gpu:
            kwargs['gpu_id'] = self.gpu_id
        
        return kwargs
    
    def get_detection_kwargs(self) -> Dict[str, Any]:
        """
        Lấy tham số cho phase detection.
        
        Returns:
            Dict[str, Any]: Dictionary chứa tham số detection
        """
        return {
            'det_db_thresh': self.det_db_thresh,
            'det_db_box_thresh': self.det_db_box_thresh,
            'det_db_unclip_ratio': self.det_db_unclip_ratio,
        }
    
    def get_recognition_kwargs(self) -> Dict[str, Any]:
        """
        Lấy tham số cho phase recognition.
        
        Returns:
            Dict[str, Any]: Dictionary chứa tham số recognition
        """
        return {
            'rec_image_shape': self.rec_image_shape,
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Chuyển đổi cấu hình thành dictionary.
        
        Returns:
            Dict[str, Any]: Dictionary chứa cấu hình
        """
        data = asdict(self)
        # Chuyển OCRLanguage enum thành string
        data['lang_list'] = [lang.value for lang in self.lang_list]
        return data
    
    def __repr__(self) -> str:
        """
        Biểu diễn chuỗi của cấu hình.
        
        Returns:
            str: Chuỗi biểu diễn
        """
        return (f"OCRConfig(use_gpu={self.use_gpu}, "
                f"languages={self.get_lang_list_str()}, "
                f"confidence={self.confidence_threshold})")
