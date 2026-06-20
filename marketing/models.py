"""
Models for the Playonix marketing site.

Everything here shows up in /admin so non-technical edits (changing a
price, adding a testimonial, adding a sport) never need a code change
or a Cursor session.
"""

from django.db import models


# ──────────────────────────────────────────────────────────────────
# PACKAGES (Spark / League Pro / Enterprise)
# ──────────────────────────────────────────────────────────────────
class Package(models.Model):
    """One pricing/plan card on the Packages section."""

    name = models.CharField(max_length=80, help_text="e.g. Spark, League Pro, Enterprise")
    badge_label = models.CharField(
        max_length=40,
        help_text="Small label above the title, e.g. 'Starter', 'Most Popular', 'Enterprise'"
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Featured plan gets the red highlighted card style."
    )
    description = models.TextField(help_text="1-2 sentence description shown under the title.")
    cta_label = models.CharField(max_length=40, default="Get a Quote")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers show first (left to right).")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PackageFeature(models.Model):
    """A single bullet/checkmark line inside a Package card."""
    package = models.ForeignKey(Package, related_name='features', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.package.name} — {self.text}"


# ──────────────────────────────────────────────────────────────────
# TESTIMONIALS ("Voices")
# ──────────────────────────────────────────────────────────────────
class Testimonial(models.Model):
    quote = models.TextField()
    author_name = models.CharField(max_length=100)
    author_role = models.CharField(max_length=150, help_text="e.g. 'HR Manager · IT Company, Hyderabad'")
    rating = models.PositiveSmallIntegerField(default=5, help_text="Out of 5 stars")
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.author_name} — {self.quote[:40]}"

    @property
    def author_initials(self):
        parts = self.author_name.split()
        return ''.join(p[0].upper() for p in parts[:2])


# ──────────────────────────────────────────────────────────────────
# CATALOGUE — Sports & Games, and Wellness
# ──────────────────────────────────────────────────────────────────
class CatalogueCategory(models.Model):
    """
    A category card in the Catalogue section, e.g. 'Sports Experiences', 'Sports Psychology' (wellness side).
    """
    GROUP_CHOICES = [
        ('sports', 'Sports & Games'),
        ('wellness', 'Wellness & Team Development'),
    ]

    group = models.CharField(max_length=20, choices=GROUP_CHOICES, default='sports')
    name = models.CharField(max_length=100, help_text="e.g. 'Sports Experiences', 'Stress Management'")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['group', 'order']
        verbose_name_plural = "Catalogue categories"

    def __str__(self):
        return f"[{self.get_group_display()}] {self.name}"


class CatalogueItem(models.Model):
    """A single item under a category, e.g. 'Cricket', 'Kho Kho'."""
    category = models.ForeignKey(CatalogueCategory, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.category.name} — {self.name}"


# ──────────────────────────────────────────────────────────────────
# CITIES (where Playonix currently/upcoming operates)
# ──────────────────────────────────────────────────────────────────
class City(models.Model):
    name = models.CharField(max_length=80)
    is_live = models.BooleanField(default=False, help_text="Checked = currently operating here.")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name_plural = "Cities"

    def __str__(self):
        return f"{self.name} ({'Live' if self.is_live else 'Upcoming'})"


# ──────────────────────────────────────────────────────────────────
# CONTACT FORM SUBMISSIONS ("Get a Proposal")
# ──────────────────────────────────────────────────────────────────
class ContactSubmission(models.Model):
    EMPLOYEE_COUNT_CHOICES = [
        ('1-50', '1–50'),
        ('51-150', '51–150'),
        ('151-500', '151–500'),
        ('500+', '500+'),
    ]

    company_name = models.CharField(max_length=150)
    contact_person = models.CharField(max_length=120)
    work_email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    employee_count = models.CharField(max_length=20, choices=EMPLOYEE_COUNT_CHOICES, blank=True)

    interested_annual_calendar = models.BooleanField(default=False, verbose_name="Annual Sports Calendar")
    interested_tournaments = models.BooleanField(default=False, verbose_name="Tournaments / Leagues")
    interested_wellness = models.BooleanField(default=False, verbose_name="Wellness Sessions")
    interested_custom = models.BooleanField(default=False, verbose_name="Custom Program")

    message = models.TextField(blank=True, verbose_name="Anything we should know?")

    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False, help_text="Mark once you've followed up.")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} — {self.contact_person} ({self.created_at:%d %b %Y})"

    @property
    def interests_list(self):
        labels = []
        if self.interested_annual_calendar:
            labels.append("Annual Sports Calendar")
        if self.interested_tournaments:
            labels.append("Tournaments / Leagues")
        if self.interested_wellness:
            labels.append("Wellness Sessions")
        if self.interested_custom:
            labels.append("Custom Program")
        return labels
