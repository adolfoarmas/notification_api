from src.celery import celery_app
import time

@celery_app.task
def send_sms_task(message_dict):
    # Implement your SMS sending logic here
    print(f"Sending SMS with details: {message_dict}")
    # Return True or any necessary result
    return True

@celery_app.task
def send_email_task(message_dict):
    # Implement your email sending logic here
    time.sleep(10)
    print(f"Sending Email with details: {message_dict}")
    # Return True or any necessary result
    return True

@celery_app.task
def send_push_task(message_dict):
    # Implement your push notification logic here
    print(f"Sending Push notification with details: {message_dict}")
    # Return True or any necessary result
    return True