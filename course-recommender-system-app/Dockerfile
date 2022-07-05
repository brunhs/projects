FROM python:3.8.13
ARG port=5000

# USER root
COPY . /course-recommender-system-app
WORKDIR /course-recommender-system-app

ENV PORT=$port

RUN apt-get update && apt-get install -y --no-install-recommends apt 

RUN chgrp -R 0 /course-recommender-system-app \
    && chmod -R g=u /course-recommender-system-app \
    && pip install pip --upgrade \
    && pip install -r requirements.txt

EXPOSE $PORT

CMD ["python", "./app.py"]