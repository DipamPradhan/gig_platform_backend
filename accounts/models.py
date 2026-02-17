import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class CustomUser(AbstractUser):
    class Choice(models.TextChoices):
        USER = "User"
        WORKER = "Worker"
        ADMIN = "Admin"

    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$", message="Phone: '+999999999'. Up to 15 digits."
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
    )
    user_type = models.CharField(
        max_length=10,
        choices=Choice.choices,
        default=Choice.USER,
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        null=True,
        blank=True,
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Designates whether the user's email and phone number have been verified.",
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "phone_number"]

    class Meta:
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    current_latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    current_longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    current_address = models.TextField(blank=True, null=True)

    preferred_radius_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=5.00,
        validators=[MinValueValidator(0.2), MaxValueValidator(20.00)],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name()} "


class SavedLocation(models.Model):
    class LocationType(models.TextChoices):
        HOME = "Home"
        WORK = "Work"
        OTHER = "Other"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="saved_locations",
    )
    label = models.CharField(max_length=50)
    location_type = models.CharField(
        max_length=10,
        choices=LocationType.choices,
        default=LocationType.HOME,
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.TextField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["user_profile", "label"]]

    def __str__(self):
        return f"{self.label} ({self.user_profile.user.get_full_name()})"


class WorkerProfile(models.Model):
    class VERIFICATION_STATUS(models.TextChoices):
        PENDING = "Pending"
        VERIFIED = "Verified"
        REJECTED = "Rejected"

    class AVAILABILITY_STATUS(models.TextChoices):
        ACTIVE = "Active"
        INACTIVE = "Inactive"
        BUSY = "Busy"

    worker = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="worker_profile",
    )
    verification_status = models.CharField(
        max_length=10,
        choices=VERIFICATION_STATUS.choices,
        default=VERIFICATION_STATUS.PENDING,
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_workers",
    )
    rejection_reason = models.TextField(blank=True, null=True)
    availability_status = models.CharField(
        max_length=10,
        choices=AVAILABILITY_STATUS.choices,
        default=AVAILABILITY_STATUS.INACTIVE,
    )

    service_category = models.CharField(max_length=100)
    skills = models.TextField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    hourly_rate = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    service_latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    service_longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    service_radius_km = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    total_jobs_completed = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.worker.get_full_name()} - {self.service_category}"


class WorkerDocument(models.Model):
    class DocumentType(models.TextChoices):
        CITIZENSHIP = "Citizenship"
        DRIVER_LICENSE = "Driver's License"
        NIN_CARD = "NIN Card"

    class VERIFICATION_STATUS(models.TextChoices):
        PENDING = "Pending"
        VERIFIED = "Verified"
        REJECTED = "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    worker_profile = models.ForeignKey(
        WorkerProfile, on_delete=models.CASCADE, related_name="documents"
    )

    document_type = models.CharField(max_length=20, choices=DocumentType.choices)
    document_number = models.CharField(max_length=100)
    document_file = models.FileField(upload_to="worker_documents/")

    verification_status = models.CharField(
        max_length=20,
        choices=VERIFICATION_STATUS.choices,
        default=VERIFICATION_STATUS.PENDING,
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_documents",
    )
    rejection_reason = models.TextField(blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["worker_profile", "document_type", "document_number"]]

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.worker_profile.worker.get_full_name()}"


class AdminProfile(models.Model):
    admin = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="admin_profile",
    )
    can_verify_workers = models.BooleanField(default=False)
    can_manage_users = models.BooleanField(default=False)
    total_verifications = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Admin Profile of {self.admin.get_full_name()}"
