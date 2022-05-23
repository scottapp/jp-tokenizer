import os
import sys
import json
import fugashi

from fastapi import Depends, FastAPI, HTTPException
from typing import List, Union
from pydantic import BaseModel

from fastapi_login import create_app
from jp_tokenizer.core import convert_furigana

# uvicorn server:app  --reload --host 0.0.0.0 --port 8000
app = create_app()
tagger = fugashi.Tagger()


class WordToken(BaseModel):
    surface: str = None
    furi: str = None
    type: str = None


@app.get("/hello")
async def hello_world():
    return {'msg': 'Hello World', 'app':'jp_tokenizer'}


@app.get("/jp/convert", response_model=List[WordToken])
async def convert_sentence():
    sentence = "麩菓子は、麩を主材料とした日本の菓子。"
    words = convert_furigana(tagger, sentence)
    output = list()
    for word in words:
        t = WordToken()
        t.surface = word.get('surface', '')
        t.furi = word.get('furi', '')
        t.type = word.get('type', '')
        output.append(t)
    return output
