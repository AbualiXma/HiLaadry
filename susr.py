from asyncio import create_task, sleep

from pyrogram import Client, filters

api_id = "25939451"  
api_hash = "243853dc20929b33d40435f2606ad50e"

app = Client(
    "Abuali",
    api_id=api_id,
    api_hash=api_hash
)

loop_chats = []


async def loop_message_in_time(client, message, time, num):
    num2 = 0
    while True:
        if num2 >= num or message.chat.id not in loop_chats:
            try:
                loop_chats.remove(message.chat.id)
            except:
                pass
            try:
                await client.send_message('me',
                                          f"تم انهاء التكرار في المجموعه {message.chat.id} \nرساله التكرار : https://t.me/{str(message.chat.id).replace('-100', '')}/{message.id} \nالوقت : {num} ثواني")
            except Exception as e:
                print(e)
            break
        else:
            try:
                await message.copy(message.chat.id)
            except Exception as e:
                print(e)
            num2 += 1
            await sleep(time)


@app.on_message(filters.me & filters.command('ن', '.'))
async def loop_message_cmd(client, message):
    if len(message.text.split(' ')) != 3 or not message.reply_to_message:
        return await message.reply('الأمر غير صحيح\nمثال على الأمر:\n`.ن {كل كام ثانية} {العدد}` (مع الرد على الرسالة)')
    try:
        if message.chat.id not in loop_chats:
            loop_chats.append(message.chat.id)
            create_task(
                loop_message_in_time(client, message.reply_to_message, int(message.text.split(' ')[1]),
                                     int(message.text.split(' ')[2])))
        else:
            return await message.reply('هناك نشر يعمل بالفعل يجب إيقافه أولاً')
    except Exception as e:
        print(e)
    await message.reply('تم ')


@app.on_message(filters.me & filters.command('ايقاف', '.'))
async def end_loop_message_cmd(client, message):
    if message.chat.id in loop_chats:
        loop_chats.remove(message.chat.id)
        await message.edit('تم طلب إيقاف التكرار\nعند توقف التكرار ستصلك رسالة في الرسائل المحفوظة')
    else:
        await message.edit('لا يوجد نشر يعمل هنا')

if __name__ == "__main__":
    app.run()
