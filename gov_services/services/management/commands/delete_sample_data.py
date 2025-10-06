"""
Django management command to delete sample data
"""
from django.core.management.base import BaseCommand
from services.models import Inquiry, ServiceRequest


class Command(BaseCommand):
    help = 'حذف البيانات التجريبية من قاعدة البيانات'

    def handle(self, *args, **options):
        self.stdout.write("Deleting sample data...")
        
        # حذف الاستعلامات التجريبية
        sample_inquiries = Inquiry.objects.filter(
            phone__in=['test1@example.com', 'test2@example.com', 'test3@example.com']
        )
        deleted_inquiries = sample_inquiries.count()
        sample_inquiries.delete()
        self.stdout.write(f"Deleted {deleted_inquiries} sample inquiries")
        
        # حذف الطلبات التجريبية
        sample_requests = ServiceRequest.objects.filter(
            requester_email__contains='@email.com'
        )
        deleted_requests = sample_requests.count()
        sample_requests.delete()
        self.stdout.write(f"Deleted {deleted_requests} sample requests")
        
        # عرض الإحصائيات النهائية
        self.stdout.write("\nFinal Statistics:")
        self.stdout.write(f"Total Inquiries: {Inquiry.objects.count()}")
        self.stdout.write(f"Total Requests: {ServiceRequest.objects.count()}")
        
        self.stdout.write(self.style.SUCCESS("\nAll sample data deleted successfully!"))
        self.stdout.write("System is now ready for real inquiries only.")
