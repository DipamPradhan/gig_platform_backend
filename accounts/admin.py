from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    UserProfile,
    WorkerProfile,
    WorkerDocument,
    SavedLocation,
    AdminProfile,
)


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        "id",
        "email",
        "username",
        "user_type",
        "is_staff",
        "is_active",
    )
    list_filter = ("user_type", "is_staff", "is_active")

    ordering = ("email",)
    search_fields = ("email", "username", "phone_number")

    fieldsets = UserAdmin.fieldsets + (
        (
            "Extra Fields",
            {"fields": ("phone_number", "user_type", "profile_picture")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "preferred_radius_km", "updated_at")
    search_fields = ("user__email", "user__username")


admin.site.register(UserProfile, UserProfileAdmin)


class WorkerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "worker",
        "service_category",
        "verification_status",
        "availability_status",
        "updated_at",
    )
    list_filter = ("verification_status", "availability_status", "service_category")
    search_fields = ("worker__email", "worker__username", "skills")


admin.site.register(WorkerProfile, WorkerProfileAdmin)


class WorkerDocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "worker_profile",
        "worker_user_id",
        "document_type",
        "document_number",
        "verification_status",
        "uploaded_at",
    )
    list_filter = ("document_type", "verification_status")
    search_fields = ("worker_profile__worker__email", "document_number")

    @admin.display(description="Worker User ID")
    def worker_user_id(self, obj):
        return obj.worker_profile.worker_id


admin.site.register(WorkerDocument, WorkerDocumentAdmin)


class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ("id", "user_profile", "label", "location_type", "is_default")
    list_filter = ("location_type", "is_default")


admin.site.register(SavedLocation, SavedLocationAdmin)


class AdminProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "admin",
        "can_verify_workers",
        "can_manage_users",
        "total_verifications",
    )


admin.site.register(AdminProfile, AdminProfileAdmin)
