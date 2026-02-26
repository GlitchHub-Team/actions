import requests

from pprint import pprint

from const import GH_TOKEN, URL


def request_api(query: str, error_blocking: bool = True) -> dict:
    headers = {
        "Authorization": f"Bearer {GH_TOKEN}"
    }
    request = requests.post(URL, json={'query': query}, headers=headers)
    
    if request.status_code == 200:
        response = request.json()

        if error_blocking and (errors := response.get('errors')):
            print("ERRORE GraphQL:")
            pprint(errors)
            exit(1)

        return response
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
