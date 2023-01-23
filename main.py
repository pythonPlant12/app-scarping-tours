import requests
import selectorlib
import smtplib
import time
# Web scraping
URL = "http://programmer100.pythonanywhere.com/tours/"
# Sometimes servers don't like script programs, so in order to make it like a browser we should use for example:
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def scrape(url):
    """Scrape the page source from the URL"""
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "testpythonplant@gmail.com"
    PASSWORD = "cawntenkvjgzmmfe"

    SENDER = "testpythonplant@gmail.com"
    RECEIVER = "testpythonplant@gmail.com"

    with smtplib.SMTP_SSL(host, port) as server:
        server.login(username, PASSWORD)
        server.sendmail(SENDER, RECEIVER, message)
    print("Email was sent!")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    with open("data.txt", "r") as file:
        return file.read()


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)
        content = read(extracted)

        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="Hey, new event was found!")
        time.sleep(2)