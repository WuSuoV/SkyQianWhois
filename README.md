# SkyQianWhois

支持多种后缀，功能强大全面，界面美观优雅，无广告，打造最实用的终极Whois查询工具

## 介绍

详细说明：[https://www.skyqian.com/archives/skyqianwhois.html](https://www.skyqian.com/archives/skyqianwhois.html)

## 展示

演示站点：[https://whois.yiove.com/](https://whois.yiove.com/)

| ![image-20231014095414120](https://static.wusuov.com/image/2023/10/e5c34bbd821e8ba29d35857d3a7b032f.png) | ![image-20231014095450074](https://static.wusuov.com/image/2023/10/cc4bd5394e59c11664cd5f083635aa38.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image-20231014095509932](https://static.wusuov.com/image/2023/10/7a6dac65b22c83803d084989e721abce.png) | ![image-20231014095523635](https://static.wusuov.com/image/2023/10/6732e4fb259ded6ea51e25a945a0e120.png) |

## 如何安装

```sh
curl -O https://raw.githubusercontent.com/WuSuoV/SkyQianWhois/main/docker-compose.yml
docker-compose up -d
```



## 反向代理 （仅提供示范，请根据自行需求修改）

**OpenResty:**

``` nginx
server {
    listen 80 ; 
    listen [::]:80 ; 
    server_name whois.yiove.com; 
    index index.php index.html index.htm default.php default.htm default.html; 
    proxy_set_header Host $host; 
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
    proxy_set_header X-Forwarded-Host $server_name; 
    proxy_set_header X-Real-IP $remote_addr; 
    proxy_http_version 1.1; 
    proxy_set_header Upgrade $http_upgrade; 
    proxy_set_header Connection "upgrade"; 
    access_log /www/sites/whois.yiove.com/log/access.log; 
    error_log /www/sites/whois.yiove.com/log/error.log; 
    access_by_lua_file /www/common/waf/access.lua; 
    set $RulePath /www/sites/whois.yiove.com/waf/rules; 
    set $logdir /www/sites/whois.yiove.com/log; 
    set $redirect on; 
    set $attackLog on; 
    set $CCDeny off; 
    set $urlWhiteAllow off; 
    set $urlBlockDeny off; 
    set $argsDeny off; 
    set $postDeny off; 
    set $cookieDeny off; 
    set $fileExtDeny off; 
    set $ipBlockDeny off; 
    set $ipWhiteAllow off; 
    location ^~ /.well-known/acme-challenge {
        allow all; 
        root /usr/share/nginx/html; 
    }
    include /www/sites/whois.yiove.com/proxy/*.conf; 
}
```

**Nginx**

```nginx
location / {
    proxy_pass http://127.0.0.1:10005;
    proxy_set_header Host 127.0.0.1:$server_port;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header REMOTE-HOST $remote_addr;
    add_header X-Cache $upstream_cache_status;
    proxy_set_header X-Host $host:$server_port;
    proxy_set_header X-Scheme $scheme;
    proxy_connect_timeout 30s;
    proxy_read_timeout 86400s;
    proxy_send_timeout 30s;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## 注意事项

1. 如需端口建站，请在防火墙放行 5000 端口
2. 如需80/443端口反代建站，请在防火墙和docker容器配置中禁止5000端口公网访问，并反代 localhost:5000 到 80/443端口

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=WuSuoV/SkyQianWhois&type=Date)](https://star-history.com/#WuSuoV/SkyQianWhois&Date)
