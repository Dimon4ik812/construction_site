// Обработка burger menu
document.addEventListener('DOMContentLoaded', function () {
  const navbarToggle = document.querySelector('.navbar-toggle');
  const raisingMenu = document.querySelector('.raising-menu');

  navbarToggle.addEventListener('click', function () {
    raisingMenu.classList.toggle('active');
  });
});

// Функция для получения CSRF-токена
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Обработка открытия модального окна
document.addEventListener('DOMContentLoaded', function () {
  var modal = document.getElementById('staticBackdrop');

  modal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget; // Кнопка, которая открыла модальное окно
    var serviceName = button.getAttribute('data-service-name'); // Название услуги
    var servicePrice = button.getAttribute('data-service-price'); // Цена услуги

    // Заполняем поля формы
    document.getElementById('serviceName').value = serviceName;
    document.getElementById('servicePrice').value = servicePrice + ' руб/час';
  });

  // Обработка отправки заказа
  document.getElementById('submitOrder').addEventListener('click', function () {
    var customerName = document.getElementById('customerName').value;
    var customerPhone = document.getElementById('customerPhone').value;


    if (!customerName || !customerPhone) {
      alert('Пожалуйста, заполните все поля.');
      return;
    }

    // Собираем данные для отправки
    var serviceName = document.getElementById('serviceName').value;
    var servicePrice = document.getElementById('servicePrice').value;

    // Отправляем данные на сервер через AJAX
    fetch('/send-order/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken') // Если используется CSRF-защита
      },
      body: JSON.stringify({
        service_name: serviceName,
        service_price: servicePrice,
        customer_name: customerName,
        customer_phone: customerPhone
      })
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          alert('Заказ успешно отправлен!');
          var modalInstance = bootstrap.Modal.getInstance(modal);
          modalInstance.hide(); // Закрываем модальное окно
          document.getElementById('orderForm').reset(); // Очищаем форму
          // Обновляем страницу
          window.location.reload();
        } else {
          alert('Ошибка: ' + data.message);
        }
      })
      .catch(error => {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при отправке заказа.');
      });
  });
});