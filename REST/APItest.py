import requests
# defining the api-endpoint 
API_ENDPOINT = "http://0.0.0.0:5001/"
data = {'hi':"hello"}
r = requests.post(url = API_ENDPOINT, data = data)
  
# extracting response text 
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)