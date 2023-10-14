FROM python:3.10
ENV TZ=Asia/Shanghai
WORKDIR /app
COPY . /app
RUN ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
&& echo $TZ > /etc/timezone \
&& pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]
