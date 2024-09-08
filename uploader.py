import requests

url = 'http://127.0.0.1:5000/'

image_path = './contact_photos/16.jpg'  

with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    
    response = requests.post(url, files=files,)

    print('Status Code:', response.status_code)
    print('Response:', response)
    print('Response JSON:', response.json())
