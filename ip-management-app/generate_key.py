import secrets,base64

# Basic way of generating random sequence to serve as API Keys
def generate_api_key():
    r = secrets.token_bytes(16)
    
    key = base64.urlsafe_b64encode(r).decode("utf-8")
    
    return key

new_key = generate_api_key()

with open('.env','a') as f:
    f.write(f'API_KEY={new_key}\n')