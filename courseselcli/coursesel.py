from courseselcli.login import JaccountCLILogin


async def get_coursesel_jsid(enable_mask: bool,  i_username = None, i_password = None):
    async with JaccountCLILogin("https://coursesel.umji.sjtu.edu.cn/") as cli:
        await cli.login(enable_mask, i_username, i_password)
        cookies = cli.get_cookies()
        return cookies["JSESSIONID"].value
