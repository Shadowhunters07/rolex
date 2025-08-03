from pyrogram import Client as bot, filters
from main import LOGGER
import master.helper as helper
import shutil
import os
from master import process
import msg

@bot.on_message(filters.command("drm"))
async def drm_download(bot, m):
    temp_dir = os.path.join(os.getcwd(), "temp")
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        LOGGER.info("✅ Temp directory cleared successfully!")
    else:
        LOGGER.info("ℹ️ Temp directory not found. Skipping cleanup.")

    editable = await m.reply_text(
        '<b><i>Hi, I am a non-DRM Downloader Bot</i></b>\n'
        '<b><i>Send me your text file containing name with URL format (e.g., Name: Link)</i></b>'
    )

    input_file = await bot.listen(chat_id=m.chat.id)
    links, file_name = await helper.process_text_file_or_input(bot, input_file, m)

    if not links:
        await editable.delete()
        await bot.send_message(m.chat.id, msg.planMessage)
        return

    await editable.edit(f"🔗 Total links found: __{len(links)}__\n\nSend starting index (default is 1):")
    input0 = await bot.listen(chat_id=m.chat.id)
    raw_text = input0.text
    await input0.delete()

    await editable.edit("📦 Enter batch name or send /d to use filename:")
    input1 = await bot.listen(chat_id=m.chat.id)
    b_name = input1.text if input1.text != '/d' else file_name
    await input1.delete()

    quality_to_resolution = {
        240: "426x240",
        360: "640x360",
        400: "400x224",
        480: "854x480",
        540: "960x540",
        576: "1024x576",
        720: "1280x720",
        1080: "1920x1080"
    }

    await editable.edit("🖥️ Enter video resolution (240, 360, 400, 480, 540, 576, 720, 1080):")
    input2 = await bot.listen(chat_id=m.chat.id)
    try:
        quality = int(input2.text)
        selected_resolution = quality_to_resolution.get(quality)
        if not selected_resolution:
            await editable.edit("❌ Invalid resolution! Try one of: 240, 360, 400, 480, 540, 576, 720, 1080.")
            await input2.delete()
            return
    except ValueError:
        await editable.edit("❌ Please enter a **numeric** value for the resolution!")
        await input2.delete()
        return
    await input2.delete()

    await editable.edit(
        "<b><i>🎨 Enter credit for caption (e.g., Admin or Admin,Admin for caption and filename). "
        "Send /d for default.</i></b>"
    )
    input3 = await bot.listen(chat_id=m.chat.id)
    credit_input = input3.text.strip()
    credit = "Admin"
    FileNameCredit = ""
    if credit_input != "/d":
        if "," in credit_input:
            credit, FileNameCredit = credit_input.split(",", 1)
        else:
            credit = credit_input
    await input3.delete()

    await editable.edit(
        "<b><i>🖼️ Send Thumbnail URL (e.g., https://...jpg), or send text (e.g., Admin) for watermark. "
        "Send /d for default.</i></b>", disable_web_page_preview=True
    )
    input6 = await bot.listen(chat_id=m.chat.id)
    thumb_input = input6.text.strip()
    thumb = ""
    watermark = None
    if thumb_input != "/d":
        if "," in thumb_input:
            thumb, watermark = thumb_input.split(",", 1)
        else:
            thumb = thumb_input
    await input6.delete()

    await editable.edit(
        "<b><i>📢 Provide Channel ID or send /d to upload here.\n\n"
        "🔹 Make me an admin to upload.\n🔸 Send /id in your channel to get the Channel ID.</i></b>"
    )
    input7 = await bot.listen(chat_id=m.chat.id)
    channel_id = m.chat.id if input7.text == "/d" else input7.text.strip()
    await input7.delete()

    if str(channel_id) == str(m.chat.id):
        await editable.delete()
    else:
        await editable.edit(
            f"<b><i>🎯 Target Batch: {b_name}</i></b>\n\n"
            "⏳ Task is being processed. Check your set channel.\n"
            "✅ You will be notified once completed."
        )

    try:
        await bot.send_message(chat_id=channel_id, text=f"<b><i>🎯 Target Batch - {b_name}</i></b>")
    except Exception as e:
        await m.reply_text(f"<b><i>❌ Failed to send message to channel:\n\n{e}</i></b>")
        return

    await process.process(
        bot=bot,
        message=m,
        links=links,
        raw_text=raw_text,
        channel_id=channel_id,
        b_name=b_name,
        credit=credit,
        FileNameCredit=FileNameCredit,
        selected_resolution=selected_resolution,
        thumb=thumb,
        watermark=watermark,
        editable=editable,
        quality=quality
    )
