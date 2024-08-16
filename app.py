from fastapi import FastAPI, Query
from pydantic import BaseModel
#from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig

from fastapi import Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
import io
import os
import time
import requests
import jsonify

app = FastAPI()

# Model and Tokenizer setup
# model_name = "google/flan-t5-base"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
# config = GenerationConfig(max_new_tokens=200)

# class PromptRequest(BaseModel):
#     line: str

# @app.get("/ai", summary="Generate text based on a prompt", description="This endpoint uses a pre-trained FLAN-T5 model to generate text from the given prompt.")
# def generate_text(prompt: str = Query(..., description="The prompt text to generate a response for")) -> str:
#     """
#     Generate text using the FLAN-T5 model.
   
#     This endpoint accepts a prompt and returns the generated text based on the model's inference.
   
#     - **prompt**: The input text for the model to generate a continuation.
#     """
#     tokens = tokenizer(prompt, return_tensors="pt")
#     outputs = model.generate(**tokens, max_new_tokens=config.max_new_tokens)
#     result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
#     return result[0]


# React build 파일을 정적 파일로 서빙
app.mount("/static", StaticFiles(directory="./build/static"), name="static")


templates = Jinja2Templates(directory="./build")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


# class inputText(BaseModel):
#     inputText: str
# @app.post("/post_inputText")
# async def receive_text(item: inputText):
#     # 클라이언트로부터 받은 텍스트를 처리합니다.
#     text = item.inputText
    
#     file_path = './static/output.txt'
#     # 텍스트 파일 생성
#     with open(file_path, "w") as file:
#         file.write(text)
    
#     # 생성된 파일을 클라이언트에게 전송
#     return FileResponse(file_path, media_type='application/octet-stream', filename=file_path)


# @app.post("/generate-file")
# async def generate_file(text: str = Form(...)):
#     time.sleep(2)
#     file_path = './static/vitals/restored_json_0813_0001.vital'
    
#     # 생성된 파일을 클라이언트에게 전송
#     return FileResponse(file_path, media_type='application/octet-stream', filename=file_path)



# @app.post("/generate-file")
# async def generate_file(text: str = Form(...)):
    


@app.post('/generate-file')
async def generate_file(text: str = Form(...)):
    try:
        input_text = text
        print(input_text)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Error in input processing: {e}"})

    try:
        # 외부 API에 POST 요청 보내기
        print('try')
        response = requests.post('http://aiyou_con:8000/ai', params={'prompt': input_text})

        response.raise_for_status()  # 요청이 성공적인지 확인

        # ZIP 파일을 반환하는 경우
        if response.headers['Content-Type'] == 'application/zip':
            # 응답 데이터를 바이너리 스트림으로 변환
            zip_file = io.BytesIO(response.content)

            # StreamingResponse로 클라이언트에 반환
            return StreamingResponse(zip_file, media_type='application/zip', headers={
                "Content-Disposition": "attachment; filename=generated_file.zip"
            })
        # 다른 처리 방식이 필요할 경우 여기에 추가 로직
        else:
            raise HTTPException(status_code=400, detail="Unexpected content type")
    except requests.exceptions.RequestException as e:
        # 오류 발생 시 클라이언트에 에러 메시지 반환
        print('bad')
        raise HTTPException(status_code=500, detail=str(e))
    


@app.get("/getsound")
async def get_sound():
    file_path = "./static/sounds/audio.wav"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio file not found")
    
    return FileResponse(path=file_path, media_type="audio/wav", filename="audio.wav")

