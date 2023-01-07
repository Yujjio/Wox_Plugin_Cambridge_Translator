from wox import Wox
import requests
from bs4 import BeautifulSoup
import webbrowser

class Translator(Wox):
    def is_chinese(self, strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
            else:
                return True
        return False

    def query(self, query):
        header = {"User-Agent": "Mozilla/5.0"}
        output_results = []
        if self.is_chinese(str(query)):
            url = "https://dict.cn/search?q="
            url += query
            temp = requests.get(url, headers=header)
            soup = BeautifulSoup(temp.text, "html.parser")
            eng_result = soup.find(name="div", attrs={"class": ["layout", "cn"]})
            eng_result = eng_result.ul.contents
            for i in range(len(eng_result)):
                each = eng_result[i].text.strip()
                if each == '':
                    continue
                else:
                    output_results.append({
                        "Title": each,
                        "SubTitle": "from dict.cn",
                        "IcoPath":"Images/icon.ico",
                        "ContextData": "ctxData"
                    })
            return output_results
        else:
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