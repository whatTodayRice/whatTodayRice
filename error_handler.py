import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from template import KakaoTemplate
from fastapi.responses import JSONResponse

'''
에러 처리 코드
그런데... 에러의 정확한 원인을 파악할 수 없었습니다..ㅠㅠ 
'''

class Homepage:   
    def checkConnection(url:str):
        context = ssl._create_unverified_context()
        try:
            urlopen(url,timeout=2.0,context=context)
            
        except HTTPError:
            print("seems like the server is down now.")
            return False
        except URLError:
            print("Seems like the url is wrong now.")
            return False
        except TimeoutError:
            print("It's taking too long to load website")
            return False
        return True
    
    def makeErrorMessage():
        return JSONResponse(
            content=KakaoTemplate.simple_text("기숙사 홈페이지 서버가 늦고 있어요. 잠시 후 다시 시도해보세요.")
        )
        
