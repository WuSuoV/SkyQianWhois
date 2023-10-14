from flask import Flask, render_template, request
from functions.whois import Whois
from cache import cache

app = Flask(__name__)
cache.init_app(app)


@app.route('/')
def app_index():
    return render_template('index.html', url='Yiove.com')


@app.route('/<domain>')
def app_domain(domain):
    return render_template('domain.html', doamin=domain, url='Yiove.com')


@app.route('/whois', methods=['POST'])
def app_whois():
    domain = request.values.get('domain')

    # 直接跳过缓存
    return Whois(domain).whois()

    # 缓存键
    key = f'{domain}-whois'
    result = cache.get(key)

    if result is None:
        value = Whois(domain).whois()
        cache.set(key, value)
        return value
    else:
        return result


@app.route('/price', methods=['POST'])
def app_price():
    domain = request.values.get('domain')

    # 缓存键
    key = f'{domain}-price'
    result = cache.get(key)

    if result is None:
        value = Whois(domain).price()
        cache.set(key, value)
        return value
    else:
        return result


@app.route('/icp', methods=['POST'])
def icp():
    domain = request.values.get('domain')

    # 缓存键
    key = f'{domain}-icp'
    result = cache.get(key)

    if result is None:
        value = Whois(domain).icp()
        cache.set(key, value)
        return value
    else:
        return result


if __name__ == '__main__':
    app.run()
