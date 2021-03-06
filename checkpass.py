import requests
import hashlib
import sys


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check api and try again!')
    return res


def pwned_api_check(password):
    # hash password
    # encode in utf-8 to avoid unicode error
    sha1pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1pw[:5], sha1pw[5:]
    res = request_api_data(first5_char)
    return get_password_leaks_count(res, tail)


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times...')
        else:
            print(f'{password} was not found. Carry on!')
    return 'done!'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
