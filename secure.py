from datetime import datetime as dt

PROXY_ID = 0


class Proxy:
    PROXY_HOST = None
    PROXY_PORT = None
    PROXY_USER = None
    PROXY_PASS = None

    __manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"76.0.0"
    }
    """

    def set_background_js(
            self,
            PROXY_HOST,
            PROXY_PORT,
            PROXY_USER,
            PROXY_PASS):
        self.PROXY_HOST = PROXY_HOST
        self.PROXY_PORT = PROXY_PORT
        self.PROXY_USER = PROXY_USER
        self.PROXY_PASS = PROXY_PASS

    def get_background_js(self):
        return """
            let config = {
                    mode: "fixed_servers",
                    rules: {
                    singleProxy: {
                        scheme: "http",
                        host: "%s",
                        port: parseInt(%s)
                    },
                    bypassList: ["localhost"]
                    }
                };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "%s",
                        password: "%s"
                    }
                };
            }
            chrome.webRequest.onAuthRequired.addListener(
                        callbackFn,
                        {urls: ["<all_urls>"]},
                        ['blocking']
            );
            """ % (self.PROXY_HOST, self.PROXY_PORT, self.PROXY_USER, self.PROXY_PASS)

    def get_manifest_json(self):
        return self.__manifest_json

    def set_proxy(self, PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
        self.PROXY_HOST = PROXY_HOST
        self.PROXY_PORT = PROXY_PORT
        self.PROXY_USER = PROXY_USER
        self.PROXY_PASS = PROXY_PASS


def get_proxy_list(file_name):
    proxy_list = []
    with open(file_name) as f:
        for line in f:
            proxy_line = []
            user = line.split(':')[0]
            port = line.split(':')[-1].replace('\n', '')
            password = line.split('@')[0].split(':')[-1]
            ip = line.split('@')[-1].split(':')[0]
            proxy_line.append(ip)
            proxy_line.append(port)
            proxy_line.append(user)
            proxy_line.append(password)
            proxy_list.append(proxy_line)
    return proxy_list


# proxy_file = 'proxy'
# proxies = get_proxy_list(proxy_file)
# num_proxs = len(proxies)


def get_proxy_pref(mode):
    host = proxies[PROXY_ID][0]
    port = proxies[PROXY_ID][1]
    user = proxies[PROXY_ID][2]
    pas = proxies[PROXY_ID][3]
    if mode == 0:
        proxy1.set_proxy(host, port, user, pas)
        return proxy1.get_manifest_json()
    elif mode == 1:
        proxy1.set_background_js(host, port, user, pas)
        return proxy1.get_background_js()
    elif mode == 3:
        return host, port, user, pas


proxy1 = Proxy()


class Log:
    __cur_dt = dt.now()
    __cur_dt_str = __cur_dt.strftime('%m-%d-%y %H-%M-%S')
    __log_name = f"log_{__cur_dt_str}.txt"

    def get_log_name(self):
        return self.__log_name

    def create_log(self):
        with open(f"result/{self.__log_name}", "w", encoding="utf-8"):
            pass

    def write_log(self, reason, ex):
        cur_dt = dt.now()
        cur_dt_str = cur_dt.strftime('%m-%d-%y %H-%M-%S')
        with open(f"result/{self.__log_name}", "a", encoding="utf-8") as file:
            file.write(cur_dt_str + " - " + reason + "\n" + str(ex) + "\n")


log = Log()


# def get_proxy_list(file_name):
#     proxy_list = []
#     with open(file_name) as f:
#         j_proxy = json.load(f)
#         vals = dict(j_proxy).values()
#         for country in vals:
#             for proxy in country:
#                 # print(proxy)
#                 # proxy_line = []
#                 port = proxy.split(':')[-1].replace('\n', '')
#                 ip = proxy.split('/')[2].split(':')[0]
#                 # proto = proxy.split(':')[0]
#                 # proxy_line.append(proto)
#                 # proxy_line.append(ip)
#                 # proxy_line.append(port)
#                 proxy_list.append(f'{ip}:{port}')
#     return proxy_list


# proxy_file = './jsons/good_proxies.json'
proxy_file = 'proxy.txt'
proxies = get_proxy_list(proxy_file)
num_proxs = len(proxies)
