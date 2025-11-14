"""
نظام التصنيف الذكي للبلاغات
يحلل النص والمرفقات ويحدد نوع القضية: مدني أو جزائي
"""
import re
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class CaseClassifier:
    """محلل ذكي لتصنيف البلاغات"""
    
    def __init__(self):
        # الكلمات المفتاحية للقضايا الجزائية
        self.criminal_keywords = {
            # جرائم العنف
            'عنف': 10,
            'اعتداء': 10,
            'ضرب': 10,
            'اعتدى': 10,
            'ضربني': 10,
            'ضربه': 10,
            'عنف جسدي': 12,
            'اعتداء جسدي': 12,
            
            # جرائم السرقة
            'سرقة': 10,
            'سرق': 10,
            'سارق': 10,
            'مسروق': 10,
            'نشل': 10,
            'اختلاس': 10,
            
            # جرائم التهديد والابتزاز
            'تهديد': 10,
            'هددني': 10,
            'يهددني': 10,
            'ابتزاز': 12,
            'يبتزني': 12,
            'تهديد بالقتل': 15,
            
            # جرائم الاحتيال
            'احتيال': 10,
            'نصب': 10,
            'خداع': 8,
            'تزوير': 10,
            'مزور': 10,
            'تزييف': 10,
            
            # جرائم إتلاف الممتلكات
            'إتلاف': 10,
            'تخريب': 10,
            'كسر': 8,
            'حرق': 10,
            'دمر': 10,
            'خرب': 10,
            
            # جرائم خطيرة
            'قتل': 15,
            'قاتل': 15,
            'قتله': 15,
            'خطف': 15,
            'اختطاف': 15,
            'اغتصاب': 15,
            
            # مخدرات وسلاح
            'مخدرات': 12,
            'سلاح': 12,
            'مسدس': 12,
            'سكين': 10,
            
            # مصطلحات جنائية
            'جريمة': 8,
            'جنحة': 10,
            'جناية': 12,
            'مجرم': 8,
            'متهم': 8,
            'شرطة': 5,
            'بلاغ': 5,
        }
        
        # الكلمات المفتاحية للقضايا المدنية
        self.civil_keywords = {
            # قضايا مالية
            'دين': 10,
            'مديون': 10,
            'مطالبة مالية': 12,
            'مبلغ مالي': 10,
            'أموال': 8,
            'فلوس': 8,
            'ذمة مالية': 12,
            'مال': 8,
            
            # العقود والاتفاقيات
            'عقد': 10,
            'اتفاقية': 10,
            'اتفاق': 8,
            'شرط': 6,
            'شروط': 6,
            'التزام': 8,
            'ملتزم': 8,
            'إخلال بالعقد': 12,
            
            # الإيجارات
            'إيجار': 10,
            'مستأجر': 10,
            'مؤجر': 10,
            'شقة': 8,
            'محل': 8,
            'عقار': 8,
            'تأمين': 8,
            
            # قضايا العمل
            'عمل': 6,
            'موظف': 6,
            'راتب': 10,
            'مرتب': 10,
            'فصل تعسفي': 12,
            'استقالة': 8,
            'نهاية خدمة': 10,
            'مكافأة': 8,
            
            # التعويضات
            'تعويض': 10,
            'ضرر': 8,
            'أضرار': 8,
            'خسارة': 8,
            'خسائر': 8,
            
            # الأسرة والأحوال الشخصية
            'طلاق': 10,
            'نفقة': 10,
            'حضانة': 10,
            'زيارة': 8,
            'ميراث': 10,
            'وراثة': 10,
            'تركة': 10,
            
            # الملكية
            'ملكية': 10,
            'مالك': 8,
            'ملك': 8,
            'نزاع ملكية': 12,
            
            # مصطلحات مدنية
            'محكمة مدنية': 12,
            'قضية مدنية': 12,
            'دعوى': 8,
            'مدعي': 8,
            'مدعى عليه': 8,
        }
        
    def analyze_text(self, text: str) -> Dict[str, any]:
        """
        تحليل النص وتحديد نوع القضية
        
        Args:
            text: النص المراد تحليله
            
        Returns:
            قاموس يحتوي على:
            - case_type: نوع القضية (civil, criminal, unknown)
            - confidence: نسبة الثقة (0-100)
            - reasoning: الأسباب
        """
        if not text or len(text.strip()) < 10:
            return {
                'case_type': 'unknown',
                'confidence': 0.0,
                'reasoning': 'النص قصير جداً أو فارغ'
            }
        
        # تنظيف النص
        text = text.lower().strip()
        
        # حساب النقاط لكل فئة
        criminal_score = 0
        civil_score = 0
        
        criminal_matches = []
        civil_matches = []
        
        # البحث عن كلمات مفتاحية جزائية
        for keyword, weight in self.criminal_keywords.items():
            if keyword in text:
                count = text.count(keyword)
                score = weight * count
                criminal_score += score
                criminal_matches.append(f"{keyword} ({count}x)")
        
        # البحث عن كلمات مفتاحية مدنية
        for keyword, weight in self.civil_keywords.items():
            if keyword in text:
                count = text.count(keyword)
                score = weight * count
                civil_score += score
                civil_matches.append(f"{keyword} ({count}x)")
        
        # تحليل إضافي: أنماط معينة
        
        # نمط المبالغ المالية (مؤشر على قضية مدنية)
        money_patterns = [
            r'\d+\s*(درهم|دينار|ريال|دولار)',
            r'\d+\s*(ألف|آلاف)',
            r'مبلغ\s+\d+',
        ]
        for pattern in money_patterns:
            if re.search(pattern, text):
                civil_score += 5
                civil_matches.append("ذكر مبالغ مالية")
                break
        
        # نمط الجرائم الخطيرة
        serious_crime_patterns = [
            r'(تعرضت|تعرض)\s+(ل|إلى)\s+(اعتداء|ضرب|سرقة)',
            r'(قام|قامت)\s+ب(ضرب|اعتداء|سرقة)',
        ]
        for pattern in serious_crime_patterns:
            if re.search(pattern, text):
                criminal_score += 10
                criminal_matches.append("نمط جريمة واضح")
                break
        
        # تحديد النوع والثقة
        total_score = criminal_score + civil_score
        
        if total_score == 0:
            return {
                'case_type': 'unknown',
                'confidence': 0.0,
                'reasoning': 'لم يتم العثور على كلمات مفتاحية واضحة'
            }
        
        # حساب نسبة الثقة
        if criminal_score > civil_score:
            case_type = 'criminal'
            confidence = min((criminal_score / (civil_score + criminal_score)) * 100, 99.0)
            reasoning = f"تم تحديد {len(criminal_matches)} مؤشر جزائي: {', '.join(criminal_matches[:5])}"
        elif civil_score > criminal_score:
            case_type = 'civil'
            confidence = min((civil_score / (civil_score + criminal_score)) * 100, 99.0)
            reasoning = f"تم تحديد {len(civil_matches)} مؤشر مدني: {', '.join(civil_matches[:5])}"
        else:
            case_type = 'unknown'
            confidence = 50.0
            reasoning = 'المؤشرات متساوية بين مدني وجزائي'
        
        return {
            'case_type': case_type,
            'confidence': round(confidence, 2),
            'reasoning': reasoning,
            'criminal_score': criminal_score,
            'civil_score': civil_score,
        }
    
    def classify_case(
        self, 
        request_details: str, 
        petition_text: str = None, 
        attachments_text: List[str] = None
    ) -> Tuple[str, float, str]:
        """
        تصنيف القضية بناءً على كل المعلومات المتاحة
        
        Args:
            request_details: تفاصيل الطلب
            petition_text: نص العريضة (اختياري)
            attachments_text: قائمة النصوص المستخرجة من المرفقات (اختياري)
            
        Returns:
            tuple: (نوع القضية, نسبة الثقة, التفسير)
        """
        try:
            # دمج كل النصوص
            full_text = request_details or ""
            
            if petition_text:
                full_text += " " + petition_text
            
            if attachments_text:
                full_text += " " + " ".join(attachments_text)
            
            # تحليل النص الكامل
            result = self.analyze_text(full_text)
            
            logger.info(
                f"تصنيف البلاغ: {result['case_type']} "
                f"(ثقة: {result['confidence']}%) - {result['reasoning']}"
            )
            
            return (
                result['case_type'],
                result['confidence'],
                result['reasoning']
            )
            
        except Exception as e:
            logger.error(f"خطأ في تصنيف البلاغ: {str(e)}")
            return ('unknown', 0.0, f'خطأ في التحليل: {str(e)}')


# إنشاء نسخة واحدة من المصنف
classifier = CaseClassifier()


