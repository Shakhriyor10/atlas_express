from django.contrib import admin

from frontend.models import Rate, RateCategory, Country, Address, City, BroadcastMessage


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'get_country', 'phone')
    list_filter = ('city__country',)

    def get_country(self, obj):
        return obj.city.country if obj.city else None
    get_country.short_description = 'Страна'



@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display   = ('rate_title', 'country', 'is_hot', 'status')
    list_filter    = ('country', 'is_hot', 'status')
    search_fields  = ('rate_title', 'country__sender_recipient')

@admin.register(RateCategory)
class RateCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "short_description", "created_at")
    search_fields = ("description",)
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)

    # Покажем первые 50 символов текста вместо огромного описания
    def short_description(self, obj):
        return obj.description[:50] + ("..." if len(obj.description) > 50 else "")
    short_description.short_description = "Описание"

