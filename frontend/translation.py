from modeltranslation.translator import register, TranslationOptions
from .models import Country, City, Address, Rate, RateCategory


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(RateCategory)
class RateCategoryTranslationOptions(TranslationOptions):
    fields = ('sender_recipient',)


@register(Rate)
class RateTranslationOptions(TranslationOptions):
    fields = ('rate_title',)