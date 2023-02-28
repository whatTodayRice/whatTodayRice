class KakaoTemplate:
    
    def build_menu_text(message: str):
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
    
    def build_dormitory_text(message):
        data = {
            "version": "2.0",
            "template": {
                "outputs": [{"simpleText": {"text": message}}],
                "quickReplies": [
                    {"messageText":"오늘 식단", "action": "message","label":"오늘 식단"},
                    {"messageText":"내일 식단", "action": "message","label":"내일 식단"},
                    {"messageText":"주간 식단", "action": "message","label":"주간 식단"},
                ]
            },
        }
        return data
        
       