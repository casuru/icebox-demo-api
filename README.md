"# icebox-demo-api" 

git clone https://github.com/casuru/icebox-demo-api.git

cd icebox-demo-api

pip install -r requirements.txt

python3 manage.py migrate

python3 manage.py loaddata icebox/fixtures/auth.json

python3 manage.py loaddata store/fixtures/store.json

python3 manage.py runserver 