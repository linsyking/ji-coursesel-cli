from courseselcli.login import JaccountCLILogin


async def get_coursesel_jsid(enable_mask: bool):
    async with JaccountCLILogin("https://coursesel.umji.sjtu.edu.cn/") as cli:
        await cli.login(enable_mask)
        cookies = cli.get_cookies()
        return cookies["JSESSIONID"].value
