# iLearn — Веб-приложение для онлайн-обучения

## Описание:

**iLearn** — это веб-приложение для онлайн-обучения, разработанное с использованием Django и Celery. Оно предоставляет
функциональность для управления курсами, подписками и отправки уведомлений пользователям.

## Установка:

1. Клонируйте репозиторий:

```
clone -b develop https://github.com/Rapunzel-Chan/ilearn.git
```

2. Установите зависимости:

```
pip install -r requirements.txt
```

## Использование:

1. Переключитесь на проект:

```
cd ilearn
```

2. Создайте виртуальное окружение:

```
python -m venv venv
```

3. Активируйте виртуальное окружение:

- Windows:

```
.\venv\Scripts\activate
```

- Linux/macOS:

```
source venv/bin/activate
```

4. Примените миграции:

```
python manage.py migrate
```

5. Создайте суперпользователя и группу менеджеров:

```
python manage.py csu
python manage.py create_groups
```

6. Запустите сервер:

```
python manage.py runserver
```

7. Запустите Celery:

```
celery -A config beat --loglevel=info
celery -A config worker --loglevel=info
```

## Тестирование:

Для запуска тестов напишите:

```
python manage.py test
```

## Администирирование:

Перейдите по адресу http://localhost:8000/admin и войдите с учётной записью суперпользователя.

- **Управление периодическими задачами**

В разделе Periodic Tasks Вы можете:

-Создавать новые периодические задачи.

-Настроить расписание задач с использованием интервалов, cron-выражений или точных временных меток.

- **Управление задачами**

В разделе Tasks Вы можете:

-Просматривать список всех задач.

-Проверять статус выполнения задач.

## Сокрытие чувствительных данных

Список переменных окружений находится в .env.example. Заполните данные для правильной работы приложения.

## Запуск и проверка сервисов приложения в Docker-контейнере


1. Установите Docker и Docker Compose.
2. Убедитесь, что в корне проекта есть: `Dockerfile`, `docker-compose.yml`, `.env.example`
3. Создайте .env и заполните необходимые значения
4. Запустите всю систему:
```
docker compose up -d --build
```
5. Поднимите базовые сервисы и проверьте статус и их "здоровье":
```
docker-compose up -d db redis
docker-compose ps
```

6. Выполните миграции для полноценной работы beat:
```
docker-compose run --rm backend python manage.py migrate
```

7. Поднимите все сервисы:
```
docker-compose up -d backend celery beat
```

8. Проверьте логи по сервисам:
```
docker-compose -f logs backend
docker-compose -f logs celery
docker-compose -f logs beat
```

## Deploy и проверка сервисов приложения на Yandex.Cloud:

1. Подготовьте сервер (Yandex Cloud / Ubuntu 22.04):
```
ssh ubuntu@SERVER_IP
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv docker.io docker-compose-plugin git ufw
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
sudo ufw status
```

2. Настройте SSH-ключи для GitHub Actions:

Локально:
```
ssh-keygen -t ed25519 -C "deploy@ilearn" -f ~/.ssh/ilearn_deploy
```
На сервере:
```
ssh-copy-id -i ~/.ssh/ilearn_deploy.pub ubuntu@SERVER_IP
ssh -i ~/.ssh/ilearn_deploy ubuntu@SERVER_IP
```

3. Подготовьте переменные окружения:
```
cp .env.example .env
base64 --wrap=0 .env > env.b64 **либо** certutil -encode .env env.b64
Get-Content env.b64 | Select-Object -Skip 1 | Select-Object -SkipLast 1 | Out-File -Encoding ascii env_clean.b64
```

4. Зайдите в Repo → Settings → Secrets → Actions и добавьте:

| Secret             | Значение                             |
|--------------------|--------------------------------------|
 ENV_FILE	          | содержимое env.b64 или env_clean.b64 |
| SERVER_IP          | 	IP сервера                          |
| SERVER_USER        | 	ubuntu или другой пользователь      |
| SERVER_SSH_KEY     | 	приватный ключ ilearn_deploy        |
| DOCKERHUB_USERNAME | 	твой Docker Hub username            |
| DOCKERHUB_TOKEN    |Access Token из Docker Hub |

5. Подготовьте Systemd Unit для Docker Compose и вставьте данные из deploy/systemd/ilearn.service:
```
sudo nano /etc/systemd/system/ilearn.service
sudo systemctl daemon-reload
sudo systemctl enable ilearn
sudo systemctl start ilearn
sudo systemctl status ilearn
```

6. Подготовьте Nginx и вставьте данные из deploy/nginx/default.conf:
```
sudo nano /etc/nginx/sites-available/ilearn.conf
sudo ln -s /etc/nginx/sites-available/ilearn.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
curl http://localhost
```

7. Запустите GitHub Actions Workflow (.github/workflows/deploy.yml):
```
script: |
  set -eux
  cd /home/${{ secrets.SERVER_USER }}/I-learn
  printf '%s' "${{ secrets.ENV_FILE }}" | base64 -d > .env
  docker compose --env-file .env -f docker-compose.prod.yml pull
  docker compose --env-file .env -f docker-compose.prod.yml up -d --remove-orphans
  docker compose --env-file .env -f docker-compose.prod.yml exec -T backend python manage.py migrate --noinput
  docker compose --env-file .env -f docker-compose.prod.yml exec -T backend python manage.py collectstatic --noinput
```

8. Проверьте работу всего deploy:

На сервере:
```
docker ps
```
В браузере:
```
http://YOUR_SERVER_IP
```

## Создатель

В случае возникновения вопросов, нахождения багов или предложений по улучшению кода, можно обратиться к разработчику
по e-mail: rapuncel.chan24@gmail.com.
