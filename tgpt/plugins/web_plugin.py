import requests

class Plugin:
    tag = "@web"

    def run(self, input_text, context):
        query = input_text.replace(self.tag, "").strip()
        response = requests.get(f"https://www.google.com/search?q={query}")
        return f"Search results: {response.url}"
