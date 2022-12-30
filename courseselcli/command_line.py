from courseselcli.main import app

def main():
    try:
        app()
    except Exception as e:
        print(e)
