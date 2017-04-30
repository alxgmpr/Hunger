from requests import request
from time import sleep
from random import randint
from datetime import datetime


def logtime():
    current = datetime.now()
    return '==' + str(current) + ' EST=='


def main():
    # SETTING THE WAIT TIME BETWEEN VOTES
    # the program is geared to pick a random number between the minimum and maximum wait
    # votes can be sent every 12 hours or every 43200 seconds.

    # FOR EXAMPLE: 400 votes per day = 200 proxies
    # 43200 / 200 proxies = 216 seconds between votes
    # So pick numbers above and below that...like 150 and 300

    # set these to the minimum wait and maximum wait between votes (in seconds)
    minwait = 2
    maxwait = 10

    print

    with open('proxies.txt') as proxies_text:
        proxies = proxies_text.read().splitlines()

    if not proxies:
        print logtime() + ' No proxies in proxies.txt file'
        exit(-1)
    else:
        print logtime() + ' Loaded ' + str(len(proxies)) + ' proxies from proxies.txt'
        print

    # p in proxies is the outer wrapper voting function.
    # process works by selecting a proxy, waiting a random range of time
    # then running the vote request
    i = 0
    for p in proxies:
        i += 1
        print logtime() + ' Currently using proxy ' + format(p) + ' for vote #' + str(i)

        # parse the proxy
        try:
            proxy_parts = p.split(':')
            ip, port, user, passw = proxy_parts[0], proxy_parts[
                1], proxy_parts[2], proxy_parts[3]
            curr_proxies = {
                'http': 'http://{}:{}@{}:{}'.format(user, passw, ip, port),
                'https': 'https://{}:{}@{}:{}'.format(user, passw, ip, port)
            }
        except IndexError:
            curr_proxies = {'http': 'http://' + p, 'https': 'https://' + p}

        # pause for a random amount of time (see top to set these wait times)
        wait = randint(minwait, maxwait)
        print logtime() + ' Waiting ' + str(wait) + ' seconds before submitting vote'
        sleep(wait)

        # call the vote with index i
        if vote(i, curr_proxies) != 0:
            print logtime() + ' Removing bad proxy' + format(p) + 'from list'
            proxies.remove(p)
        else:
            print logtime() + ' Vote #' + str(i) + ' was submitted, moving onto vote #' + str(i+1)
            print


def vote(i, proxies):
    url = "http://woobox.com/enaobd/vote/add"

    # set the ID key to the ID of the submission you want to promote.
    payload = {
        'id': '20201205',
        'signed_request': 'false'
        }
    headers = {
        'accept': "*/*",
        'origin': "http://woobox.com",
        'x-requested-with': "XMLHttpRequest",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
        'content-type': "application/x-www-form-urlencoded",
        'dnt': "1",
        'referer': "http://woobox.com/enaobd/gallery/Wk0-NFAHBco",
        'accept-encoding': "gzip, deflate",
        'accept-language': "en-US,en;q=0.8",
        'cache-control': "no-cache"
        }
    print logtime() + ' Submitting vote #' + str(i) + ' with proxies: ' + format(proxies)

    response = request("POST", url, data=payload, headers=headers, proxies=proxies)

    # make sure it goes through
    if response.status_code != 200:
        print logtime() + ' Vote #' + str(i) + ' encountered bad response code ' + str(response.status_code)
        return -1
    else:
        print logtime() + ' Vote #' + str(i) + ' encountered good response code '
        return 0


if __name__ == '__main__':
    main()