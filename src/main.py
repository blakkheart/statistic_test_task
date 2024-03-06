from fastapi import FastAPI
import uvicorn

from src.statistic.crud import router as statistic_router


app = FastAPI()
app.include_router(statistic_router, prefix='/statistic')

if __name__ == '__main__':
    uvicorn.run('src.main:app', host='127.0.0.1', port=8000, reload=False)
