FROM python:3.10-alpine
ENV TZ=Asia/Shanghai
WORKDIR /app
COPY . /app/
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
&& echo $TZ > /etc/timezone \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
&& pip install flask-caching
EXPOSE 5000
CMD ["flask","run","-h","0.0.0.0","-p","5000"]
