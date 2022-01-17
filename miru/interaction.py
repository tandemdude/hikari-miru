from __future__ import annotations

import functools
import typing

import hikari
from hikari import undefined

if typing.TYPE_CHECKING:
    from hikari import embeds as embeds_
    from hikari import guilds
    from hikari import messages
    from hikari import snowflakes
    from hikari import users
    from hikari.api import special_endpoints


class Interaction(hikari.ComponentInteraction):
    """
    Represents a component interaction on Discord. Has additional short-hand methods for ease-of-use.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._issued_response: bool = False

    @classmethod
    def from_hikari(self, interaction: hikari.ComponentInteraction) -> Interaction:
        """
        Create a new Interaction object from a hikari.ComponentInteraction. This should be rarely used.
        """
        return Interaction(
            channel_id=interaction.channel_id,
            component_type=interaction.component_type,
            custom_id=interaction.custom_id,
            values=interaction.values,
            guild_id=interaction.guild_id,
            message=interaction.message,
            member=interaction.member,
            user=interaction.user,
            app=interaction.app,
            id=interaction.id,
            application_id=interaction.application_id,
            type=interaction.type,
            token=interaction.token,
            version=interaction.version,
        )

    @functools.wraps(hikari.ComponentInteraction.create_initial_response)
    async def create_initial_response(self, *args, **kwargs) -> None:
        await super().create_initial_response(*args, **kwargs)
        self._issued_response = True

    @functools.wraps(hikari.ComponentInteraction.execute)
    async def send_message(self, *args, **kwargs):
        """
        Short-hand method to send a message response to the interaction
        """
        if self._issued_response:
            await self.execute(*args, **kwargs)
        else:
            await self.create_initial_response(hikari.ResponseType.MESSAGE_CREATE, *args, **kwargs)

    async def defer(self, flags: typing.Union[int, messages.MessageFlag] = None):
        """
        Short-hand method to defer an interaction response. Raises RuntimeError if the interaction was already responded to.
        """

        if self._issued_response:
            raise RuntimeError("Interaction was already responded to.")

        await self.create_initial_response(hikari.ResponseType.DEFERRED_MESSAGE_UPDATE, flags=flags)
