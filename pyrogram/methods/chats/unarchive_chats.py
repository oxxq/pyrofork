#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import Union, List

import pyrogram
from pyrogram import raw


class UnarchiveChats:
    async def unarchive_chats(
        self: "pyrogram.Client",
        chat_ids: Union[int, str, List[Union[int, str]]],
    ) -> bool:
        """Unarchive one or more chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_ids (``int`` | ``str`` | List[``int``, ``str``]):
                Unique identifier (int) or username (str) of the target chat.
                You can also pass a list of ids (int) or usernames (str).
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Unarchive chat
                await app.unarchive_chats(chat_id)

                # Unarchive multiple chats at once
                await app.unarchive_chats([chat_id1, chat_id2, chat_id3])
        """

        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = []

        for chat in chat_ids:
            folder_peers.append(
                raw.types.InputFolderPeer(
                    peer=await self.resolve_peer(chat), folder_id=0
                )
            )

        await self.invoke(
            raw.functions.folders.EditPeerFolders(folder_peers=folder_peers)
        )

        return True
