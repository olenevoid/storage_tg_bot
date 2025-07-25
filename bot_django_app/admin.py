from django.contrib import admin
from django.utils.timezone import now
from datetime import timedelta

from .models import (
    Client, StorageLocation, Box, PickupRequest,
    Notification, OrderSource, StoredItem, PromoCode, PromoUsage
)

# --- ВСПОМОГАТЕЛЬНЫЕ КОМПОНЕНТЫ ---

# Фильтр "Заканчивается скоро"
class EndingSoonFilter(admin.SimpleListFilter):
    title = 'Заканчивается скоро'
    parameter_name = 'ending_soon'

    def lookups(self, request, model_admin):
        return (
            ('7days', 'В течение 7 дней'),
            ('30days', 'В течение 30 дней'),
        )

    def queryset(self, request, queryset):
        today = now().date()
        if self.value() == '7days':
            return queryset.filter(end_date__range=(today, today + timedelta(days=7)))
        if self.value() == '30days':
            return queryset.filter(end_date__range=(today, today + timedelta(days=30)))
        return queryset

# Inline: Предметы, хранящиеся в боксе
class StoredItemInline(admin.TabularInline):
    model = StoredItem
    extra = 1

# Actions для промокодов
@admin.action(description='Активировать выбранные промокоды')
def activate_promo_codes(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} промокодов активировано")

@admin.action(description='Деактивировать выбранные промокоды')
def deactivate_promo_codes(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} промокодов деактивировано")

# --- АДМИНКИ ---

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
        'days_until_end',
        'extended_until',
    )
    list_filter = ('size', 'is_active', 'created_at', 'end_date', EndingSoonFilter)
    search_fields = ('client__full_name', 'description')
    ordering = ('-created_at',)
    inlines = [StoredItemInline]

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name

    @admin.display(description="Телефон")
    def client_phone(self, obj):
        return obj.client.phone

    @admin.display(description="Склад")
    def location_name(self, obj):
        return obj.location.name if obj.location else '—'

    @admin.display(description="Дней до окончания")
    def days_until_end(self, obj):
        if obj.end_date:
            delta = (obj.end_date - now().date()).days
            return max(delta, 0)
        return '—'


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


@admin.register(StoredItem)
class StoredItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'box_id', 'client_name', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('name', 'box__client__full_name')
    ordering = ('-added_at',)

    @admin.display(description="Box ID")
    def box_id(self, obj):
        return obj.box.id

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.box.client.full_name


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_until')
    search_fields = ('code',)
    ordering = ('-valid_from',)
    actions = [activate_promo_codes, deactivate_promo_codes]


@admin.register(PromoUsage)
class PromoUsageAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'client_name', 'used_at')
    list_filter = ('used_at',)
    search_fields = ('promo__code', 'client__full_name')
    ordering = ('-used_at',)

    @admin.display(description="Промокод")
    def promo_code(self, obj):
        return obj.promo.code

    @admin.display(description="Клиент")
    def client_name(self, obj):
        return obj.client.full_name