from django.contrib import admin
from .models import Client, StorageLocation, Box, PickupRequest, Notification, OrderSource


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'telegram_id', 'email', 'consent_given', 'created_at')
    search_fields = ('full_name', 'phone', 'telegram_id', 'email')
    list_filter = ('consent_given', 'created_at')
    ordering = ('-created_at',)


@admin.register(StorageLocation)
class StorageLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'has_delivery', 'is_active')
    list_filter = ('has_delivery', 'is_active')
    search_fields = ('name', 'address')


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'client_name', 
        'client_phone',
        'size', 
        'location_name', 
        'is_active', 
        'created_at', 
        'end_date', 
        'extended_until'
    )
    list_filter = ('size', 'is_active', 'created_at', 'end_date')
    search_fields = ('client__full_name', 'description')
    ordering = ('-created_at',)

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name

    @admin.display(description="Телефон")
    def client_phone(self, obj):
        return obj.client.phone

    @admin.display(description="Склад")
    def location_name(self, obj):
        return obj.location.name if obj.location else '—'


@admin.register(PickupRequest)
class PickupRequestAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 
        'client_phone',
        'address', 
        'preferred_date', 
        'preferred_time', 
        'is_completed', 
        'created_at'
    )
    list_filter = ('preferred_date', 'is_completed')
    search_fields = ('client__full_name', 'address', 'comment')
    ordering = ('-created_at',)

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name

    @admin.display(description="Телефон")
    def client_phone(self, obj):
        return obj.client.phone


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 
        'client_phone',
        'notification_type', 
        'box_id', 
        'sent_at'
    )
    list_filter = ('notification_type', 'sent_at')
    search_fields = ('client__full_name', 'notification_type')
    ordering = ('-sent_at',)

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name

    @admin.display(description="Телефон")
    def client_phone(self, obj):
        return obj.client.phone

    @admin.display(description="Box ID")
    def box_id(self, obj):
        return obj.box.id if obj.box else '—'


@admin.register(OrderSource)
class OrderSourceAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 
        'client_phone',
        'utm_source', 
        'created_at'
    )
    list_filter = ('utm_source',)
    search_fields = ('client__full_name', 'utm_source')
    ordering = ('-created_at',)

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name

    @admin.display(description="Телефон")
    def client_phone(self, obj):
        return obj.client.phone