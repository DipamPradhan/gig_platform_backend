from django.contrib import admin
from .models import (
	ServiceCategory,
	ServiceRequest,
	ServiceRequestBroadcast,
	ServiceRequestEvent,
	ServiceRouteSnapshot,
)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
	list_display = ("id", "name", "slug", "is_active", "created_at")
	search_fields = ("name", "slug")
	list_filter = ("is_active",)
	readonly_fields = ("id",)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
	list_display = (
		"id",
		"requester",
		"category",
		"status",
		"assigned_worker",
		"created_at",
	)
	list_filter = ("status", "category")
	search_fields = ("title", "requester__email")


@admin.register(ServiceRequestBroadcast)
class ServiceRequestBroadcastAdmin(admin.ModelAdmin):
	list_display = ("id", "request", "worker", "status", "ranking_score", "created_at")
	list_filter = ("status",)
	search_fields = ("request__title", "worker__worker__email")


@admin.register(ServiceRequestEvent)
class ServiceRequestEventAdmin(admin.ModelAdmin):
	list_display = ("id", "request", "event_type", "actor", "created_at")
	list_filter = ("event_type",)
	search_fields = ("request__title", "actor__email")


@admin.register(ServiceRouteSnapshot)
class ServiceRouteSnapshotAdmin(admin.ModelAdmin):
	list_display = ("id", "request", "estimated_distance_km", "estimated_duration_minutes")
