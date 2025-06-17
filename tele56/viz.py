import requests

token = "7238510627:AAGun_5ePvYaBgrew6j7Z9rwzIIuJ2t9TWQ"  # Replace with your actual bot token
response = requests.get(f"https://api.telegram.org/bot{token}/getWebhookInfo")
print(response.json())
