import requests


def request(proxy_list):
    proxies = ''
    if isinstance(proxy_list, list):
        proxies = {"http": x for x in proxy_list}
    elif isinstance(proxy_list, str) and "," in proxy_list:
        proxies = {"http": x for x in proxy_list.replace('"', '').replace("'", "").split(",")}
    else:
        print("格式不对")

    if proxies:
        url = "http://httpbin.org/ip"
        response = requests.get(url=url, proxies=proxies, timeout=10)

        return response.status_code


proxies = ["213.30.13.147:8379", "185.41.112.29:57190", "1.20.97.214:38550", "171.80.173.73:9013", "182.88.126.86:8287"]
print(request(proxy_list=proxies))
