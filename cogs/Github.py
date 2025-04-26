import disnake
from disnake.ext import commands

from utils.bot import Sico


class GitHub(commands.Cog):
    """Commands involving GitHub! :)"""

    def __init__(self, bot: Sico):
        self.bot = bot

    # Command to get information about a GitHub user
    @commands.slash_command(
        name="ghperson", description="Gets the Profile of the github person."
    )
    async def ghperson(self, inter, ghuser: str):
        person_raw = await self.bot.session.get(
            f"https://api.github.com/users/{ghuser}"
        )
        if person_raw.status != 200:
            return await inter.send("User not found!")
        else:
            person = await person_raw.json()
        # Returning an Embed containing all the information:
        embed = disnake.Embed(
            title=f"GitHub Profile: {person['login']}",
            description=f"**Bio:** {person['bio']}",
            color=0xFFFFFF,
        )
        embed.set_thumbnail(url=f"{person['avatar_url']}")
        embed.add_field(name="Username 📛: ", value=f"{person['name']}", inline=True)
        # embed.add_field(name="Email ✉: ", value=f"{person['email']}", inline=True) Commented due to GitHub not responding with the correct email
        embed.add_field(
            name="Repos 📁: ", value=f"{person['public_repos']}", inline=True
        )
        embed.add_field(
            name="Location 📍: ", value=f"{person['location']}", inline=True
        )
        embed.add_field(name="Company 🏢: ", value=f"{person['company']}", inline=True)
        embed.add_field(
            name="Followers 👥: ", value=f"{person['followers']}", inline=True
        )
        embed.add_field(name="Website 🖥️: ", value=f"{person['blog']}", inline=True)
        button = disnake.ui.Button(
            label="Link", style=disnake.ButtonStyle.url, url=person["html_url"]
        )
        await inter.send(embed=embed, components=button)

    # Command to get search for GitHub repositories:
    @commands.slash_command(
        name="ghsearchrepo", description="Searches for the specified repo."
    )
    async def ghsearchrepo(self, inter, query: str):
        pages = 1
        url = f"https://api.github.com/search/repositories?q={query}&{pages}"
        repos_raw = await self.bot.session.get(url)
        if repos_raw.status != 200:
            return await inter.send("Repo not found!")
        else:
            repos = await repos_raw.json()  # Getting first repository from the query
        repo = repos["items"][0]
        # Returning an Embed containing all the information:
        embed = disnake.Embed(
            title=f"GitHub Repository: {repo['name']}",
            description=f"**Description:** {repo['description']}",
            color=0xFFFFFF,
        )
        embed.set_thumbnail(url=f"{repo['owner']['avatar_url']}")
        embed.add_field(
            name="Author 🖊:",
            value=f"__[{repo['owner']['login']}]({repo['owner']['html_url']})__",
            inline=True,
        )
        embed.add_field(
            name="Stars ⭐:", value=f"{repo['stargazers_count']}", inline=True
        )
        embed.add_field(name="Forks 🍴:", value=f"{repo['forks_count']}", inline=True)
        embed.add_field(name="Language 💻:", value=f"{repo['language']}", inline=True)
        embed.add_field(
            name="Size 🗃️:",
            value=f"{round(repo['size'] / 1000, 2)} MB",
            inline=True,
        )
        if repo["license"]:
            spdx_id = repo["license"]["spdx_id"]
            embed.add_field(
                name="License name 📃:",
                value=f"{spdx_id if spdx_id != 'NOASSERTION' else repo['license']['name']}",
                inline=True,
            )
        else:
            embed.add_field(
                name="License name 📃:",
                value=f"This Repo doesn't have a license",
                inline=True,
            )
        button = disnake.ui.Button(
            label="Link", style=disnake.ButtonStyle.url, url=repo["html_url"]
        )
        await inter.send(embed=embed, components=button)


def setup(bot):
    bot.add_cog(GitHub(bot))
