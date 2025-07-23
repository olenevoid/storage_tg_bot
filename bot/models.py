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


class Box(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)  
    location = models.ForeignKey(StorageLocation, on_delete=models.SET_NULL, null=True)  
    size = models.CharField(
        max_length=10,
        choices=[('S', 'S'), ('M', 'M'), ('L', 'L')]  
    )
    description = models.TextField(blank=True)  
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)  
    end_date = models.DateField()  
    extended_until = models.DateField(blank=True, null=True)  

    def __str__(self):
        return f"Box {self.id} ({self.size}) for {self.client.full_name}"


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