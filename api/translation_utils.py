import requests

def translate_to_nepali(text):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "en",
            "tl": "ne",
            "dt": "t",
            "q": text,
        }
        response = requests.get(base_url, params=params)
        response_json = response.json()
        translated_text = response_json[0][0][0]
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")  # Print the error message in the terminal
        return ""

def translate_to_english(text):
    try:
        base_url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "ne",  # Nepali
            "tl": "en",  # English
            "dt": "t",
            "q": text,
        }
        response = requests.get(base_url, params=params)
        response_json = response.json()
        translated_text = response_json[0][0][0]
        return translated_text
    except Exception as e:
        print(f"Translation error: {e}")  # Print the error message in the terminal
        return ""