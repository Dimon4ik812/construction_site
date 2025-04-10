import json
import os

from django.shortcuts import redirect

from construction.models import Services

from django.views.generic import ListView

import requests
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

load_dotenv(override=True)

import logging

logger = logging.getLogger(__name__)

class ServicesListView(ListView):
    model = Services
    template_name = "construction/index.html"
    context_object_name = "services"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@csrf_exempt
def send_order_to_telegram(request):
    if request.method == 'POST':
        try:
            # Логируем полученные данные
            logger.info(f"Получен POST-запрос: {request.body}")

            # Парсим JSON-данные из тела запроса
            data = json.loads(request.body)
            service_name = data.get('service_name')
            service_price = data.get('service_price')
            customer_name = data.get('customer_name')
            customer_phone = data.get('customer_phone')

            # Проверяем, что все обязательные поля заполнены
            if not all([service_name, service_price, customer_name, customer_phone]):
                return JsonResponse({'status': 'error', 'message': 'Не все поля заполнены'})

            # Формируем текст сообщения
            message = (
                f"Новый заказ:\n"
                f"Услуга: {service_name}\n"
                f"Стоимость: {service_price}\n"
                f"Имя клиента: {customer_name}\n"
                f"Телефон: {customer_phone}"
            )

            # Отправляем сообщение в Telegram
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
            }
            response = requests.post(url, json=payload)

            # Логируем ответ от Telegram
            logger.info(f"Ответ от Telegram: {response.text}")

            # Проверяем успешность отправки
            if response.status_code == 200 and response.json().get('ok'):
                return JsonResponse({'status': 'success', 'message': 'Заказ отправлен в Telegram'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Ошибка при отправке в Telegram'})

        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@csrf_exempt
def send_order_to_telegram_2(request):
    if request.method == 'POST':
        try:
            # Получаем данные из POST-запроса
            customer_name = request.POST.get('customer_name')
            customer_email = request.POST.get('customer_email')
            customer_phone = request.POST.get('customer_phone')
            service_name = request.POST.get('service_name')
            message_text = request.POST.get('message')

            # Проверяем, что все обязательные поля заполнены
            if not all([customer_name, customer_email, customer_phone, service_name]):
                return HttpResponse('Не все обязательные поля заполнены', status=400)

            # Формируем текст сообщения
            message = (
                f"Новая заявка:\n"
                f"Имя: {customer_name}\n"
                f"Email: {customer_email}\n"
                f"Телефон: {customer_phone}\n"
                f"Услуга: {service_name}\n"
                f"Сообщение: {message_text}"
            )

            # Отправляем сообщение в Telegram
            url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
            }
            response = requests.post(url, json=payload)

            # Логируем ответ от Telegram
            logger.info(f"Ответ от Telegram: {response.text}")

            # Проверяем успешность отправки
            if response.status_code == 200 and response.json().get('ok'):
                # Добавляем сообщение об успехе
                messages.success(request, 'Заявка успешно отправлена!')
                return redirect('/home/')
            else:
                return HttpResponse('Ошибка при отправке в Telegram', status=500)

        except Exception as e:
            logger.error(f"Произошла ошибка: {str(e)}")
            return HttpResponse(f'Ошибка: {str(e)}', status=500)

    return HttpResponse('Метод не поддерживается', status=405)