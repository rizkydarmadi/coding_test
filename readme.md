
## How to install
- Clone this repo
```bash
git clone https://github.com/rizkydarmadi/coding_test.git
```
- Create virtualenv(python 3.11.4 and ubuntu os is recommended)
```bash
python -m venv env
```
- Activate virtualenv
```bash
source env/bin/activate
```
- Change directory to /backend_coding_test
```bash
cd backend_coding_test
```
- Create migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
- Run Server
```bash
python manage.py runserver
```

on server: http://localhost:8000/countries/

for other path and api
- http://localhost:8000/login/
- http://localhost:8000/logout/
- http://localhost:8000/countries/
- http://localhost:8000/countries/create/
- http://localhost:8000/countries/<int:pk>/update/
- http://localhost:8000/countries/<int:pk>/delete/
- http://localhost:8000/categories/
- http://localhost:8000/categories/create/
- http://localhost:8000/categories/<int:pk>/update/,
- http://localhost:8000/categories/<int:pk>/delete/,
- http://localhost:8000/api/token/
- http://localhost:8000/api/token/refresh/
- http://localhost:8000/api/token/verify/
- http://localhost:8000/api/countries/
- http://localhost:8000/api/countries/<int:pk>/
- http://localhost:8000/api/categories/,
- http://localhost:8000/api/categories/<int:pk>/
- http://localhost:8000/api/destination/
- http://localhost:8000/api/calculate/


