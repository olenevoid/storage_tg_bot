from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class User(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True)
    consent_given = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.phone})"


class StorageLocation(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    has_delivery = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class BoxSize(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    volume_m3 = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.code}) — {self.volume_m3} м³\xb3"


class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(BoxSize, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    extended_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Box {self.id} ({self.size.code}) for {self.user.full_name}"


class BoxAvailability(models.Model):
    location = models.ForeignKey(StorageLocation, on_delete=models.CASCADE)
    size = models.ForeignKey(BoxSize, on_delete=models.CASCADE)
    total_boxes = models.PositiveIntegerField(default=0)
    occupied_boxes = models.PositiveIntegerField(default=0)

    @property
    def available_boxes(self):
        return self.total_boxes - self.occupied_boxes

    def __str__(self):
        return f"{self.size.code} at {self.location.name}: {self.available_boxes} available"


class StoredItem(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} x{self.quantity} (Box #{self.box.id})"


class PickupRequest(models.Model):
    TYPE_CHOICES = [
        ('deliver', 'Доставка на склад'),
        ('withdraw', 'Вывоз со склада'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Выполнена'),
        ('cancelled', 'Отменена'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pickup_requests')
    executor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_pickup_requests',
        limit_choices_to={'role__name__in': ['courier', 'executor', 'исполнитель']},  
        help_text="Исполнитель заявки (курьер)"
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='deliver')
    address = models.TextField(help_text="Адрес для забора или доставки вещей")
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    estimated_volume = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.get_type_display()} для {self.user.full_name} на {self.preferred_date} (Статус: {self.get_status_display()})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.user.full_name} ({self.notification_type})"


class OrderSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    utm_source = models.CharField(max_length=255, help_text="Источник, например: google_ads, telegram_bot")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utm_source} for {self.user.full_name}"


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Скидка в процентах, например: 20")
    valid_from = models.DateField()
    valid_until = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    def is_valid(self, date=None):
        from datetime import date as dt
        date = date or dt.today()
        return self.is_active and self.valid_from <= date <= self.valid_until


class PromoUsage(models.Model):
    promo = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.full_name} used {self.promo.code}"