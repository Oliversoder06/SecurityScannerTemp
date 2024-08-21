import requests
from http.cookies import SimpleCookie
from urllib.parse import urlparse
import json
from time import time
from bs4 import BeautifulSoup

##### COOKIES #####

# Check if cookie is secure
def is_secure(cookie):
    return cookie.get('secure', False)

# Check if cookie is HttpOnly
def is_httponly(cookie):
    return cookie.get('httponly', False)

# Check if cookie is SameSite
def is_samesite(cookie):
    same_site = str(cookie.get('samesite', '')).lower()
    if same_site == 'strict':
        return "good", "SameSite=Strict"
    elif same_site == 'lax':
        return "good", "SameSite=Lax"
    elif same_site == 'none' and is_secure(cookie):
        return "good", "SameSite=None with Secure"
    else:
        return "bad", "Missing or invalid SameSite"
    
# Check if cookie is expired
def check_expiration(cookie):
    max_age = cookie.get('max-age')
    expires = cookie.get('expires')

    excessive_lifetime = 365 * 24 * 60 * 60  # 1 year in seconds

    if max_age:
        if int(max_age) > excessive_lifetime:
            return 'bad', 'Excessively Long Expiration Date'
        else:
            return 'good', 'Reasonable Max-Age'
    elif expires:
        if int(expires) - time() > excessive_lifetime:
            return 'bad', 'Excessively Long Expiration Date'
        else:
            return 'good', 'Reasonable Expiration Date'
    else:
        return 'good', 'Session Cookie'
    
# Check attributes of a cookie
def check_cookie_attributes(cookie):
    secure = is_secure(cookie)
    httponly = is_httponly(cookie)
    samesite, samesite_value = is_samesite(cookie)
    expiration, expiration_value = check_expiration(cookie)

    return secure, httponly, samesite, samesite_value, expiration, expiration_value

# Analyze cookies from website
def analyze_cookies(url):
    # Parse the URL
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url

    # Get response from website
    response = requests.get(url)
    
    # Get cookies from the response
    cookie_jar = response.cookies
    cookies = []
    for cookie in cookie_jar:
        cookies.append({
            'name': cookie.name,
            'value': cookie.value,
            'secure': cookie.secure,
            'httponly': cookie.has_nonstandard_attr('HttpOnly'),
            'samesite': cookie.get_nonstandard_attr('SameSite'),
            'expires': cookie.expires,
        })

    # Analyze each cookie and append results
    results = []
    for cookie in cookies:
        secure, httponly, samesite, samesite_value, expiration, expiration_value = check_cookie_attributes(cookie)
        cookie_result = {
            'name': cookie['name'],
            'secure': secure,
            'httponly': httponly,
            'samesite': samesite,
            'samesite_value': samesite_value,
            'expiration': expiration,
            'expiration_value': expiration_value,
        }
        results.append(cookie_result)

    # Output the results as JSON
    print(json.dumps(results, indent=4))

##### COOKIES #####




# Main function
if __name__ == "__main__":
    import sys
    # url = sys.argv[1]
    url = "https://www.google.com"
    analyze_cookies(url)
    sys.stdout.flush()