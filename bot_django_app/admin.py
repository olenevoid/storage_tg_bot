from django.contrib import admin
from django.utils.timezone import now
from datetime import timedelta

from .models import (
    User, StorageLocation, Box, PickupRequest,
    Notification, OrderSource, StoredItem,
    PromoCode, PromoUsage,
    BoxSize, BoxAvailability, Role
)

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


class StoredItemInline(admin.TabularInline):
    model = StoredItem
    extra = 1


@admin.action(description='Активировать выбранные промокоды')
def activate_promo_codes(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(request, f"{updated} промокодов активировано")


@admin.action(description='Деактивировать выбранные промокоды')
def deactivate_promo_codes(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(request, f"{updated} промокодов деактивировано")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
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
        'user_name',
        'user_phone',
        'size',
        'location_name',
        'is_active',
        'created_at',
        'end_date',
        'days_until_end',
        'extended_until',
    )
    list_filter = ('size', 'is_active', 'created_at', 'end_date', EndingSoonFilter)
    search_fields = ('user__full_name', 'description')
    ordering = ('-created_at',)
    inlines = [StoredItemInline]

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Телефон")
    def user_phone(self, obj):
        return obj.user.phone

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
        'user_name',
        'user_phone',
        'type',
        'executor_name',
        'address',
        'preferred_date',
        'preferred_time',
        'status',
        'created_at',
    )
    list_filter = ('type', 'status', 'preferred_date')
    search_fields = ('user__full_name', 'address', 'comment', 'executor__full_name')
    ordering = ('-created_at',)

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Телефон")
    def user_phone(self, obj):
        return obj.user.phone

    @admin.display(description="Исполнитель")
    def executor_name(self, obj):
        return obj.executor.full_name if obj.executor else '—'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'user_name',
        'user_phone',
        'notification_type',
        'box_id',
        'sent_at'
    )
    list_filter = ('notification_type', 'sent_at')
    search_fields = ('user__full_name', 'notification_type')
    ordering = ('-sent_at',)

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Телефон")
    def user_phone(self, obj):
        return obj.user.phone

    @admin.display(description="Box ID")
    def box_id(self, obj):
        return obj.box.id if obj.box else '—'


@admin.register(OrderSource)
class OrderSourceAdmin(admin.ModelAdmin):
    list_display = (
        'user_name',
        'user_phone',
        'utm_source',
        'created_at'
    )
    list_filter = ('utm_source',)
    search_fields = ('user__full_name', 'utm_source')
    ordering = ('-created_at',)

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.user.full_name

    @admin.display(description="Телефон")
    def user_phone(self, obj):
        return obj.user.phone


@admin.register(StoredItem)
class StoredItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'box_id', 'user_name', 'added_at')
    list_filter = ('added_at',)
    search_fields = ('name', 'box__user__full_name')
    ordering = ('-added_at',)

    @admin.display(description="Box ID")
    def box_id(self, obj):
        return obj.box.id

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.box.user.full_name


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('is_active', 'valid_from', 'valid_until')
    search_fields = ('code',)
    ordering = ('-valid_from',)
    actions = [activate_promo_codes, deactivate_promo_codes]


@admin.register(PromoUsage)
class PromoUsageAdmin(admin.ModelAdmin):
    list_display = ('promo_code', 'user_name', 'used_at')
    list_filter = ('used_at',)
    search_fields = ('promo__code', 'user__full_name')
    ordering = ('-used_at',)

    @admin.display(description="Промокод")
    def promo_code(self, obj):
        return obj.promo.code

    @admin.display(description="Клиент")
    def user_name(self, obj):
        return obj.user.full_name


@admin.register(BoxSize)
class BoxSizeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'volume_m3', 'price_per_month')
    search_fields = ('code', 'name')
    ordering = ('code',)


@admin.register(BoxAvailability)
class BoxAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'size_code', 'total_boxes', 'occupied_boxes', 'available_boxes')
    list_filter = ('location', 'size')
    ordering = ('location', 'size')

    @admin.display(description="Локация")
    def location_name(self, obj):
        return obj.location.name

    @admin.display(description="Размер")
    def size_code(self, obj):
        return obj.size.code

    @admin.display(description="Доступно")
    def available_boxes(self, obj):
        return obj.available_boxes
    
admin.site.register(Role)