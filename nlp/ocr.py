import os
import json
import requests
text_file = open("path.txt","r")
x=text_file.read()
text_file.close()
        
API_KEY = '796ebd9abbd04653a98cc260e124382d'
ENDPOINT = 'https://southeastasia.api.cognitive.microsoft.com/vision/v1.0/ocr'
DIR = x

def handler():
        text = ''
        results = get_text(x)
        text += parse_text(results)

        open('output.txt', 'w').write(text)
    
def parse_text(results):
    text = ''
    for region in results['regions']:
        for line in region['lines']:
            for word in line['words']:
                text += word['text'] + ' '
            text += '\n'
    print(text)
    return text  

def get_text(pathToImage):
    print('Processing: ' + pathToImage)
    headers  = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-Type': 'application/octet-stream'
    }
    params   = {
        'language': 'en',
        'detectOrientation ': 'true'
    }
    payload = open(pathToImage, 'rb').read()
    response = requests.post(ENDPOINT, headers=headers, params=params, data=payload)
    results = json.loads(response.content)
    return results

if __name__ == '__main__':
    handler()
