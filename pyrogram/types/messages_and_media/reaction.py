#  PyroFork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of PyroFork.
#
#  PyroFork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  PyroFork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with PyroFork.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

import pyrogram
from pyrogram import enums, raw
from ..object import Object


class Reaction(Object):
    """Contains information about a reaction.

    Parameters:
        type (``enums.ReactionType``):
            Reaction type.

        emoji (``str``, *optional*):
            Reaction emoji.

        custom_emoji_id (``int``, *optional*):
            Custom emoji id.

        count (``int``, *optional*):
            Reaction count.

        chosen_order (``int``, *optional*):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "enums.ReactionType",
        emoji: Optional[str] = None,
        custom_emoji_id: Optional[int] = None,
        count: Optional[int] = None,
        chosen_order: Optional[int] = None,
    ):
        super().__init__(client)

        self.type = type
        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id
        self.count = count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(client: "pyrogram.Client", reaction: "raw.base.Reaction") -> "Reaction":
        if isinstance(reaction, raw.types.ReactionEmoji):
            return Reaction(
                client=client, type=enums.ReactionType.EMOJI, emoji=reaction.emoticon
            )

        if isinstance(reaction, raw.types.ReactionCustomEmoji):
            return Reaction(
                client=client,
                type=enums.ReactionType.CUSTOM_EMOJI,
                custom_emoji_id=reaction.document_id,
            )
        if isinstance(reaction, raw.types.ReactionPaid):
            return Reaction(client=client, type=enums.ReactionType.PAID)

    @staticmethod
    def _parse_count(
        client: "pyrogram.Client", reaction_count: "raw.base.ReactionCount"
    ) -> "Reaction":
        reaction = Reaction._parse(client, reaction_count.reaction)
        reaction.count = reaction_count.count
        reaction.chosen_order = reaction_count.chosen_order

        return reaction
