from django.db import models
from account.models import Account
from user_auth.models import User
from shortuuid.django_fields import ShortUUIDField

TRANSACTION_TYPE = (
    ("transfer", "Transfer"),
    ("recieved", "Recieved"),
    ("withdraw", "Withdraw"),
    ("refund", "Refund"),
    ("payment_request", "Payment Request"),
    ("none", "None")
)

TRANSACTION_STATUS = (
    ("failed", "Failed"),
    ("completed", "completed"),
    ("withdraw", "Withdraw"),
    ("pending", "Pending"),
    ("processing", "Processing"),
    ("request_sent", "Request Sent"),
    ("request_processing", "Request Processing"),
    ("request_settled", "Request Settled"),
    ("request_rejected", "Rejected"),
)


class Transaction(models.Model):
    transaction_id = ShortUUIDField(
        unique=True, length=15, max_length=20, prefix="TRN")
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="user")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    description = models.CharField(max_length=1000, null=True, blank=True)
    reciever = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="reciever")
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="sender")

    reciever_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="reciever_account")
    sender_account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, related_name="sender_account")

    status = models.CharField(
        choices=TRANSACTION_STATUS, max_length=100, default="pending")
    transaction_type = models.CharField(
        choices=TRANSACTION_TYPE, max_length=100, default="none")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self) -> str:
        try:
            return f"{self.user}"
        except:
            return f"Transaction"
