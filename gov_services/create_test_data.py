# -*- coding: utf-8 -*-
import os
import sys
import django
from django.contrib.auth.models import User

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gov_services.settings')
django.setup()

from services.models import Center, EmployeeProfile, Service, ServiceRequest

def create_test_data():
    print("Creating test data...")
    
    # Create Centers
    centers_data = [
        {"name": "Riyadh Main Center", "code": "RYD001", "location": "Riyadh - King Fahd District"},
        {"name": "Jeddah Main Center", "code": "JED001", "location": "Jeddah - Al Rawda District"},
        {"name": "Dammam Main Center", "code": "DMM001", "location": "Dammam - Al Faisaliah District"},
    ]
    
    centers = []
    for center_data in centers_data:
        center, created = Center.objects.get_or_create(
            code=center_data["code"],
            defaults=center_data
        )
        centers.append(center)
        if created:
            print(f"Created center: {center.name}")
    
    # Create Users and Employees
    employees_data = [
        {
            "username": "admin",
            "password": "admin123",
            "first_name": "Ahmed",
            "last_name": "Manager",
            "email": "admin@gov.sa",
            "role": "admin",
            "center": None
        },
        {
            "username": "emp_riyadh",
            "password": "emp123",
            "first_name": "Mohammed",
            "last_name": "Riyadh",
            "email": "emp.riyadh@gov.sa",
            "role": "center_staff",
            "center": centers[0]
        },
        {
            "username": "emp_jeddah",
            "password": "emp123",
            "first_name": "Fatima",
            "last_name": "Jeddah",
            "email": "emp.jeddah@gov.sa",
            "role": "center_staff",
            "center": centers[1]
        },
        {
            "username": "emp_dammam",
            "password": "emp123",
            "first_name": "Abdullah",
            "last_name": "Dammam",
            "email": "emp.dammam@gov.sa",
            "role": "center_staff",
            "center": centers[2]
        }
    ]
    
    for emp_data in employees_data:
        user, created = User.objects.get_or_create(
            username=emp_data["username"],
            defaults={
                "first_name": emp_data["first_name"],
                "last_name": emp_data["last_name"],
                "email": emp_data["email"],
                "is_staff": True
            }
        )
        
        if created:
            user.set_password(emp_data["password"])
            user.save()
            print(f"Created user: {user.username}")
        
        # Create Employee Profile
        employee_profile, created = EmployeeProfile.objects.get_or_create(
            user=user,
            defaults={
                "role": emp_data["role"],
                "center": emp_data["center"]
            }
        )
        
        if created:
            print(f"Created employee profile: {employee_profile}")
    
    # Create Test Services
    services_data = [
        {"name": "Birth Certificate", "slug": "birth-certificate"},
        {"name": "ID Renewal", "slug": "id-renewal"},
        {"name": "Passport", "slug": "passport"},
        {"name": "Criminal Record Certificate", "slug": "criminal-record"},
    ]
    
    services = []
    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            slug=service_data["slug"],
            defaults=service_data
        )
        services.append(service)
        if created:
            print(f"Created service: {service.name}")
    
    # Create Test Requests
    requests_data = [
        {
            "service": services[0],
            "full_name": "Sara Ahmed Mohammed",
            "email": "sara@example.com",
            "phone": "0501234567",
            "description": "Birth certificate for newborn child",
            "status": "pending",
            "priority": "medium",
            "center": centers[0]
        },
        {
            "service": services[1],
            "full_name": "Khalid Abdullah Saad",
            "email": "khalid@example.com",
            "phone": "0507654321",
            "description": "Renew expired national ID",
            "status": "in_progress",
            "priority": "high",
            "center": centers[0]
        },
        {
            "service": services[2],
            "full_name": "Nora Mohammed Ali",
            "email": "nora@example.com",
            "phone": "0551234567",
            "description": "Passport for travel abroad",
            "status": "pending",
            "priority": "low",
            "center": centers[1]
        },
        {
            "service": services[3],
            "full_name": "Omar Salem Ahmed",
            "email": "omar@example.com",
            "phone": "0559876543",
            "description": "Criminal record certificate for new job",
            "status": "completed",
            "priority": "medium",
            "center": centers[1]
        },
        {
            "service": services[0],
            "full_name": "Reem Fahd Mohammed",
            "email": "reem@example.com",
            "phone": "0501111111",
            "description": "Birth certificate for school registration",
            "status": "pending",
            "priority": "high",
            "center": centers[2]
        },
        {
            "service": services[1],
            "full_name": "Youssef Abdulrahman",
            "email": "youssef@example.com",
            "phone": "0502222222",
            "description": "Renew damaged national ID",
            "status": "rejected",
            "priority": "medium",
            "center": centers[2]
        }
    ]
    
    for req_data in requests_data:
        service_request, created = ServiceRequest.objects.get_or_create(
            email=req_data["email"],
            service=req_data["service"],
            defaults=req_data
        )
        
        if created:
            print(f"Created request: {service_request.full_name} - {service_request.service.name}")
    
    print("\n" + "="*50)
    print("Test data created successfully!")
    print("="*50)
    print("Login credentials:")
    print("Admin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nRiyadh Center Staff:")
    print("  Username: emp_riyadh")
    print("  Password: emp123")
    print("\nJeddah Center Staff:")
    print("  Username: emp_jeddah")
    print("  Password: emp123")
    print("\nDammam Center Staff:")
    print("  Username: emp_dammam")
    print("  Password: emp123")
    print("="*50)

if __name__ == "__main__":
    create_test_data()