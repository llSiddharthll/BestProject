from curl_cffi.requests import get, RequestsError
from uuid import uuid4
from re import findall

def chatAI(prompt):
    url = "https://you.com/api/streamingSearch"

    response = get(
        url,
        headers={
            "cache-control": "no-cache",
            "referer": "https://you.com/search?q=gpt4&tbm=youchat",
            "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
        },
        params={
            "q": prompt,
            "page": 1,
            "count": 10,
            "safeSearch": "Off",
            "onShoppingPage": False,
            "mkt": "",
            "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
            "domain": "youchat",
            "queryTraceId": str(uuid4()),
            "chat": [],
        },
        impersonate="chrome107",
    )
    if "youChatToken" not in response.text:
        raise RequestsError("Unable to fetch the response.")

    return (
        "".join(
            findall(
                r"{\"youChatToken\": \"(.*?)\"}",
                response.content.decode("unicode-escape"),
            )
        )
        .replace("\\n", "\n")
        .replace("\\\\", "\\")
        .replace('\\"', '"')
    )