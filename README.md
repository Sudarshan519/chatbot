---
title: FastAPI
description: A FastAPI server
tags:
  - fastapi
  - python
---

# FastAPI Example

This example starts up a [FastAPI](https://fastapi.tiangolo.com/) server.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template/-NvLj4?referralCode=milo)
## ✨ Features

- FastAPI
- Python 3

## 💁‍♀️ How to use

- Deploy using the button 👆
- Clone locally and install packages with Pip using `pip install -r requirements.txt` or Poetry using `poetry install`
- Connect to your project using `railway link`
- Run locally using `uvicorn main:app --reload`

## 📝 Notes

- To learn about how to use FastAPI with most of its features, you can visit the [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/).
- FastAPI provides automatic documentation to call and test your API directly from the browser. You can access it at `/docs` with [Swagger](https://github.com/swagger-api/swagger-ui) or at `/redoc` with [Redoc](https://github.com/Rebilly/ReDoc).


source venv/bin/activate
 locust -f api_test_user
 uvicorn main:app --reload --host=192.168.0. --reload-dir apps/rps_remit


    query = db.query(Product.id, Product.name, func.sum(Product.price * Order.quantity).label("total_price")) \
        .outerjoin(Order) \
        .group_by(Product.id, Product.name) \
        .all()


  from django.db.models import Sum, F
  product_list = Product.objects.annotate(
    total_price=Sum(F('order__quantity') * F('price'), distinct=True)
)


# Run Docker
docker-compose up -d --build

whitelisted ip
111.119.49.75 
110.44.115.161
