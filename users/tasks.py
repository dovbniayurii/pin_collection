from celery import shared_task
import firebase_admin
from firebase_admin import messaging, credentials
from .models import FCMToken
from firebase_admin.exceptions import FirebaseError
import os
from pathlib import Path
import logging
logger = logging
   
@shared_task
def my_task():
    print('Task is running!')
    
    
import requests
from celery import shared_task
from django.conf import settings
from .models import FCMToken

FCM_URL = "https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
SERVER_KEY = "AAAA...your-server-key"  # From Firebase Console
PROJECT_ID = "distenypin-c9e72"  # From Firebase settings

@shared_task
def send_morning_push_notification():
    try:
        # Get valid tokens
        tokens = list(FCMToken.objects.values_list('token', flat=True))
        print(tokens)
        if not tokens:
            return "No tokens available"

        # Prepare headers
        headers = {
            "Authorization": f"Bearer {get_access_token()}",
            "Content-Type": "application/json",
        }

        successes = 0
        invalid_tokens = []

        for token in tokens:
            print(token)
            payload = {
                "message": {
                    "token": token,
                    "notification": {
                        "title": "Update Your Pins",
                        "body": "Don't forget to add today's collection!"
                    }
                }
            }

            response = requests.post(
                FCM_URL.format(project_id=PROJECT_ID),
                headers=headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                successes += 1
            elif response.status_code == 404:
                invalid_tokens.append(token)
            else:
                response.raise_for_status()

        # Clean invalid tokens
        if invalid_tokens:
            FCMToken.objects.filter(token__in=invalid_tokens).delete()

        return f"Sent: {successes}, Invalid tokens removed: {len(invalid_tokens)}"

    except Exception as e:
        return f"Error: {str(e)}"


def get_access_token():
    """Get OAuth2 access token using service account credentials"""
    auth_url = "https://oauth2.googleapis.com/token"
    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": create_signed_jwt()
    }
    response = requests.post(auth_url, data=data)
    return response.json()["access_token"]


def create_signed_jwt():
    """Create signed JWT for service account authentication"""
    from datetime import datetime, timedelta
    import jwt

    service_account_email = "firebase-adminsdk-fbsvc@distenypin-c9e72.iam.gserviceaccount.com"  # From credentials
    private_key = "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCmMrzZ5v46lKbR\n/fwqOoVHipvGhJQKxplwThBJGEO6ZdRSPk5xeKBGf9mTumixqxsA+IxEDb+9jPA/\nUmIEBVVL6rD21jmAZZ/ko2fRswfoz3CQYMVMMp+KsDBr02CMwHn1VXDDlveqhKWa\nXnQBmfjFAfzYEJhMbilTsmN7YHYvskoF4Ht0+n0r5Q8fPNhkrvBcJmHdZNHJz7jU\nYefw/hZeMzju486NH8GrQYKW9C+IYz0GBzZAGT7yZ/9d7htpJftDxpZyOGQ9oIDV\nyHO5EQKStRK/YiWqWEY7YyBWBpnCZcu65WudllnOhS8iEhk+0aKsbx4Swy2ol5nX\nMEVgeO1PAgMBAAECggEAQdrL8ynxJeQ+P+o8r7z1j9YQCLcC9Ewig5ojINuRBryP\nx7Dxo0vRcm35mGxeTLxInHdgGR07k0/T6LtrpD06wbSyv3Q+X66lD1NicXjX0vvT\nlhoKQ7mxdyJ+ZVNiKBOin8BlyNK6u2IJPqRbokDRDrtNZY4Z0vs5u/TtL3eXDSmc\nZ0qbgxJhmxrIyj5zM+gnaa4mOdzfFBdoiPrueX2/ZA4OTbdfHu6y0nbVmQ0v8vmk\nOFGMrXXWyuucntaXvkZRynTtHiX9zubFw1xjPJ0z6opUShhfTga6Sn7rh/Ons/4x\n4J6Kc9SBNBkdMM5VRpBoA/E91FmLgmQRL2hnSAnIaQKBgQDRm6TkvkZqeHUs0/wI\nhlpHp4g5nm80oxwpvYyCbTaewzHkjXb41X+ucoXmMnueocp2RzCqcqQI7FGm1tUX\ndWLUPXdzDyz/plLahLI7XngcwUtAUlRrG+UGY41iXcnkTWinan7vNbeyqhVkyTiy\nwaFWhjk+d4bHTqYfYmzjANmceQKBgQDK+4BntWDojD9Mo02nFkHRKO2OJN+6vtx7\nzEl3Wo9uFaKxek4krDdhLEQIFVyiEmzMJelj0CdkxfOSKyOoDSf5uVXAlVgoip69\non+Xpa1X1tzLMN5MKBffHkERIQDjaz18p4Casi41GRExtwX82wfxSyk2hjrFCfvG\nPY/aqF1WBwKBgQC2de93M28mlY8io7GcVh/Wii6aQaF6R5Zne1oJ2zoVv8L5um9b\nMrZ/y69lcIKN1zbf+R6S8VJ7dgOp4Q8D6apLKOqHHSnFrSookCR6a8TQ+y4fYsub\npV+bTSOxAgWSGBRGz/yJDNDI1SfkYQlbChUAtby09OU9L+iKH2q7vGyxuQKBgQCg\n5CdMjQVqbrhB2/NSLJ8w1hsuH2ZDVMPZUP0uoNatsHKL8OD9yo/+8yJdsekCAk7A\nppBPcI+5HfrJ8m3J59u24sPo6be+MtpOf/5YypcS2Bmc6XharzD0xrtWg2171eYf\n53lVpURhDCSH3oXdfhPWm/fn4w+0XQx3fxaGgAuzgwKBgCKkwBxRYhihN8aynVnq\nbxVxlXuHFHrAn67BEbTw4xbP4CbN3e2Uz6LcAwC4rmUh+wOU75iRpSHApTN7QzLs\nT4kpL1kl8FxRu0uz2qDpvuJHasdlgLWqp3BiVkWFEE4lOQ9lLkbKFfVssrwwFLNb\n3+suS/Iz7OdBTymPF6DidnBV\n-----END PRIVATE KEY-----\n"

    now = datetime.utcnow()
    payload = {
        "iss": service_account_email,
        "sub": service_account_email,
        "aud": "https://oauth2.googleapis.com/token",
        "iat": now,
        "exp": now + timedelta(hours=1),
        "scope": "https://www.googleapis.com/auth/firebase.messaging"
    }

    return jwt.encode(
        payload,
        private_key,
        algorithm="RS256",
        headers={"kid": "8fe7b8d7e00ad8a5b61a18be90da353a3a676b89"}  # From service account
    )