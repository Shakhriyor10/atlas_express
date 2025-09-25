import requests
from django.shortcuts import render, redirect
from django.views.generic import ListView
from frontend.models import Rate, RateCategory, Address, Country, BroadcastMessage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
from rest_framework import generics
from .models import BroadcastMessage
from .serializers import BroadcastMessageSerializer

class HomeRateListView(ListView):
    model = Rate
    template_name = 'index-2.html'
    context_object_name = 'rates'

    def get_queryset(self):
        return (
            Rate.objects
                .filter(status=True)
                .order_by('-id')[:3]
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = (
            Address.objects
            .select_related('city__country')  # переходим через city к country
            .filter(city__country__status=True)  # фильтрация по стране
            .order_by('-id')[:6]
        )
        context['countries'] = Country.objects.all()
        return context


class ContactListView(ListView):
    model = Address
    template_name = 'contacts.html'
    context_object_name = 'contacts'
    paginate_by = 10

    def get_queryset(self):
        qs = Address.objects.select_related('city__country') \
            .filter(city__country__status=True) \
            .order_by('-id')

        country_id = self.request.GET.get('country')
        if country_id:
            qs = qs.filter(city__country_id=country_id)

        city_id = self.request.GET.get('city')
        if city_id:
            qs = qs.filter(city_id=city_id)

        return qs


class TariffsByCategoryView(ListView):
    model = RateCategory
    template_name = 'tarrifs.html'
    context_object_name = 'categories'
    paginate_by = 12

    def get_queryset(self):
        qs = RateCategory.objects.filter(status=True).prefetch_related('rates')
        pk = self.kwargs.get('pk')
        if pk:
            qs = qs.filter(pk=pk)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_cats = []
        for cat in context['categories']:
            rates = list(cat.rates.filter(status=True).order_by('rate_title'))
            hot = next((r for r in rates if r.is_hot), None)
            if hot:
                rates.remove(hot)
                idx = 1 if rates else 0
                rates.insert(idx, hot)
            cat.rates_ordered = rates
            new_cats.append(cat)
        context['categories'] = new_cats
        return context

def track_package(request):
    if request.method == 'POST':
        trackid = request.POST.get('trackid')
        try:
            url = f"http://app.fgf.ai/trackings/box?country=&identityNumber=&number={trackid}"
            resp = requests.get(url, headers={"Accept": "application/json"})
            resp.raise_for_status()
            data = resp.json()
            return JsonResponse({
                'id': data.get('id'),
                'status': data.get('status'),
                'estimatedArrival': data.get('estimatedArrival'),
                'updatedAt': data.get('updatedAt'),
            })
        except Exception as e:
            print("Track error:", e)
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'index-2.html')



@require_http_methods(["GET", "POST"])
def tracking_details_view(request, trackid=None):
    if request.method == "POST":
        trackid = request.POST.get("trackid") or trackid
    else:
        trackid = trackid or request.GET.get("trackid")

    data, error = None, None
    if trackid:
        try:
            url = f"http://app.fgf.ai/trackings/box?country=&identityNumber=&number={trackid}"
            resp = requests.get(url, headers={"Accept": "application/json"})
            resp.raise_for_status()
            data = resp.json()
            data["updatedDateOnly"], data["updatedDateOnlyTime"] = data["updatedAt"].split(" ")
            if data.get("estimatedArrival"):
                try:
                    est_date = datetime.strptime(data["estimatedArrival"], "%d.%m.%Y")
                    data[
                        "arrival_range"] = f"{est_date.strftime('%d.%m.%Y')} - {(est_date + timedelta(days=5)).strftime('%d.%m.%Y')}"
                except Exception:
                    data["arrival_range"] = data["estimatedArrival"]
        except Exception as e:
            error = str(e)

    # список шагов + их "человеческие" названия
    steps = [
        ("location", "Местоположение"),
        ("in_warehouse", "На складе"),
        ("packed", "Упакован"),
        ("shipped", "Отправлен"),
        ("in_customs", "На таможне"),
        ("arrive_warehouse", "Прибыл на склад"),
        ("accept_location", "Принято в местоположение"),
        ("delivered", "Доставлено"),
    ]

    # индекс текущего шага
    current_index = -1
    if data and data.get("status"):
        codes = [s[0] for s in steps]
        if data["status"] in codes:
            current_index = codes.index(data["status"])

    return render(
        request,
        "id_details.html",
        {
            "data": data,
            "error": error,
            "trackid": trackid,
            "steps": steps,
            "current_index": current_index,  # 🔑 передаём в шаблон
        },
    )



@login_required(login_url='/login/')
def send_message_view(request):
    if request.method == "POST":
        description = request.POST.get("description")
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")

        # сохраняем сообщение
        BroadcastMessage.objects.create(
            description=description,
            image1=image1,
            image2=image2,
            image3=image3
        )

        return redirect("send_message")

    messages = BroadcastMessage.objects.order_by("-created_at")[:5]
    return render(request, "send_message.html", {"messages": messages})

# список всех сообщений
class BroadcastMessageListView(generics.ListAPIView):
    queryset = BroadcastMessage.objects.all().order_by("-created_at")
    serializer_class = BroadcastMessageSerializer

# последнее сообщение
class BroadcastMessageLatestView(generics.RetrieveAPIView):
    serializer_class = BroadcastMessageSerializer

    def get_object(self):
        return BroadcastMessage.objects.latest("created_at")
