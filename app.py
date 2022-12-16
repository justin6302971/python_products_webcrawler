import schedule
import time
from crawlers.hermes import collect_product

from constants.crawler_url import HERMES_BAGS_AND_SMALL_LEATHER_GOODS_URL
from constants.linenotify_url import LOGIN_URL, MESSAGE_URL
from databases.productinfodb import Product, session
from datetime import datetime
import requests,random
from os import environ


def upsert_product_job():
    print("start collecting product")
    latest_product_info_list = collect_product(
        HERMES_BAGS_AND_SMALL_LEATHER_GOODS_URL)

    if len(latest_product_info_list) == 0:
        print("got error when collecting product ")
        return

    print("done collecting product")

    print('start processing product item')

    current_product_entity_list = session.query(
        Product).filter(Product.status == True).all()

    current_product_code_list = set(
        x.code for x in current_product_entity_list)  # All ids in list 1

    intersection_product_info_list = [
        item for item in latest_product_info_list if item['code'] in current_product_code_list]

    intersection_product_code_list = set(
        x['code'] for x in intersection_product_info_list)

    new_product_info_list = [
        item for item in latest_product_info_list if item['code'] not in intersection_product_code_list]

    if len(new_product_info_list) > 0:
        for item in new_product_info_list:
            new_product_entity = Product(
                code=item["code"], description=item["description"], created_dt=datetime.now())
            session.add(new_product_entity)
        session.commit()

    offline_product_info_list = [
        item for item in current_product_entity_list if item.code not in intersection_product_code_list]

    if len(offline_product_info_list) > 0:
        for item in offline_product_info_list:
            item.status = False
            item.modified_dt = datetime.now()
        session.commit()

    intersection_product_entity_list = [
        item for item in current_product_entity_list if item.code in intersection_product_code_list]
    if len(intersection_product_entity_list) > 0:
        for item in intersection_product_entity_list:
            if item.notify_counts >= 3 and item.status == True and item.is_new_item == True:
                item.is_new_item = False
                item.modified_dt = datetime.now()
        session.commit()

    print('done processing product item')


def check_latest_products():
    print("start checking new product")
    new_product_entity_list = session.query(Product).filter(
        Product.status == True, Product.is_new_item == True, Product.notify_counts < 3).all()
    if len(new_product_entity_list) > 0:
        # process message

        now = datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        product_msg_list = [
            f'{idx}. {item.description}' for idx, item in enumerate(new_product_entity_list, start=1)]
        product_msg = "\n".join(product_msg_list)
        message = f'got these new products today at {formatted_now}:\n\nproducts:\n{product_msg}\n\nwebsite_url:\n{HERMES_BAGS_AND_SMALL_LEATHER_GOODS_URL}'

        email = environ.get("SENDER_EMAIL")
        password = environ.get("SENDER_PASSWORD")
        target = environ.get("TARGET_NAME")

        # send message to line notify
        print("start sending new product message")

        # todo: error handling
        body = {
            "email": email,
            "password": password
        }

        token_resonpse = requests.post(LOGIN_URL, json=body)
        token_resonpse_result = token_resonpse.json()

        access_token = token_resonpse_result["access_token"]

        token_params = f'Bearer {access_token}'
        body = {
            "message": message,
            "target": target
        }

        message_resonpse = requests.post(
            MESSAGE_URL, headers={'Authorization': token_params}, json=body)
        message_resonpse_result = message_resonpse.json()

        print(f"send message result: {message_resonpse_result}")

        if message_resonpse_result["isSuccess"] == True:
            for item in new_product_entity_list:
                item.notify_counts = item.notify_counts+1
            session.commit()

    print('done checking product item')

# upsert_product_job()
# check_latest_products()

# def test():
#     latest_product_info_list = collect_product(
#         HERMES_BAGS_AND_SMALL_LEATHER_GOODS_URL)
#     print(latest_product_info_list)

# test()




formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"start products web crawler job at {formatted_now}")

schedule.every(1).minutes.do(upsert_product_job)
schedule.every(30).seconds.do(check_latest_products)


while True:
    schedule.run_pending()
    time.sleep(1)
