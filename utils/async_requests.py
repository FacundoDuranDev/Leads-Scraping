from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import requests



def _obtain_response(url, **kwargs):
        requestsTimeout = 5
        method  = kwargs.get("method", "GET")
        session = kwargs.get("session",None)
        while True:
            try:
                if method == "GET":
                    response = session.get(url, timeout=requestsTimeout)
                else:
                    response = None
                return response
            except requests.exceptions.ConnectionError:
                print("Connection Error, Retrying")
                time.sleep(requestsTimeout)
                continue
            except requests.exceptions.RequestException:
                print('Waiting...', url)
                time.sleep(requestsTimeout)
                continue

    # Utilizado para realizar peticiones a los episodios de forma asíncrona.
    # Por defecto se realizan de a 3 peticiones asíncronas por vez.
def _async_requests(list_urls, max_workers=3, session=requests):
    list_responses = []
    len_urls = len(list_urls)
    # ["url1","url2","url3","url4","url5","url6"] --> [["url1","url2","url3"], ["url4","url5","url6"]]
    list_urls = [list(list_urls[i:i+max_workers]) for i in range(0, len_urls, max_workers)]
    for current_urls in list_urls:
        list_threads = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for url in current_urls:
                time.sleep(0.1)
                print("ASYNC request:", url)
                list_threads.append(
                    executor.submit(_obtain_response, url,session=session))
            for task in as_completed(list_threads):
                list_responses.append(task.result())
        del list_threads

    return list_responses