import requests
import json
import os
import time

# setup
FIRST = 1
LAST = 1
DING_ON_COMPLETE = False  # set to True for dong sound on script completion
URL = "http://www.bureauwbtv.nl/tolkvertaler-search/api/search/s"
TIMEOUT = 10

# @todo grequests threading speedup?
# @todo functions

headers = {
}

json_content = {
    "searchType": "wbtv_search",
    "wbtvNumber": None
}

output = {
    "elapsed_time": 0,
    "range": {
        "first": FIRST,
        "last": LAST
    },
    "errored_customers": [],
    "exceptions": [],
    "customers": []
}

TOTAL_REQUESTS = LAST - FIRST + 1


print(f"Starting requests. {FIRST} to {LAST}, ({TOTAL_REQUESTS} total)...")

start_time = time.time()
request_number = 0
request_successes = 0
request_exceptions = 0
for wbtvNumber in range(FIRST, LAST + 1):  # range(FIRST, LAST + 1)
    request_number += 1
    json_content["wbtvNumber"] = wbtvNumber

    try:
        response = requests.post(URL, headers=headers,
                                 json=json_content, timeout=TIMEOUT)
        request_successes += 1

        time_now = time.time()
        average_request_time = float(time_now - start_time) / request_number
        requests_left = TOTAL_REQUESTS - request_number
        remaining_time = round(average_request_time * requests_left)
        remaining_time_formatted = time.strftime(
            "%H:%M:%S", time.gmtime(remaining_time))
        time_now_formatted = time.strftime("[%H:%M:%S]", time.gmtime(time_now))

        response_json = response.json()
        exists = False
        if response_json["total"] == 1:
            exists = True
            output["customers"].append(response_json["items"][0])

        elif response_json["total"]:
            raise Exception(
                f"More than 1 customer returned for wbtvNumber={wbtvNumber}")

        print(
            f"{time_now_formatted} Received #{wbtvNumber} (exists={exists}). {round(request_number / TOTAL_REQUESTS * 100, 1)}%, {remaining_time_formatted} left")

    except Exception as ex:
        output["errored_customers"].append(wbtvNumber)
        try:
            output["exceptions"].append(
                str(wbtvNumber) + "\n" + str(ex) +
                "\n\nRaw response:\n" + str(response.text)
            )
        except Exception:
            output["exceptions"].append(
                str(wbtvNumber) + "\n" + str(ex) +
                "\n\nRaw response:\n<no response>"
            )
        print(
            f"Exception on request for wbtvNumber={str(wbtvNumber)}: {str(ex)}"
        )
        request_exceptions += 1

time_now = time.time()
elapsed_time = time_now - start_time
output["elapsed_time"] = elapsed_time

time_now_formatted = time.strftime("%Y%m%dT%H%M%S", time.gmtime(time_now))
filename_formatted = f"output_{time_now_formatted}.json"

print(f"Saving to {filename_formatted}...")
with open(filename_formatted, "w", encoding="utf8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)
    size_mb = round(os.path.getsize(filename_formatted) / 1048576.0, 1)

    print(f"Saved. File size: {size_mb} MB")

elapsed_time_formatted = time.strftime(
    '%H:%M:%S', time.gmtime(elapsed_time))
print(
    f"Finished {TOTAL_REQUESTS} requests in {elapsed_time_formatted}. Exceptions: {request_exceptions} {output['errored_customers']}")

if DING_ON_COMPLETE:
    import playsound
    playsound.playsound("ding.mp3")
