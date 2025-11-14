"""
نظام استخراج النص من الملفات (PDF, صور, مستندات)
"""
import logging
from typing import Optional
import os

logger = logging.getLogger(__name__)


class TextExtractor:
    """مستخرج النص من الملفات"""
    
    def __init__(self):
        """تهيئة المستخرج"""
        self.pdf_available = False
        self.ocr_available = False
        self.docx_available = False
        
        # محاولة استيراد المكتبات
        try:
            import PyPDF2
            self.pdf_available = True
            logger.info("PyPDF2 is available for PDF text extraction")
        except ImportError:
            logger.warning("PyPDF2 not available - PDF text extraction will be disabled")
        
        try:
            import pytesseract
            from PIL import Image
            self.ocr_available = True
            logger.info("Tesseract OCR is available for image text extraction")
        except ImportError:
            logger.warning("Tesseract OCR not available - Image text extraction will be disabled")
        
        try:
            import docx
            self.docx_available = True
            logger.info("python-docx is available for Word text extraction")
        except ImportError:
            logger.warning("python-docx not available - Word text extraction will be disabled")
    
    def extract_from_pdf(self, file_path: str) -> Optional[str]:
        """
        استخراج النص من ملف PDF
        
        Args:
            file_path: مسار الملف
            
        Returns:
            النص المستخرج أو None إذا فشل
        """
        if not self.pdf_available:
            return None
        
        try:
            import PyPDF2
            
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # استخراج النص من كل صفحة
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
            
            logger.info(f"✅ تم استخراج {len(text)} حرف من PDF: {os.path.basename(file_path)}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"❌ خطأ في استخراج النص من PDF: {str(e)}")
            return None
    
    def extract_from_image(self, file_path: str) -> Optional[str]:
        """
        استخراج النص من صورة باستخدام OCR
        
        Args:
            file_path: مسار الملف
            
        Returns:
            النص المستخرج أو None إذا فشل
        """
        if not self.ocr_available:
            return None
        
        try:
            import pytesseract
            from PIL import Image
            
            # فتح الصورة
            image = Image.open(file_path)
            
            # استخراج النص (عربي + إنجليزي)
            text = pytesseract.image_to_string(image, lang='ara+eng')
            
            logger.info(f"✅ تم استخراج {len(text)} حرف من الصورة: {os.path.basename(file_path)}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"❌ خطأ في استخراج النص من الصورة: {str(e)}")
            return None
    
    def extract_from_docx(self, file_path: str) -> Optional[str]:
        """
        استخراج النص من ملف Word
        
        Args:
            file_path: مسار الملف
            
        Returns:
            النص المستخرج أو None إذا فشل
        """
        if not self.docx_available:
            return None
        
        try:
            import docx
            
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            logger.info(f"✅ تم استخراج {len(text)} حرف من Word: {os.path.basename(file_path)}")
            return text.strip()
            
        except Exception as e:
            logger.error(f"❌ خطأ في استخراج النص من Word: {str(e)}")
            return None
    
    def extract_from_file(self, file_path: str, file_type: str = None) -> Optional[str]:
        """
        استخراج النص من أي نوع ملف
        
        Args:
            file_path: مسار الملف
            file_type: نوع الملف (اختياري، سيتم تحديده تلقائياً)
            
        Returns:
            النص المستخرج أو None إذا فشل
        """
        if not os.path.exists(file_path):
            logger.error(f"❌ الملف غير موجود: {file_path}")
            return None
        
        # تحديد نوع الملف من الامتداد
        if not file_type:
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                file_type = 'pdf'
            elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']:
                file_type = 'image'
            elif ext in ['.docx', '.doc']:
                file_type = 'doc'
            else:
                logger.warning(f"⚠️ نوع ملف غير مدعوم: {ext}")
                return None
        
        # استخراج النص حسب النوع
        if file_type == 'pdf':
            return self.extract_from_pdf(file_path)
        elif file_type == 'image':
            return self.extract_from_image(file_path)
        elif file_type == 'doc':
            return self.extract_from_docx(file_path)
        else:
            logger.warning(f"⚠️ نوع ملف غير مدعوم: {file_type}")
            return None
    
    def get_capabilities(self) -> dict:
        """
        الحصول على قدرات المستخرج
        
        Returns:
            قاموس بالقدرات المتاحة
        """
        return {
            'pdf': self.pdf_available,
            'ocr': self.ocr_available,
            'docx': self.docx_available,
        }


# إنشاء نسخة واحدة من المستخرج
text_extractor = TextExtractor()


