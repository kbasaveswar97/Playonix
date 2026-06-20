"""
Seeds the database with the initial content locked in during planning:
Packages, Catalogue (Sports + Wellness), Cities, and starter Testimonials.

Run with: python manage.py seed_content

Safe to re-run — it clears and re-creates these records each time, so
don't run it after you've started editing real content in /admin
without backing up first.
"""

from django.core.management.base import BaseCommand
from marketing.models import (
    Package, PackageFeature,
    CatalogueCategory, CatalogueItem,
    City,
    Testimonial,
)


class Command(BaseCommand):
    help = "Seed initial Playonix content (packages, catalogue, cities, testimonials)"

    def handle(self, *args, **options):
        self.seed_packages()
        self.seed_catalogue()
        self.seed_cities()
        self.seed_testimonials()
        self.stdout.write(self.style.SUCCESS("✓ Seed data created."))

    def seed_packages(self):
        Package.objects.all().delete()

        spark = Package.objects.create(
            name="Spark",
            badge_label="Starter",
            is_featured=False,
            description="Perfect for teams of 50–150 employees wanting to pilot corporate sports with a single league season.",
            cta_label="Get a Quote",
            order=1,
        )
        for i, text in enumerate([
            "1 Sport · 1 Season (8 weeks)",
            "Up to 8 teams / 80 players",
            "Venue booking & equipment",
            "Scorecards & fixtures",
            "Closing ceremony & trophies",
        ]):
            PackageFeature.objects.create(package=spark, text=text, order=i)

        league_pro = Package.objects.create(
            name="League Pro",
            badge_label="Most Popular",
            is_featured=True,
            description="For mid-size companies (150–500 employees) wanting a full annual sports calendar across multiple sports.",
            cta_label="Book a Demo",
            order=2,
        )
        for i, text in enumerate([
            "3 Sports · Year-round seasons",
            "Unlimited teams & players",
            "Full ops — venues, refs, gear",
            "Live scoring & leaderboards",
            "Engagement reports for HR",
            "Brand sponsorship integration",
        ]):
            PackageFeature.objects.create(package=league_pro, text=text, order=i)

        enterprise = Package.objects.create(
            name="Enterprise",
            badge_label="Enterprise",
            is_featured=False,
            description="For large enterprises (500+ employees) needing multi-city, multi-sport programs with deep customization.",
            cta_label="Contact Us",
            order=3,
        )
        for i, text in enumerate([
            "All sports · All cities",
            "Dedicated account manager",
            "Custom branding & jersey kits",
            "Sports offsites included",
            "Executive dashboard & ROI data",
            "Priority support & renewals",
        ]):
            PackageFeature.objects.create(package=enterprise, text=text, order=i)

    def seed_catalogue(self):
        CatalogueCategory.objects.all().delete()

        sports_data = [
            ("Sports Experiences", ["Cricket", "Badminton", "Football", "Pickleball"]),
            ("Childhood Throwback Games", ["Seven Stones", "Kho Kho", "Tug of War", "Sack Race", "Lemon & Spoon"]),
            ("Social Connection Games", ["Treasure Hunt", "Human Bingo", "Pictionary", "Charades"]),
            ("Team Challenges", ["Obstacle Courses", "Problem Solving Challenges", "Leadership Games"]),
        ]
        for i, (cat_name, items) in enumerate(sports_data):
            cat = CatalogueCategory.objects.create(group='sports', name=cat_name, order=i)
            for j, item_name in enumerate(items):
                CatalogueItem.objects.create(category=cat, name=item_name, order=j)

        wellness_data = ["Sports Psychology", "Team Bonding", "Leadership Sports", "Stress Management"]
        for i, cat_name in enumerate(wellness_data):
            CatalogueCategory.objects.create(group='wellness', name=cat_name, order=i)

    def seed_cities(self):
        City.objects.all().delete()
        City.objects.create(name="Hyderabad", is_live=True, order=0)
        for i, name in enumerate(["Bengaluru", "Mumbai", "Delhi NCR", "Chennai", "Pune"], start=1):
            City.objects.create(name=name, is_live=False, order=i)

    def seed_testimonials(self):
        # NOTE: These are placeholders, clearly NOT real testimonials.
        # Replace with genuine client quotes via /admin once you have them.
        Testimonial.objects.all().delete()
        Testimonial.objects.create(
            quote="Placeholder — replace with a real client quote once your first league wraps up.",
            author_name="Pending",
            author_role="Awaiting first cohort feedback",
            rating=5,
            is_published=False,  # hidden by default until replaced with something real
            order=0,
        )
