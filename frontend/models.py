from django.db import models
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Название страны')
    photo = models.ImageField(verbose_name='Фото страны',
                              upload_to='images/',
                              blank=True,
                              null=True)
    status = models.BooleanField(default=True,
                                 verbose_name='Статус')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

class City(models.Model):
    title = models.CharField(max_length=100,
                             verbose_name='Город')
    photo = models.ImageField(verbose_name='Фото',
                              upload_to='images/',
                              blank=True,
                              null=True)
    status = models.BooleanField(default=True,
                                 verbose_name='Статус')
    country = models.ForeignKey(Country,
                                verbose_name='Страна',
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='countries',)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Address(models.Model):
    photo = models.ImageField(verbose_name='image',
                              upload_to='image/',
                              blank=True,
                              null=True)
    title = models.CharField(max_length=100,
                             verbose_name='Название')
    city = models.ForeignKey(City,
                             verbose_name=_('Город'),
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True,
                             related_name='cities')

    phone = models.CharField(max_length=250,
                             verbose_name='Телефон номер')
    phone2 = models.CharField(max_length=250,
                              verbose_name='Доп телефон номер',
                              blank=True,
                              null=True)
    coordinates1 = models.CharField(max_length=250,
                                    verbose_name='Кординаты A',
                                    blank=True,
                                    null=True)
    coordinates2 = models.CharField(max_length=250,
                                    verbose_name='Кординаты B',
                                    blank=True,
                                    null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class RateCategory(models.Model):
    sender_recipient = models.CharField(max_length=250,
                                        verbose_name='Страна отправителя')
    recipient_country = models.CharField(max_length=250,
                                         verbose_name='Страна получателя',
                                         blank=True,
                                         null=True)
    status = models.BooleanField(default=True,
                                 verbose_name='Статус')

    def __str__(self):
        return self.sender_recipient

    class Meta:
        verbose_name = 'Страна отправителя и получателя'
        verbose_name_plural = 'Страна отправителя и получателя'


class Rate(models.Model):
    rate_title = models.CharField(max_length=100,
                                  verbose_name='Название тарифа')
    price = models.FloatField(verbose_name='Цена',
                              default=0)
    country = models.ForeignKey(RateCategory,
                                verbose_name='Страна отправителя и получателя',
                                on_delete=models.PROTECT,
                                related_name='rates')
    status = models.BooleanField(default=True,)
    delivery_within = models.CharField(max_length=100,
                                       verbose_name='Доставка в течение (дней)',
                                       )
    minimal_weight = models.FloatField(verbose_name='Минимальный вес',
                                       default=0,
                                       blank=True,
                                       null=True)
    is_hot = models.BooleanField(default=False,
                                 verbose_name='Горячий тариф (по центру, оранжевый)')

    def __str__(self):
        return self.rate_title

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

class BroadcastMessage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    image1 = models.FileField(upload_to='broadcasts/', blank=True, null=True)
    image2 = models.FileField(upload_to='broadcasts/', blank=True, null=True)
    image3 = models.FileField(upload_to='broadcasts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

