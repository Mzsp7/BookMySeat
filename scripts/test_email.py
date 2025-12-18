"""
Test Email Configuration Script
Run this to verify your email settings are working correctly.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    print("📧 Testing Email Configuration...\n")
    print(f"Backend: {settings.EMAIL_BACKEND}")
    print(f"Host: {settings.EMAIL_HOST}")
    print(f"Port: {settings.EMAIL_PORT}")
    print(f"From: {settings.EMAIL_HOST_USER}\n")
    
    # Get recipient email
    recipient = input("Enter recipient email address (or press Enter to use EMAIL_HOST_USER): ").strip()
    if not recipient:
        recipient = settings.EMAIL_HOST_USER
    
    print(f"\n📤 Sending test email to: {recipient}")
    
    try:
        send_mail(
            subject='🎬 BookMySeat - Test Email',
            message='''
Hello!

This is a test email from your BookMySeat application.

If you're seeing this, your email configuration is working correctly! ✅

Movie booking confirmation emails will be sent from this address.

---
BookMySeat Team
            ''',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[recipient],
            fail_silently=False
        )
        
        print("\n✅ Email sent successfully!")
        
        if 'console' in settings.EMAIL_BACKEND.lower():
            print("\n⚠️  NOTE: You're using Console Backend")
            print("   The email was printed above, not actually sent.")
            print("   To send real emails, update EMAIL_BACKEND in settings.py")
        else:
            print(f"\n📬 Check the inbox for: {recipient}")
            
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        print("\nTroubleshooting:")
        print("1. Check your Gmail App Password is correct")
        print("2. Ensure 2-Step Verification is enabled")
        print("3. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in settings.py")
        print("4. Check your internet connection")

if __name__ == '__main__':
    test_email()
