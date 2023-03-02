class KakaoTemplate:
    
    def build_simple_text(message: str):
        data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ],
                "quickReplies": [
                    {"messageText":"오늘 식단", "action": "message","label":"오늘 식단"},
                    {"messageText":"내일 식단", "action": "message","label":"내일 식단"},
                    {"messageText":"주간 식단", "action": "message","label":"주간 식단"},
                ]}}
        return data
    
    def build_register_dormitory_text(message: str):
        data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ],
                "quickReplies": [
                    {"messageText":"기숙사 등록", "action": "message","label":"기숙사 등록"},
                    {"messageText":"건의사항", "action": "message","label":"건의사항"},
    
                ]}}
        return data
    
    
    
    def build_no_menu_text(message: str):
        data = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": message
                        }
                    }
                ],
                "quickReplies": [
                    {"messageText":"홈으로", "action": "message","label":"홈으로"},
                    {"messageText":"도움말", "action": "message","label":"도움말"},
                    {"messageText":"건의사항", "action": "message","label":"건의사항"},
                ]}}
        return data 