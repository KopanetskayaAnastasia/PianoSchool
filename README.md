# PianoSchool
1. Необходимое ПО
Windows:
	Docker Desktop
	Скачать: https://www.docker.com/products/docker-desktop/

Linux:
	Docker Engine
	Docker Compose

2. Пошаговая инструкция по развертыванию
Шаг 1. Скопируйте проект и архив с флешки
Скопируйте папку проекта (PianoSchool/) с флешки на диск, например:
	Windows: C:\Projects\PianoSchool\
	Linux: /home/username/Projects/PianoSchool/

Шаг 2. Убедитесь, что Docker работает
Windows: 
	Запустите Docker Desktop 
Linux: 
	Проверьте:
	docker --version
	docker compose version

Шаг 3. Перейдите в папку проекта
Windows (PowerShell):
	cd C:\Projects\PianoSchool

Linux:
	cd /home/username/Projects/PianoSchool

Шаг 4. Восстановите volume с базой данных
4.1. Создайте volume с нужным именем
	docker volume create pianoschool_postgres_data

4.2. Восстановите данные из архива в volume
Windows (PowerShell):
	docker run --rm -v pianoschool_postgres_data:/volume -v "%cd%:/backup" busybox tar xzvf /backup/pianoschool_postgres_data.tar.gz -C /volume

Linux:
	docker run --rm -v pianoschool_postgres_data:/volume -v $(pwd):/backup busybox tar xzvf /backup/pianoschool_postgres_data.tar.gz -C /volume

Шаг 5. Соберите и запустите проект
docker compose up --build

Шаг 6. Откройте приложение в браузере
Перейдите на http://localhost:8080

3. Остановка приложения
Чтобы остановить приложение, нажмите Ctrl+C в терминале, где оно запущено,
или выполните:

docker compose down

4. Кратко: команды для развертывания

Linux:
	cd /путь/к/проекту
	docker volume create pianoschool_postgres_data
	docker run --rm -v pianoschool_postgres_data:/volume -v $(pwd):/backup busybox tar xzvf /backup/pianoschool_postgres_data.tar.gz -C /volume
	docker compose up --build


Windows (PowerShell):

	cd C:\путь\к\проекту
	docker volume create pianoschool_postgres_data
	docker run --rm -v pianoschool_postgres_data:/volume -v "%cd%:/backup" busybox tar xzvf /backup/pianoschool_postgres_data.tar.gz -C /volume
	docker compose up --build
