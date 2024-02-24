import asyncio
import os
import re
import aiohttp

from github_stats import Stats

async def generate_overview(s: Stats) -> None:
    """
    Generate an SVG badge with summary statistics
    :param s: Represents user's GitHub statistics
    """
    with open("templates/overview.svg", "r") as f:
        output = f.read()
        output = re.sub("{{ name }}", await s.name, output)
        output = re.sub("{{ stars }}", f"{await s.stargazers:,}", output)
        output = re.sub("{{ forks }}", f"{await s.forks:,}", output)
        output = re.sub("{{ repos }}", f"{len(await s.repos):,}", output)

    with open("generated/overview.svg", "w") as f:
        f.write(output)

async def main() -> None:
    """
    Generate all badges
    """
    access_token = os.getenv("ACCESS_TOKEN")
    # from dotenv import dotenv_values
    # access_token = dotenv_values('.env')['ACCESS_TOKEN']
    if not access_token:
        raise Exception("A personal access token is required to proceed!")

    async with aiohttp.ClientSession() as session:
        s = Stats(
            'ngntrgduc',
            access_token,
            session,
        )
        await generate_overview(s)


if __name__ == "__main__":
    from time import perf_counter
    tic = perf_counter()
    asyncio.run(main())
    print(f'Took {perf_counter()-tic:.2f}s')
