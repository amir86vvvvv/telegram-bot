import asyncio
import random
import time
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import PeerChannel, ChatInviteExported


# ---------------- تنظیمات API ----------------
api_id = 24072095
api_hash = 'e528f7c3a9ea454963ad9beab9f6f6ea'


# ---------------- String Session ----------------
string = '1BJWap1wBuweCkG9wsh1U3aOrdq7wmOwY5gYqC_MXmFBy-jhf9UOgleHiKJJuLTLvBdubLO3AcZQJ3Eu7krkZeB1DU8-9DCd19dJj02MWtkKliF9szrrQ3G97697_3ZF67jmQnaxQnHOqKcv5iy84vnI6-uQLi5E5O72SKjCtQlGNT0Dop0-ENNxOb8JYFhJrSlY861-Hax8OD73myVmU9W9VJ49GnC5aOpGTNgAXDzNx0mh_kkDQfZ2qyEOmBQwtkOg42_3m8Poo5yLBCtsV0fkOn0U-cMCAROtFy_lWhc96SLv5ohxkD-2uEFoN6ey8Dty7MEsvq660qESmuYSq0QIh7jipxLk='


# ---------------- لینک‌ کانال‌ها ----------------
channel_ids = [
    2511974588,  # شماره کارت 1
    2319925957   # شماره کارت 2
]


# ---------------- پیام خوش‌آمدگویی و تبلیغات ----------------
welcome_message = (
    "سلام درود\n"
    "[https://t.me/soallat4](https://t.me/soallat4) کانال اصلی ما\n"
    "[https://t.me/soallat3](https://t.me/soallat3) کانال رضایت مشتری و اعتماد به ما\n"
    "این یک پیام از طرف ربات است. در اولین فرصت پاسخگوی شما خواهم بود.\n"
    "با تشکر از صبر شما.\n\n"
    "لیست قیمت‌ها:\n"
    "هزینه سوالات نهایی تمامی پایه ها بدونه پاسخ نامه با تخفیف ویژه 980 ت ✅\n"
    "هزینه سوالات نهایی تمامی پایه ها با پاسخ نامه 1 میلیون و 580 ✅\n"
    "هزینه سوالات کنکور 4 میلیون و 980 ت ✅\n"
    "خرید تمامی سوالات یک جا بدون پاسخ نامه با تخفیف ویژه 1 میلیون و 980 ✅\n"
    "خرید تمامی سوالات یک جا همراه پاسخ نامه با تخفیف ویژه 2 میلیون و 580 ✅\n"
    "تغییر نمرات سیستمی یک درس 980 ت✅\n"
    "تغییر نمرات سیستمی تمامی دروس تضمینی با تخفیف ویژه 1 میلیون و 980 ✅"
)


advertising_messages = [
    "فروش سوالات نهایی نهم ، یازدهم ، دوازدهم 100 درصد تضمینی ✅\nفروش سوالات کنکور ✅\nتغییرات نمرات سیستمی تمام دروس ✅\nفروش انواع سوالات کشوری و نهایی ✅\nانجام انواع خدمات هک و امنیت ✅\nاعتماد شما اعتبار ماست ✅",
    "سوالات نهایی و کنکور موجود است",
    "سوالات نهایی موجود است انجام انواع هک"
]


# ---------------- داده‌های کاربران ----------------
welcomed_users = set()
user_card_requests = {}
blocked_until = {}


# ---------------- اجرای کلاینت ----------------
client = TelegramClient(StringSession(string), api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def handle_user(event):
    if not event.is_private:
        return


    sender_id = event.sender_id
    text = event.raw_text.lower()


    # ارسال پیام خوش‌آمدگویی یک‌بار
    if sender_id not in welcomed_users:
        await event.respond(welcome_message)
        await asyncio.sleep(1)
        await event.respond("اگر قصد خرید دارید کلمه *شماره کارت* را ارسال کنید.\nاگر سوالی دارید بنویسید *وصل به پشتیبانی*.")
        welcomed_users.add(sender_id)
        return


    # درخواست پشتیبانی
    if "وصل به پشتیبانی" in text:
        await event.respond("لطفاً منتظر بمانید، در اولین فرصت ادمین‌ها پاسخگوی شما خواهند بود.")
        return


    # درخواست شماره کارت
    if "شماره کارت" in text:
        now = time.time()
        last_time = blocked_until.get(sender_id, 0)
        if now < last_time:
            remaining = int((last_time - now) / 60)
            await event.respond(f"شما به حد مجاز رسیدید. لطفاً بعد از {remaining} دقیقه دوباره تلاش کنید.")
            return


        count = user_card_requests.get(sender_id, 0)
        if count >= 2:
            blocked_until[sender_id] = now + 14400  # 4 ساعت
            await event.respond("شما به حد مجاز رسیدید. لطفاً بعد از 4 ساعت دوباره تلاش کنید.")
            return


        selected_id = random.choice(channel_ids)
        try:
            expire_timestamp = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
            invite: ChatInviteExported = await client(ExportChatInviteRequest(
                peer=PeerChannel(selected_id),
                expire_date=expire_timestamp,
                usage_limit=1
            ))
            link = invite.link
            await event.respond(f"برای دریافت شماره کارت وارد لینک زیر شوید. این لینک فقط ۱۰ دقیقه و یکبار قابل استفاده است:\n{link}")
            user_card_requests[sender_id] = count + 1
        except Exception as e:
            print(f"خطا در ساخت لینک زمان‌دار: {e}")
            await event.respond("خطا در ساخت لینک. لطفاً بعداً تلاش کنید.")


# ---------------- تبلیغات خودکار ----------------
async def auto_advertise():
    await client.start()
    print("ربات فعال شد. تبلیغات در حال ارسال...")
    while True:
        try:
            dialogs = await client.get_dialogs()
            groups = [d for d in dialogs if d.is_group]
            for group in groups:
                try:
                    msg = random.choice(advertising_messages)
                    await client.send_message(group.id, msg)
                    print(f"ارسال شد به {group.name}")
                except Exception as e:
                    print(f"خطا در {group.name}: {e}")
            wait = random.randint(60, 900)
            print(f"صبر {wait} ثانیه")
            await asyncio.sleep(wait)
        except Exception as e:
            print(f"خطای عمومی: {e}")
            await asyncio.sleep(60)


# ---------------- اجرای برنامه ----------------
with client:
    client.loop.run_until_complete(auto_advertise())
