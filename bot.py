from constants import constants
from datetime import datetime
import time
import requests
import randomheaders
import telebot
from telebot.types import InputMediaPhoto
from tqdm import tqdm


def get_direct_link_and_top(hash_id):
    r = requests.get("https://www.sreality.cz/api/en/v2/estates/{}".format(hash_id))
    r = r.json()

    locality = r['seo']['locality']
    category = constants['category_sub_cb'][r['seo']['category_sub_cb']]
    main_type = constants['category_main_cb_detail'][r['seo']['category_main_cb']]
    is_topped = r['is_topped']

    link = "https://www.sreality.cz/en/detail/lease/{main_type}/{category}/{locality}/{hash_id}#img=0&fullscreen=false".format(
        main_type=main_type,
        category=category,
        locality=locality,
        hash_id=hash_id
    )
    return link, is_topped


def main():
    bot = telebot.TeleBot("YOUR_BOT_API_TOKEN",
                          parse_mode=None)  # You can set parse_mode by default. HTML or MARKDOWN
    chat_id = 0  # YOUR CHAT ID
    api_link = """https://www.sreality.cz/api/en/v2/estates?category_main_cb=1&category_sub_cb=4%7C5%7C6%7C7&category_type_cb=2&czk_price_summary_order2=10000%7C24000&estate_age=2&floor_number=2%7C100&locality_district_id=5005%7C5010%7C5004%7C5003%7C5002%7C5001&locality_region_id=10&per_page=60&tms=1638903072136&usable_area=60%7C10000000000"""

    open("log.txt", "a").write("{} started\n".format(str(datetime.now())[:19]))
    header = randomheaders.LoadHeader()

    open("already_sent.txt", "a").write("")
    alreay_sent_ids = open("already_sent.txt", "r").read().split()
    alreay_sent_ids = list(filter(lambda x: x.strip() != '', alreay_sent_ids))
    alreay_sent_ids = list(map(lambda x: int(x.strip()), alreay_sent_ids))

    q = requests.get(api_link,
                     "",
                     headers=header)

    q = q.json()
    q = q['_embedded']['estates']

    flats_ids = list(map(lambda x: x['hash_id'], q))
    flats_ids = list(map(int, flats_ids))

    flats_photos = list(map(lambda x: x['_links']['images'], q))

    for enum, (i, images) in enumerate(tqdm(zip(flats_ids, flats_photos))):
        if i not in alreay_sent_ids:
            try:
                alreay_sent_ids.append(i)
                alreay_sent_ids_str = "\n".join(list(map(str, alreay_sent_ids)))
                open("already_sent.txt", "w").write(alreay_sent_ids_str)

                direct_link, is_top = get_direct_link_and_top(i)
                if is_top and enum < 2:
                    continue
                bot.send_message(
                    chat_id,
                    direct_link,
                    disable_web_page_preview=False
                )

                images_to_send = []
                for image_url in images:
                    image_content = requests.get(image_url['href'], allow_redirects=True, headers=header).content
                    images_to_send.append(InputMediaPhoto(image_content))

                bot.send_media_group(chat_id, images_to_send[:4], disable_notification=True)
                time.sleep(2)
            except Exception as e:
                print(e)

    open("log.txt", "a").write("{} finished\n\n".format(str(datetime.now())[:19]))


if __name__ == "__main__":
    main()
