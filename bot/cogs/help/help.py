import typing as t

import nextcord
from nextcord import Embed
from nextcord.ext import commands

from bot.config import Config
from bot.views.help import HelpView


class HelpCommand(commands.MinimalHelpCommand):
    def get_command_signature(self, command):
        return f'`{self.context.clean_prefix}{command.qualified_name}` {command.signature}'

    async def _cog_select_options(self) -> t.List[nextcord.SelectOption]:
        options: t.List[nextcord.SelectOption] = []
        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort=True)
            if not filtered:
                continue
            emoji = getattr(cog, "COG_EMOJI", None)
            options.append(nextcord.SelectOption(
                label=cog.qualified_name if cog else 'No Category',
                emoji=emoji,
                description=cog.description[:Config.max_desk_len] if cog and cog.description else None
            ))
        return options

    async def _help_embed(self, title: str,
                          description: t.Optional[str] = None,
                          mapping: t.Optional[dict] = None,
                          command_set: t.Optional[t.Union[
                              t.List[commands.Command], t.Set[commands.Command]
                          ]] = None) -> Embed:
        embed = Embed(title=title, description=description)
        avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
        embed.set_author(name=self.context.bot.user.name, icon_url=avatar)
        if command_set:
            # show help about all commands in the set
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.help,
                    inline=False
                )
        elif mapping:
            # add a short description of commands in each cog
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else 'No Category'
                cmd_list = '\n'.join(
                    f'`{self.context.clean_prefix}{cmd.name}`' for cmd in filtered
                )
                value = (
                    f'{cog.description}\n{cmd_list}'
                    if cog and cog.description else cmd_list
                )
                embed.add_field(name=name, value=value)
        return embed

    async def bot_help_embed(self, mapping: dict) -> Embed:
        return await self._help_embed(
            title='All Commands',
            description=self.context.bot.description,
            mapping=mapping
        )

    async def cog_help_embed(self, cog: commands.Cog) -> Embed:
        return await self._help_embed(
            title=cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )

    async def send_bot_help(self, mapping: dict):
        await self.context.message.delete()
        embed = await self.bot_help_embed(mapping)
        options = await self._cog_select_options()
        await self.get_destination().send(
            embed=embed,
            view=HelpView(self, options)
        )

    async def send_command_help(self, command: t.Union[commands.Command, commands.Group]):
        await self.context.message.delete()
        embed = await self._help_embed(
            title=command.qualified_name,
            description=command.help,
            command_set=command.commands if isinstance(command, commands.Group) else None
        )
        await self.get_destination().send(
            embed=embed,
            delete_after=120
        )

    async def send_group_help(self, group: commands.Group):
        await self.send_command_help(group)

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(
            embed=embed,
            delete_after=120
        )
