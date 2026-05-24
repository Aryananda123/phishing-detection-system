import re
from urllib.parse import urlparse
import tldextract

def extract_features(url):
    """
    Extracts features from a URL for phishing detection.
    Returns a dictionary of features.
    """
    # Ensure URL has a scheme for proper parsing
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url

    parsed_url = urlparse(url)
    ext = tldextract.extract(url)
    
    # Feature 1: URL length
    url_length = len(url)
    
    # Feature 2: Domain length
    domain_length = len(parsed_url.netloc)
    
    # Feature 3: Check for IP address in domain
    has_ip = 1 if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', parsed_url.netloc) else 0
    
    # Feature 4: Count of '@' symbol (often used in phishing to hide the real domain)
    count_at = url.count('@')
    
    # Feature 5: Count of '-' in domain (phishers often use dash to make fake domains look real)
    count_dash_domain = parsed_url.netloc.count('-')
    
    # Feature 6: Check for shortening service
    shortening_services = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net'
    has_shortener = 1 if re.search(shortening_services, parsed_url.netloc, re.I) else 0
    
    # Feature 7: HTTPS token in domain
    https_in_domain = 1 if 'https' in parsed_url.netloc else 0
    
    # NLP Features: Keywords commonly used in phishing
    suspicious_words = ['login', 'verify', 'update', 'secure', 'account', 'bank', 'paypal', 'apple', 'security', 'free']
    
    keyword_count = 0
    url_lower = url.lower()
    for word in suspicious_words:
        if word in url_lower:
            keyword_count += 1
            
    return {
        'url_length': url_length,
        'domain_length': domain_length,
        'has_ip': has_ip,
        'count_at': count_at,
        'count_dash_domain': count_dash_domain,
        'has_shortener': has_shortener,
        'https_in_domain': https_in_domain,
        'keyword_count': keyword_count
    }

def get_feature_names():
    return [
        'url_length', 'domain_length', 'has_ip', 'count_at', 
        'count_dash_domain', 'has_shortener', 'https_in_domain', 'keyword_count'
    ]
