import requests

class Invoker:
    def __init__(self):
        pass

    def invoke(self, method, url: str, params: list, headers: dict, data: dict, auth: dict):
        request = requests.Request(
            method,
            url = url,
            params = params,
            headers = headers,
            data = data,
            auth = auth
        )

        prepared = request.prepare()
        response = requests.Session().send(prepared)

        print(f"{response.status_code} | {method.ljust(4)} | {url}")

        return (response)