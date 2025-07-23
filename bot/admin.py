from django.contrib import admin
from .models import Client, StorageLocation, Box, PickupRequest, Notification, OrderSource


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_id', 'consent_given', 'created_at')
    search_fields = ('full_name', 'phone', 'telegram_id')
    list_filter = ('consent_given', 'created_at')


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'has_delivery', 'is_active')
    search_fields = ('name', 'address')
    list_filter = ('has_delivery', 'is_active')


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'location', 'size', 'is_active', 'created_at', 'end_date', 'extended_until')
    list_filter = ('size', 'is_active', 'created_at', 'end_date')
    search_fields = ('client__full_name',)
    autocomplete_fields = ['client', 'location']


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'address', 'preferred_date', 'preferred_time', 'is_completed')
    list_filter = ('preferred_date', 'is_completed')
    search_fields = ('client__full_name', 'address')
    autocomplete_fields = ['client']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'notification_type', 'box', 'sent_at')
    list_filter = ('notification_type', 'sent_at')
    search_fields = ('client__full_name', 'notification_type')
    autocomplete_fields = ['client', 'box']


@admin.register(OrderSource)
class OrderSourceAdmin(admin.ModelAdmin):
    list_display = ('client', 'utm_source', 'created_at')
    list_filter = ('utm_source', 'created_at')
    search_fields = ('client__full_name', 'utm_source')
    autocomplete_fields = ['client']