from django.db import models
import uuid

# class Company(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255, null=False)
#     location = models.TextField(null=False)
#     email = models.EmailField(unique=True, null=False)
#     hashed_password = models.TextField(null=False)
#
#     class Meta:
#         db_table = "companies"
#
# class CompanySession(models.Model):
#     session_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()
#
#     class Meta:
#         db_table = "company_sessions"