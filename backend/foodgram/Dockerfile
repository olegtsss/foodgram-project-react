FROM python:3.7-slim
WORKDIR /app
COPY foodgram-project-react/backend/foodgram/requirements.txt .
RUN pip3 install -r ./requirements.txt --no-cache-dir
COPY foodgram-project-react/backend/foodgram/ .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
#CMD ["python3", "manage.py", "runserver", "0:8000"]
LABEL author='olegtsss' version=1.1