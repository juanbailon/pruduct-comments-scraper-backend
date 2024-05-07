import requests
import scraper


async def amazon_comment_scraper(product_name: str) -> tuple[str, list[str], list[str]]:
    
    driver = scraper.create_firefox_web_driver_conection()
    try:
        scraper.open_url(driver, scraper.AMAZON_US_URL)

        scraper.search_product_amazon(driver, product_name= product_name)
        product_id = scraper.get_amazon_choice_product_id(driver)
        product_url = scraper.get_amazon_product_url_by_id(product_id)

        review_url = scraper.get_amazon_product_reviews_url(product_id= product_id, review_type= 'positive')
        comments_positive = scraper.get_product_comments(driver, review_url)

        review_url_2 = scraper.get_amazon_product_reviews_url(product_id= product_id, review_type= 'critical')
        comments_critical = scraper.get_product_comments(driver, review_url_2)

        if comments_positive != None:
            comments_positive = [comment for comment in comments_positive if len(comment)!=0]

            if len(comments_positive) == 0: comments_positive = None
        
        if comments_critical != None:
            comments_critical = [comment for comment in comments_critical if len(comment)!=0]
            
            if len(comments_critical) == 0: comments_critical = None


        scraper.close_driver_conection(driver= driver)

        return (product_url, comments_positive, comments_critical)     
    
    except Exception as e:
        scraper.close_driver_conection(driver= driver)
        raise e





async def get_comments_summary_from_GPT(api_key: str, comments: list[str]):

    if comments == None:
        return "No hay comentarios al respecto"

    prompt = "te voy a dar unos comentrios/reviews sobre un producto, Los comentarios pueden\
         estar escritos en ingles o espanol, tu respesta debe de ser en espanol. por favor dime\
         cual es el tema o aspecto que mas se repite.\
         Si no entre los comentario  NO hay ningun tema o aspecto que se repita,\
         solo retorna la palabra NULL y nada mas. trabaja solo con los comentarios que te doy.\
         Tu respuesta NO puede superar las 30 palabras, 30 es el maximo de palabras que puedes usar en la respuesta.\n \
         estos son los comentarios: \n"
    
    all_comments = ""
    for comment in comments:
        all_comments += comment + '\n' + '\n'

    try:
        response = requests.post('https://api.openai.com/v1/chat/completions',
                                 headers={
                                     'Content-Type': 'application/json',
                                     'Authorization': f'Bearer {api_key}'
                                 },
                                 json={
                                     'model': 'gpt-3.5-turbo-16k',
                                     'messages': [{'role': 'user', 'content': f'{prompt}\n{all_comments}'}],
                                     'max_tokens': 50
                                 })

        if not response.ok:
            raise Exception(f"OpenAI API Error: {response.status_code} - {response.reason}")
        
        data = response.json()

        # print(response.status_code , '\n', data)
            
        return data.get('choices')[0].get('message').get('content')

    except Exception as e:
        raise Exception(f"OpenAI API Request Failed: {e}")
    


if __name__ == '__main__':
    import os
    import asyncio
    from dotenv import load_dotenv
    load_dotenv()

    API_KEY = os.getenv("API_KEY")

    async def main():
        result = await get_comments_summary_from_GPT(API_KEY, ['muy bueno', 'excelente calidad', 'buena relacion calidad precio'])
        print(result)

    asyncio.run(main())


