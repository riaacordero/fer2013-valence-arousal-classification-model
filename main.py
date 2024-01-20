import uvicorn
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from camera import detect_face, predict_from_img
from time import strftime, localtime
from panic_attack import PanicAttackClassifier
import asyncio
import base64
import numpy as np
import cv2

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/test_files", StaticFiles(directory="test_files"), name="test_files")

templates = Jinja2Templates(directory="templates")

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    source = request.query_params.get('source', '0')
    # play a file from /test_files/test_video/bbc_news.mp4
    # http://localhost:3000/?source=/test_files/test_video/bbc_news.mp4
    # or use the webcam ('0')
    # http://localhost:3000/?source=0 (default)
    print(source)
    return templates.TemplateResponse(
        request=request, name='index.html', context={'source': source}
    )

async def analyze(classifier: PanicAttackClassifier, websocket: WebSocket, command: str, params: dict):
    timestamp = params.get('timestamp')
    # captured = params.get('captured')
    decoded_img = base64.b64decode(params.get('image').split(',')[1])
    img_arr = np.frombuffer(decoded_img, dtype=np.uint8)
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    has_results = False

    for face, x, y, w, h in detect_face(img):
        has_results = True
        valence, arousal, emotion, result = predict_from_img(classifier, face, timestamp)
        await websocket.send_json({
            'command': command,
            'result': {
                'timestamp': strftime("%H:%M:%S", localtime()),
                'valence': valence.item(),
                'arousal': arousal.item(),
                'emotion': emotion if emotion is not None else 'unknown',
                'result': result if result is not None else '',
                'bbox': [int(x), int(y), int(w), int(h)]
            }
        })

    if not has_results:
        await websocket.send_json({
            'command': command,
            'result': {
                'timestamp': strftime("%H:%M:%S", localtime()),
                'valence': 0,
                'arousal': 0,
                'emotion': 'unknown',
                'bbox': [0,0,0,0]
            }
        })

@app.websocket('/session')
async def session(websocket: WebSocket):
    await websocket.accept()

    analyze_task = None
    panic_attack_classifier = PanicAttackClassifier()

    while True:
        data = await websocket.receive_json()
        if type(data) != dict:
            await websocket.send_json({'type': 'error', 'message': 'Invalid data'})
            continue

        command = data.get('command')
        params = data.get('params')

        match command:
            case 'analyze':
                try:
                    if analyze_task is not None and not analyze_task.done():
                        analyze_task.cancel()

                    analyze_task = asyncio.create_task(analyze(panic_attack_classifier, websocket, command, params))
                    await analyze_task
                except asyncio.CancelledError:
                    await websocket.send_json({'type': 'info', 'message': 'Analysis cancelled'})
            case 'reset_analyze':
                panic_attack_classifier.reset()
            case 'close':
                await websocket.send_json({'type': 'info', 'message': 'Closing connection'})
                await websocket.close()
            case _:
                await websocket.send_json({'type': 'error', 'message': 'Invalid command'})

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=3000)
