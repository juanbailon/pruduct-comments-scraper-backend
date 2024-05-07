# Run container

```
docker build -t fastapi-scraper-img .
```

```
docker run -p 8080:8080 --name scraper-container  fastapi-scraper-img
```

## make request to the server
```
 http://172.17.0.2/reviews-summary/?search=acer
```
response
```
{
  "product_url": "https://amazon.com/dp/B0BTQS4N1F/",

  "positive_comments_summary": "El aspecto que más se repite en los comentarios es la velocidad y el rendimiento del producto.",
  
  "critical_comments_summary": "El aspecto que más se repite en los comentarios es la insatisfacción con la calidad y durabilidad del producto."
}
```
