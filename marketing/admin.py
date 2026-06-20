from django.contrib import admin
from .models import (
    Package, PackageFeature,
    Testimonial,
    CatalogueCategory, CatalogueItem,
    City,
    ContactSubmission,
)


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'badge_label', 'is_featured', 'order')
    list_editable = ('order', 'is_featured')
    inlines = [PackageFeatureInline]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_role', 'rating', 'is_published', 'order')
    list_editable = ('is_published', 'order')
    list_filter = ('is_published',)


class CatalogueItemInline(admin.TabularInline):
    model = CatalogueItem
    extra = 1


@admin.register(CatalogueCategory)
class CatalogueCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'order')
    list_editable = ('order',)
    list_filter = ('group',)
    inlines = [CatalogueItemInline]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_live', 'order')
    list_editable = ('is_live', 'order')


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'contact_person', 'work_email', 'employee_count', 'created_at', 'is_handled')
    list_editable = ('is_handled',)
    list_filter = ('is_handled', 'employee_count', 'created_at')
    readonly_fields = (
        'company_name', 'contact_person', 'work_email', 'phone', 'employee_count',
        'interested_annual_calendar', 'interested_tournaments', 'interested_wellness',
        'interested_custom', 'message', 'created_at',
    )
    search_fields = ('company_name', 'contact_person', 'work_email')

    def has_add_permission(self, request):
        # Submissions only ever come in through the public form.
        return False
