from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .forms import ContactForm
from .models import Package, Testimonial, CatalogueCategory, City


def home(request):
    context = {
        'packages': Package.objects.prefetch_related('features').all(),
        'testimonials': Testimonial.objects.filter(is_published=True),
        'sports_categories': CatalogueCategory.objects.filter(group='sports').prefetch_related('items'),
        'wellness_categories': CatalogueCategory.objects.filter(group='wellness'),
        'cities': City.objects.all(),
    }
    return render(request, 'marketing/home.html', context)


def about(request):
    # Placeholder page — swap in real content once provided.
    return render(request, 'marketing/about.html')


def blog(request):
    # "Coming Soon" placeholder.
    return render(request, 'marketing/blog.html')


def contact(request):
    initial = {}
    # Allows links like /contact/?interest=custom to pre-check a box
    # (handy for "Partner With Us" / "Sponsor a League" footer links later).
    preset_interest = request.GET.get('interest')
    interest_field_map = {
        'calendar': 'interested_annual_calendar',
        'tournaments': 'interested_tournaments',
        'wellness': 'interested_wellness',
        'custom': 'interested_custom',
    }
    if preset_interest in interest_field_map:
        initial[interest_field_map[preset_interest]] = True

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()

            # Email notification to the team inbox. If SMTP isn't configured
            # yet, this just prints to the console (see settings.py) instead
            # of failing — so the form still "works" during development.
            try:
                send_mail(
                    subject=f"New Proposal Request — {submission.company_name}",
                    message=(
                        f"Company: {submission.company_name}\n"
                        f"Contact: {submission.contact_person}\n"
                        f"Email: {submission.work_email}\n"
                        f"Phone: {submission.phone or '—'}\n"
                        f"Employee count: {submission.get_employee_count_display() or '—'}\n"
                        f"Interested in: {', '.join(submission.interests_list) or '—'}\n\n"
                        f"Message:\n{submission.message or '—'}\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_NOTIFICATION_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(request, "Thanks! We've received your details and will be in touch within one business day.")
            return redirect('contact')
    else:
        form = ContactForm(initial=initial)

    return render(request, 'marketing/contact.html', {'form': form})
