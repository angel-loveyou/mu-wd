from Process.Cache.admins import admins
from Process.main import call_py
from pyrogram import filters
from Process.decorators import authorized_users_only
from Process.filters import command, other_filters
from Process.queues import QUEUE, clear_queue
from Process.main import bot as Client
from Process.utils import skip_current_song, skip_item
from WOODcraft.config import BOT_USERNAME, GROUP_SUPPORT, IMG_3, UPDATES_CHANNEL, IMG_5
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from WOODcraft.inline import stream_markup

bttn = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ð Go Back", callback_data="cbmenu")]]
)


bcl = InlineKeyboardMarkup(
    [[InlineKeyboardButton("ð Close", callback_data="cls")]]
)


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "â Bot **reloaded correctly !**\nâ **Admin list** has **updated !**"
    )


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}", "vskip"]) & other_filters)
@authorized_users_only
async def skip(client, m: Message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="â¢ Má´É´á´", callback_data="cbmenu"
                ),
                InlineKeyboardButton(
                    text="â¢ CÊá´sá´", callback_data="cls"
                ),
            ]
        ]
    )

    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("â nothing is currently playing")
        elif op == 1:
            await m.reply("â __Queues__ **is empty.**\n\n**â¢ userbot leaving voice chat**")
        elif op == 2:
            await m.reply("ðï¸ **Clearing the Queues**\n\n**â¢ userbot leaving voice chat**")
        else:
            await m.reply_photo(
                photo=f"{IMG_3}",
                caption=f"â­ **Skipped to the next track.**\n\nð· **Name:** [{op[0]}]({op[1]})\nð­ **Chat:** `{chat_id}`\nð¡ **Status:** `Playing`\nð§ **Request by:** {m.from_user.mention()}",
                reply_markup=keyboard,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "ð **removed song from queue:**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#{x}** - {hm}"
            await m.reply(OP)


@Client.on_message(
    command(["stop", f"stop@{BOT_USERNAME}", "end", f"end@{BOT_USERNAME}", "vstop"])
    & other_filters
)
@authorized_users_only
async def stop(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("â The userbot has disconnected from the video chat.")
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **nothing is streaming**")


@Client.on_message(
    command(["pause", f"pause@{BOT_USERNAME}", "vpause"]) & other_filters
)
@authorized_users_only
async def pause(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                "â¸ **Track paused.**\n\nâ¢ **To resume the stream, use the**\nÂ» /resume command."
            )
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **nothing in streaming**")


@Client.on_message(
    command(["resume", f"resume@{BOT_USERNAME}", "vresume"]) & other_filters
)
@authorized_users_only
async def resume(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                "â¶ï¸ **Track resumed.**\n\nâ¢ **To pause the stream, use the**\nÂ» /pause command."
            )
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **nothing in streaming**")


@Client.on_message(
    command(["mute", f"mute@{BOT_USERNAME}", "vmute"]) & other_filters
)
@authorized_users_only
async def mute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await m.reply(
                "ð **Userbot muted.**\n\nâ¢ **To unmute the userbot, use the**\nÂ» /unmute command."
            )
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **nothing in streaming**")


@Client.on_message(
    command(["unmute", f"unmute@{BOT_USERNAME}", "vunmute"]) & other_filters
)
@authorized_users_only
async def unmute(client, m: Message):
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await m.reply(
                "ð **Userbot unmuted.**\n\nâ¢ **To mute the userbot, use the**\nÂ» /mute command."
            )
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **nothing in streaming**")


@Client.on_callback_query(filters.regex("cbpause"))
async def cbpause(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\nÂ» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await query.edit_message_text(
                "â¸ The Streaming Has Paused", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"ð« **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("â Nothing is currently Streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbresume"))
async def cbresume(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\nÂ» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await query.edit_message_text(
                "â¶ï¸ The Streaming has Resumed", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"ð« **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("â Nothing is currently Streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbstop"))
async def cbstop(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\nÂ» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await query.edit_message_text("â **This Streaming has Ended**", reply_markup=bcl)
        except Exception as e:
            await query.edit_message_text(f"ð« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("â Nothing is currently Streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbmute"))
async def cbmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("You're an Anonymous Admin !\n\nÂ» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ Only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.mute_stream(chat_id)
            await query.edit_message_text(
                "ð Userbot Succesfully Muted", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"ð« **Error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("â Nothing is currently Streaming", show_alert=True)


@Client.on_callback_query(filters.regex("cbunmute"))
async def cbunmute(_, query: CallbackQuery):
    if query.message.sender_chat:
        return await query.answer("you're an Anonymous Admin !\n\nÂ» revert back to user account from admin rights.")
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ only admin with manage voice chats permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.unmute_stream(chat_id)
            await query.edit_message_text(
                "ð userbot succesfully unmuted", reply_markup=bttn
            )
        except Exception as e:
            await query.edit_message_text(f"ð« **error:**\n\n`{e}`", reply_markup=bcl)
    else:
        await query.answer("â nothing is currently streaming", show_alert=True)


@Client.on_message(
    command(["volume", f"volume@{BOT_USERNAME}", "vol"]) & other_filters
)
@authorized_users_only
async def change_volume(client, m: Message):
    range = m.command[1]
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.change_volume_call(chat_id, volume=int(range))
            await m.reply(
                f"â **Volume set To** `{range}`%"
            )
        except Exception as e:
            await m.reply(f"ð« **error:**\n\n`{e}`")
    else:
        await m.reply("â **Nothing in Streaming**")

@Client.on_callback_query(filters.regex("cbskip"))
async def cbskip(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("ð¡ Only admin with manage video chat permission that can tap this button !", show_alert=True)
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    queue = await skip_current_song(chat_id)
    if queue == 0:
        await query.answer("â Nothing is Currently Playing", show_alert=True)
    elif queue == 1:
        await query.answer("Â» There's no more Music in Queue to Skip, Userbot leaving Video Chat.", show_alert=True)
    elif queue == 2:
        await query.answer("ðï¸ Clearing the **Queues**\n\nÂ» **Userbot** leaving Video Chat.", show_alert=True)
    else:
        await query.answer("goes to the next track, proccessing...")
        await query.message.delete()
        buttons = stream_markup(user_id)
        requester = f"[{query.from_user.first_name}](tg://user?id={query.from_user.id})"
        thumbnail = f"{IMG_5}"
        title = f"{queue[0]}"
        userid = query.from_user.id
        gcname = query.message.chat.title
        ctitle = await CHAT_TITLE(gcname)
        image = await thumb(thumbnail, title, userid, ctitle)
        await _.send_photo(
            chat_id,
            photo=image,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=f"â­ **Skipped** to the next track.\n\nð **Name:** [{queue[0]}]({queue[1]})\nð­ **Chat:** `{chat_id}`\nð§¸ **Request by:** {requester}",
        )
        remove_if_exists(image)
