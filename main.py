from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks

app = FastAPI()

languages = ["English", "Hindi", "German", "French"]
    
class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str
    
    @validator('base_lang','final_lang')
    def valid_lang(cls, lang):
        if lang not in languages:
            raise ValueError("Invalid Language")
        return lang
 
#testing route    
@app.get("/")
def get_root():
    return { "message": "Hello World!" }

@app.post("/translate")
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    t_id = tasks.store_translation(t)
    background_tasks.add_task(tasks.run_translation, t_id)
    return { "task_id": t_id }

@app.get("/results")
def get_translation(t_id: int):
    return { "translation": tasks.find_translation(t_id) }
        