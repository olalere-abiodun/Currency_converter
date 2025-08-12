# notifications.py
def send_notification(user_id: int, base_currency: str, target_currency: str, current_rate: float):
    """
    Send a notification to the user when the target rate is reached.
    Replace this with your actual email, SMS, or push service logic.
    """
    # This is just a placeholder print — replace with real notification logic.
    print(
        f"ALERT for User {user_id}: "
        f"{base_currency}/{target_currency} has reached {current_rate}"
    )
