import pokepy
import requests

from twitchio.ext import commands


class pokemon_cog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    pokemonClient = pokepy.V2Client(cache="in_disk", cache_location="./cache")

    async def event_ready(self):
        print(f"{self.bot.nick} is online!")

    @commands.command(name="type")
    async def types2(self, ctx, *, msg) -> None:
        pokemon = [pokepy.V2Client().get_pokemon(msg.lower())]
        pokemon_type = ""
        for x in range(len(pokemon[0].types)):
            pokemon_type += pokemon[0].types[x].type.name
            pokemon_type += " "
        await ctx.channel.send(str(pokemon_type))
        # return list(pokemon_type)

    @commands.command(name="weak")
    async def ww(self, ctx, *, msg) -> None:
        if " " in msg:
            msg = msg.replace(" ", "-")
        typings = ""
        damage = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}
        pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
        # print(pokemon)
        if pokemon:
            pokemon_type = []
            for x in range(len(pokemon[0].types)):
                pokemon_type.append(pokemon[0].types[x].type.name)
            for j in range(len(pokemon_type)):
                # print(pokemon_type[j])
                typings += pokemon_type[j]
                typings += " "
                # print(typings)

            if len(pokemon_type) != 0:
                pass
                # await ctx.channel.send(pokemon[0].name + ' is: ' + str(pokemon_type) + ' and is weak to: ')
            else:
                pokemon_type = msg.split()
                # print(str(pokemon_type))
        x = 1
        loop = 0
        if pokemon_type:
            for typing in pokemon_type:

                g = 0
                # print('loop')
                response = requests.get(f"https://pokeapi.co/api/v2/type/{typing}")
                fetch = response.json()
                # print(typing)
                for effect, types in fetch["damage_relations"].items():
                    if x % 2 != 0:
                        if loop == 0:
                            g += 1
                        test2 = [type["name"] for type in types]
                        # print(test2)
                        if g == 1:
                            for fetch_weak in test2:
                                damage["2x"].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                damage["0.5x"].append(fetch_weak)

                        if g == 3:
                            for fetch_weak in test2:
                                damage["0x"].append(fetch_weak)

                        if loop == 1:
                            g += 1
                            if g == 1:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["4x"].append(fetch_weak)
                                    if fetch_weak not in damage["2x"]:
                                        damage["2x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        damage["2x"].remove(fetch_weak)
                                    if fetch_weak in damage["0.5x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["1x"].append(fetch_weak)

                            if g == 2:
                                for fetch_weak in test2:
                                    print(fetch_weak)
                                    if fetch_weak not in damage["0.5x"]:
                                        damage["0.5x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["0.5x"]:
                                            damage["0.5x"].remove(fetch_weak)
                                    if fetch_weak in damage["2x"]:
                                        print(fetch_weak + "in 2x")
                                        damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)

                                        print(damage["2x"])

                            if g == 3:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["4x"]:
                                        damage["4x"].remove(fetch_weak)
                                    elif fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)

                    x += 1
                loop += 1

        for type in damage["0x"]:
            for type in damage["0x"]:
                if type in damage["2x"]:
                    damage["2x"].remove(type)
            if type in damage["4x"]:
                damage["4x"].remove(type)
        for type in damage["2x"]:
            if type in damage["4x"]:
                damage["2x"].remove(type)

        message1 = ""
        message2 = ""
        if damage["4x"]:
            message1 = ", ".join(damage["4x"])
            # for x in range(len(damage['4x'])):
            #     message += damage['4x'][x]
        if damage["2x"]:
            message2 = ", ".join(damage["2x"])

        if message1:
            await ctx.channel.send(
                pokemon[0].name
                + " is: "
                + typings
                + " takes 4x: "
                + message1
                + "; 2x: "
                + message2
            )
            return
        await ctx.channel.send(
            pokemon[0].name + " is: " + typings + " takes 2x: " + message2
        )

    @commands.command(name="w")
    async def weak_type(self, ctx, *, msg) -> None:
        damage = {"4x": [], "2x": [], "1x": [], "0.5x": [], "0.25x": [], "0x": []}
        pokemon_type = msg.split()
        x = 1
        loop = 0
        if pokemon_type:
            for typing in pokemon_type:

                g = 0
                # print('loop')
                response = requests.get(f"https://pokeapi.co/api/v2/type/{typing}")
                fetch = response.json()
                # print(typing)
                for effect, types in fetch["damage_relations"].items():
                    if x % 2 != 0:
                        if loop == 0:
                            g += 1
                        test2 = [type["name"] for type in types]
                        # print(test2)
                        if g == 1:
                            for fetch_weak in test2:
                                damage["2x"].append(fetch_weak)

                        if g == 2:
                            for fetch_weak in test2:
                                damage["0.5x"].append(fetch_weak)

                        if g == 3:
                            for fetch_weak in test2:
                                damage["0x"].append(fetch_weak)

                        if loop == 1:
                            g += 1
                            if g == 1:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["4x"].append(fetch_weak)
                                    if fetch_weak not in damage["2x"]:
                                        damage["2x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        damage["2x"].remove(fetch_weak)
                                    if fetch_weak in damage["0.5x"]:
                                        damage["2x"].remove(fetch_weak)
                                        damage["1x"].append(fetch_weak)

                            if g == 2:
                                for fetch_weak in test2:
                                    print(fetch_weak)
                                    if fetch_weak not in damage["0.5x"]:
                                        damage["0.5x"].append(fetch_weak)
                                    if fetch_weak in damage["0x"]:
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["0.5x"]:
                                            damage["0.5x"].remove(fetch_weak)
                                    if fetch_weak in damage["2x"]:
                                        print(fetch_weak + "in 2x")
                                        damage["2x"].remove(fetch_weak)
                                        if fetch_weak in damage["2x"]:
                                            damage["2x"].remove(fetch_weak)

                                        print(damage["2x"])

                            if g == 3:
                                for fetch_weak in test2:
                                    if fetch_weak in damage["4x"]:
                                        damage["4x"].remove(fetch_weak)
                                    elif fetch_weak in damage["2x"]:
                                        damage["2x"].remove(fetch_weak)

                    x += 1
                loop += 1

        for type in damage["0x"]:
            for type in damage["0x"]:
                if type in damage["2x"]:
                    damage["2x"].remove(type)
            if type in damage["4x"]:
                damage["4x"].remove(type)
        for type in damage["2x"]:
            if type in damage["4x"]:
                damage["2x"].remove(type)

        message = ""
        if damage["4x"]:
            message += "4x: " + str(damage["4x"])
            # for x in range(len(damage['4x'])):
            #     message += damage['4x'][x]
        if damage["2x"]:
            message += " 2x: " + str(damage["2x"])

        await ctx.channel.send(str(message))

    @commands.command(name="trigger")
    async def trigger(self, ctx, *, msg) -> None:
        if msg.isnumeric() is True:
            pokemon_id = msg
        elif msg.isnumeric() is False:
            pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
            pokemon_id = pokemon[0].id
            print(pokemon, pokemon_id)
        pokemon = [self.pokemonClient.get_pokemon(msg.lower())]
        # print(pokemon_id)
        id = [self.pokemonClient.get_pokemon_species(pokemon_id)]
        pokemon_species_id = id[0].evolution_chain.url
        pokemon_evolution_id = pokemon_species_id.split("/")[-2]
        print(pokemon_evolution_id)
        pokemon_evolution = [
            self.pokemonClient.get_evolution_chain(pokemon_evolution_id)
        ]
        # print(str(pokemon_species_id) + " chain")
        # print(pokemon_evolution_id)
        # pokemon_trigger = pokemon_evolution[0].chain.evolves_to[0].evolution_details[0].trigger.name
        # print(pokemon_trigger)
        # pokemon_evolution_details = pokemon_evolution[0].chain.evolves_to[0].evolution_details
        pokemon_name1 = pokemon_evolution[0].chain.species.name
        pokemon_name2 = pokemon_evolution[0].chain.evolves_to[0].species.name
        try:
            pokemon_name3 = (
                pokemon_evolution[0].chain.evolves_to[0].evolves_to[0].species.name
            )
        except IndexError:
            pokemon_name3 = None
        # print(msg)
        # print(pokemon[0].name)
        # print(pokemon_name1 + "1st evolution")
        # print(pokemon_name2 + "2nd evolution")
        pokemon_message = " "
        names = ""
        if pokemon[0].name == pokemon_name1:
            evolution_details = (
                pokemon_evolution[0].chain.evolves_to[0].evolution_details[0]
            )
            names += pokemon[0].name + " -> " + pokemon_name2 + "; "
        elif pokemon[0].name == pokemon_name2:
            evolution_details = (
                pokemon_evolution[0]
                .chain.evolves_to[0]
                .evolves_to[0]
                .evolution_details[0]
            )
            names += pokemon[0].name + " -> " + pokemon_name3 + "; "
        elif pokemon[0].name == pokemon_name3:
            await ctx.channel.send(f"{pokemon[0].name} doesn't evolve AFAIK :3")
        else:
            evolution_details = (
                pokemon_evolution[0]
                .chain.evolves_to[0]
                .evolves_to[0]
                .evolution_details[0]
            )
        trigger_level = evolution_details.min_level
        trigger_affection = evolution_details.min_affection
        trigger_time = evolution_details.time_of_day
        trigger_trade = evolution_details.trade_species
        trigger_move = evolution_details.known_move
        trigger_move_type = evolution_details.known_move_type
        trigger_item = evolution_details.item
        trigger_held_item = evolution_details.held_item
        trigger_happiness = evolution_details.min_happiness

        if trigger_happiness is not None:
            pokemon_message += "Min happiness: " + str(trigger_happiness)
        if trigger_level is not None:
            pokemon_message += "Min level: " + str(trigger_level)
        if trigger_affection is not None:
            pokemon_message += "Min affection: " + str(trigger_affection)
        if trigger_time != "":
            pokemon_message += "Time of the day: " + str(trigger_time)
        if trigger_trade is not None:
            pokemon_message += "Needs to be traded!"
        if trigger_move is not None:
            pokemon_message += "Needs to know a move:   " + str(trigger_move).replace(
                "<Named_API_Resource |", ""
            ).replace(">", "")
        if trigger_move_type is not None:
            pokemon_message += "Needs to know a move of type: " + str(trigger_move_type)
        if trigger_item is not None:
            pokemon_message += "Needs an item to evolve: " + str(trigger_item.name)
        if trigger_held_item is not None:
            pokemon_message += "Needs to hold item to evolve: " + str(trigger_held_item)

        if pokemon_message == " ":
            await ctx.channel.send(
                "Another evolution trigger that I have not accounted for yet, please bare with me :3"
            )
            return
        await ctx.channel.send(names + ": " + pokemon_message)

    @commands.command(name="move")
    async def move(self, ctx, *, msg) -> None:
        # ctx.channel.send(msg)
        if " " in msg:
            msg = msg.replace(" ", "-")
        # print(msg)
        move = [self.pokemonClient.get_move(msg)]
        type = str(move[0].type.name)
        damage_class = str(move[0].damage_class.name)
        power = str(move[0].power)
        pp = str(move[0].pp)
        priority = str(move[0].priority)
        accuracy = str(move[0].accuracy)
        effect_chance = str(move[0].effect_chance)
        effect_entries = str(move[0].effect_entries[0].effect).replace(
            " $effect_chance", " " + effect_chance
        )
        if (
                len(
                    type.capitalize()
                    + "; "
                    + damage_class.capitalize()
                    + " Power: "
                    + power
                    + " Accuracy: "
                    + accuracy
                    + " PP: "
                    + pp
                    + " Priority: "
                    + priority
                    + "  "
                    + effect_entries
                )
                >= 500
        ):
            await ctx.channel.send(
                type.capitalize()
                + "; "
                + damage_class.capitalize()
                + " Power: "
                + power
                + " PP: "
                + pp
                + " Priority: "
                + priority
                + "  "
            )
            if len(effect_entries) > 500:
                split_entries = effect_entries.split(".")
                len_split_entries = len(split_entries)
                first_half = ""
                second_half = ""
                for index in range(len_split_entries):
                    if index < len_split_entries // 2:
                        first_half += split_entries[index] + "."
                    else:
                        second_half += split_entries[index] + "."
                await ctx.channel.send(first_half)
                await ctx.channel.send(second_half)
                return
            await ctx.channel.send(effect_entries)
            return
        await ctx.channel.send(
            type.capitalize()
            + "; "
            + damage_class.capitalize()
            + " Power: "
            + power
            + " PP: "
            + pp
            + " Priority: "
            + priority
            + "  "
            + effect_entries
        )


def prepare(bot: commands.Bot):
    # Load our cog with this module...
    bot.add_cog(pokemon_cog(bot))
