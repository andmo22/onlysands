from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Beach, BeachImage, UserProfile


class BeachImageInline(admin.TabularInline):
    model = BeachImage
    extra = 1
    fields = ["image"]


@admin.register(Beach)
class BeachAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "suburb", "rating")
    search_fields = ("name", "suburb", "review")
    list_filter = ("location", "rating", "visited", "return_visit")
    ordering = ("name",)
    inlines = [BeachImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        for field_name in [
            "beach_type",
            "tags",
            "vibe",
            "related_walks",
            "other_names",
        ]:
            if obj:
                form.base_fields[field_name].initial = (
                    ", ".join(obj.__dict__[field_name])
                    if obj.__dict__[field_name]
                    else ""
                )
        return form


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"
    fk_name = "user"
    extra = 0
    fields = (
        "email_confirmed",
        "last_confirmation_email_sent_at",
        "confirmation_token",
    )


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if obj:
            return [inline(self.model, self.admin_site) for inline in self.inlines]
        return []


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
