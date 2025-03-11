from django.contrib import admin

from apps.bookings.models import TableLayoutModel


# Register your models here.
@admin.register(TableLayoutModel)
class TableLayoutModelAdmin(admin.ModelAdmin):
    pass