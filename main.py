from wox import Wox
import requests
from bs4 import BeautifulSoup
import webbrowser

class Translator(Wox):

    def query(self, query):
        output_results = []
        header = {"User-Agent": "Mozilla/5.0"}
        url = "https://dictionary.cambridge.org/zhs/%E8%AF%8D%E5%85%B8/%E8%8B%B1%E8%AF%AD-%E6%B1%89%E8%AF%AD-%E7%AE%80%E4%BD%93/"
        url += query
        check = requests.get(url, headers=header)
        soup = BeautifulSoup(check.text, 'html.parser')
        results = soup.find_all("div", attrs={'class': ["def-body", "ddef_b"]})
        if len(results):
            for i in results:
                output_results.append({
                    "Title": i.span.text,
                    "SubTitle": "from Cambridge Dictionary",
                    "IcoPath":"Images/icon.ico",
                    "ContextData": "ctxData"
                })
            
        else:
            url = "https://translate.google.com/?sl=auto&tl=zh-CN&op=translate&text="
            url += query
            output_results.append({
                "Title": "Open Google Translation",
                "SubTitle": "Cambridge Dictionary doesn't support sentence translation",
                "IcoPath":"Images/icon.ico",
                "JsonRPCAction": {
                    "method": "openWeb",
                    "parameters": [url], 
                    "dontHideAfterAction": False
                }
            })
        return output_results


    def openWeb(self, url):
        webbrowser.open(url)


if __name__ == "__main__":
    Translator()