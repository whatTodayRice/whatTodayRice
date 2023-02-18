class KakaoTemplate:
    
    def simple_text(msg: str):
        return {
    "version": "2.0",
    "template": {
        "outputs": [
            {
                "simpleText": {
                    "text": msg
                }
            }
        ]
    }
}
        