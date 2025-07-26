from django.db import models


class Client(models.Model):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    telegram_id = models.BigIntegerField(unique=True)
    consent_given = models.BooleanField(default=False)
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
    code = models.CharField(max_length=10, unique=True)  # 'S', 'M', 'L', etc.
    name = models.CharField(max_length=50)               # 'Small', 'Medium', etc.
    volume_m3 = models.DecimalField(max_digits=5, decimal_places=2)
    price_per_month = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.code}) — {self.volume_m3} м³"


class Box(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(BoxSize, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    end_date = models.DateField()
    extended_until = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Box {self.id} ({self.size.code}) for {self.client.full_name}"


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    address = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.CharField(max_length=50, blank=True)
    comment = models.TextField(blank=True)
    estimated_volume = models.CharField(max_length=100, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pickup for {self.client.full_name} on {self.preferred_date}"


class Notification(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE, null=True, blank=True)
    notification_type = models.CharField(max_length=100)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.client.full_name} ({self.notification_type})"


class OrderSource(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    utm_source = models.CharField(max_length=255, help_text="Источник, например: google_ads, telegram_bot")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utm_source} for {self.client.full_name}"


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
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    used_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} used {self.promo.code}"