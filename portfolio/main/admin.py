from django.contrib import admin
from .models import (
    Category,
    Profile,
    Resume,
    Education,
    Experience,
    Skill,
    Project,
    Certificate,
    Service,
    SocialLink,
    ContactMessage,
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "title", "email", "location", "visitor_count")
    readonly_fields = ("visitor_count",)
    fieldsets = (
        ("Personal Information", {
            "fields": ("name", "title", "bio", "summary", "profile_photo", "about_photo")
        }),
        ("Contact & Location", {
            "fields": ("email", "phone", "location")
        }),
        ("Integrations & Metrics", {
            "fields": ("github_username", "visitor_count", "quick_facts")
        }),
        ("SEO Meta Settings", {
            "fields": ("meta_title", "meta_description", "meta_keywords"),
            "classes": ("collapse",),
        }),
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "uploaded_at")
    list_filter = ("is_active",)
    search_fields = ("title",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_date", "end_date", "is_current")
    list_filter = ("is_current", "institution")
    search_fields = ("degree", "institution", "description")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("position", "company", "start_date", "end_date", "is_current")
    list_filter = ("is_current", "company")
    search_fields = ("position", "company", "description")
    filter_horizontal = ("skills_used",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "created_at")
    list_filter = ("category", "featured")
    search_fields = ("title", "tech_stack", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("order", "-created_at")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("title", "issuer", "date_issued")
    list_filter = ("issuer",)
    search_fields = ("title", "issuer")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title", "description")
    ordering = ("order",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform_name", "url")
    search_fields = ("platform_name",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
    actions = ["mark_as_read", "mark_as_unread"]
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as unread"
