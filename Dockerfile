## Dockerfile

FROM python:3.9.16-slim-bullseye

RUN mkdir product_webcrawler_job
# 進去容器及指到該資料夾
WORKDIR /product_webcrawler_job
# 複製所有檔案進去該資料夾
COPY . ./

RUN apt-get update -y 

RUN apt-get install -y --no-install-recommends tzdata
RUN apt-get install -y procps
RUN TZ=Asia/Taipei \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata 

RUN pip install -r requirements.txt

RUN chmod -cR 640 *

RUN echo $(pwd)

CMD [ "python","-u","app.py" ]

