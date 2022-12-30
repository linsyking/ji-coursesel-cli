from jaccount_cli import JaccountCLIAsyncIO
from getpass import getpass


class JaccountCLILogin(JaccountCLIAsyncIO):
    async def login(self, enable_mask=True, i_username = None, i_password = None):
        await self.init()
        captcha_ascii = self.captcha_generate_ascii()
        print("", captcha_ascii, "", sep="\n")
        captcha = input("Please enter the shown captcha: ")
        if i_username:
            username = i_username
        else:
            username = input("Please enter jaccount username: ")
        if i_password:
            password = i_password
        else:
            if enable_mask:
                password = getpass("Please enter password: ")
            else:
                password = input("Please enter password: ")
        await super().login(username, password, captcha)
