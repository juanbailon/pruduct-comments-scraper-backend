import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from utils import amazon_comment_scraper, get_comments_summary_from_GPT

from dotenv import load_dotenv
load_dotenv()

class ImageURL(BaseModel):
    img_url: str

API_KEY = os.getenv("API_KEY")

app = FastAPI()

origins = [
    "*"
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/reviews-summary/")
async def check_for_adult_content(search: str):
    
    try:
       product_url, comments_positive, comments_critical = await amazon_comment_scraper(product_name= search)

       positive = await get_comments_summary_from_GPT(api_key= API_KEY, comments= comments_positive)
       critical = await get_comments_summary_from_GPT(api_key= API_KEY, comments= comments_critical)

       return JSONResponse(content=
                           {
                            'product_url': product_url, 
                            'positive_comments_summary': positive, 
                            'critical_comments_summary': critical
                           }
           )
    
    except Exception as e:
        raise e