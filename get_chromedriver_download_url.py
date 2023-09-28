import sys
import urllib.request
import json

response = urllib.request.urlopen(
    "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json"
)
data = json.load(response)

chrome_driver_result = data["channels"]["Stable"]["downloads"]["chromedriver"]

platform = sys.argv[1] if len(sys.argv) >= 2 else None

if platform is None:
    print(
        "Error: Please provide platform for which chromedriver download url will be fetched."
    )
    sys.exit(1)

found = False

for result in chrome_driver_result:
    if result["platform"] == platform:
        print(result["url"])
        found = True
        break

if not found:
    print(f'Error: Unable to find chromedriver download url for platform "{platform}"')
    sys.exit(1)
