#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2020 Cezar H. <https://github.com/usernein>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import pyrogram
from typing import Union
from functools import partial

from pyrogram import types
from pyrogram.filters import Filter


class WaitForMessage:
    async def wait_for_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        filters: Filter = None,
        timeout: int = None,
    ) -> "types.Message":
        """Wait for message.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            filters (:obj:`Filters`):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your callback function.

            timeout (``int``, *optional*):
                Timeout in seconds.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the reply message is returned.

        Raises:
            asyncio.TimeoutError: In case message not received within the timeout.

        Example:
            .. code-block:: python

                # Simple example
                reply_message = app.wait_for_message(chat_id)

                # Example with filter
                reply_message = app.wait_for_message(chat_id, filters=filters.text)

                # Example with timeout
                reply_message = app.wait_for_message(chat_id, timeout=60)
        """

        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        conversation_handler = self.dispatcher.conversation_handler
        future = self.loop.create_future()
        future.add_done_callback(partial(conversation_handler.delete_waiter, chat_id))
        waiter = dict(future=future, filters=filters, update_type=types.Message)
        conversation_handler.waiters[chat_id] = waiter
        return await asyncio.wait_for(future, timeout=timeout)
