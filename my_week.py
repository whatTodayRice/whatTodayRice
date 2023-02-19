from fastapi import FastAPI
from pydantic import BaseModel
import test
app = FastAPI()

class ResponseBody(BaseModel):
    version: str
    template: dict

def show_hello():
    response_body = ResponseBody(
            version="2.0",
            template={
                "outputs": [
                    {"simpleText": {

                        "text": test.get_meal_table()
                        }
                    }
                ]
            }
        )
    return (response_body)
print(show_hello())