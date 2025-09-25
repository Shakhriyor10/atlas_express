from django.template.loader import render_to_string
from django.middleware.csrf import get_token
from collections import defaultdict

def banner_section(request):
    token = get_token(request)
    html = render_to_string(
        'banner.html',
        { 'csrf_token': token },
    )
    return {
        'banner_section': html
    }

from .models import Country, RateCategory, City


def countries(request):
    countries_qs = Country.objects.filter(status=True)

    cities_by_country = defaultdict(list)
    for city in City.objects.select_related('country').filter(status=True):
        cities_by_country[city.country_id].append(city)

    return {
        'countries': countries_qs,
        'cities_by_country': cities_by_country,
        'selected_country': request.GET.get('country'),
        'selected_city': request.GET.get('city')
    }

def rate_categories(request):
    return {
        'rate_categories': RateCategory.objects.filter(status=True).order_by('sender_recipient')
    }