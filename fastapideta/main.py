from fastapi import FastAPI
from pydantic import BaseModel
from crawller import new_breakfast
app = FastAPI()

class ResponseBody(BaseModel):
    version: str
    template: dict

@app.get("/")
def read_root():
    return {"hello":'World'}


@app.post("/showHello")
async def show_hello():
    response_body = ResponseBody(
        version="2.0",
        template={
            "outputs": [
                {
                    "simpleText": {
                        "text": new_breakfast
                    }
                }
            ]
        }
    )
    return response_body

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



