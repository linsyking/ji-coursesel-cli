#!/usr/bin/env python3
'''
@Author: King
@Date: 2022-12-23 23:46:21
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import typer
import json

app = typer.Typer(add_completion=False)


def get_jsession(force_update=False):
    import os.path
    obj = {}
    if os.path.exists("coursesel.json"):
        with open("coursesel.json", "r") as f:
            obj = json.load(f)
        if "jsessionID" in obj and not force_update:
            return obj["jsessionID"]
    import courseselcli.coursesel as coursesel
    import asyncio

    username = None
    password = None
    if "username" in obj:
        username = obj["username"]

    if "password" in obj:
        password = obj["password"]

    print("Getting your JSESSIONID...")
    try:
        res = asyncio.run(coursesel.get_coursesel_jsid(
            True, username, password))
    except Exception:
        raise RuntimeError("Failed to get JSESSIONID")
    obj["jsessionID"] = res
    with open("coursesel.json", "w") as f:
        f.write(json.dumps(obj, indent=4, ensure_ascii=False))
    return res


def get_conf():
    import os.path
    obj = {}
    if os.path.exists("coursesel.json"):
        with open("coursesel.json", "r") as f:
            obj = json.load(f)
        return obj
    else:
        raise RuntimeError(
            "Configuration file not found, please first run `auth` command.")


@app.command()
def auth(save_username: bool = typer.Option(True, prompt=True),
         save_password: bool = typer.Option(True, prompt=True),
         username: str = typer.Option(..., prompt=True),
         password: str = typer.Option(..., prompt=True, hide_input=True)
         ):
    """
    Auth username and password.
    """
    import os.path

    import courseselcli.coursesel as coursesel
    import asyncio
    obj = {}
    if os.path.exists("coursesel.json"):
        with open("coursesel.json", "r") as f:
            obj = json.load(f)
    if save_username:
        obj["username"] = username
    if save_password:
        obj["password"] = password
    try:
        res = asyncio.run(coursesel.get_coursesel_jsid(
            True, username, password))
    except Exception:
        raise RuntimeError("Failed to get JSESSIONID")
    obj["jsessionID"] = res

    with open("coursesel.json", "w") as f:
        f.write(json.dumps(obj, indent=4, ensure_ascii=False))
    return res


@app.command()
def autoadd(use_realtime: bool = typer.Option(
        False, "--realtime", "-r", help="Use realtime request instead of preview request.")):
    """
    Auto add courses.
    """
    js = get_jsession()
    from courseselcli.elector import JIEelector
    elector = JIEelector(js, use_realtime)
    try:
        elector.run()
    except KeyboardInterrupt:
        return
    except:
        get_jsession(True)
        autoadd(use_realtime)


@app.command()
def refresh():
    """
    Refresh JSESSIONID in current configuration file.
    """
    get_jsession(True)
    print("Done.")


@app.command()
def search(keyword: str = typer.Argument(..., help="Keyword to search.")):
    """
    Search courses.
    """
    from courseselcli.elector import JIEelector
    js = get_jsession()
    elector = JIEelector(js)
    try:
        elector.search_courses(keyword)
    except KeyboardInterrupt:
        return
    except:
        get_jsession(True)
        search(keyword)


@app.command()
def elect(jsessionID: str = typer.Option(None, "--jsessionID", "-j", help="Your JSESSIONID"),
          electTurnID: str = typer.Option(None, "--electTurnID", "-e"),
          ElectTurnLessonTaskID: str = typer.Option(None, "--electTurnLessonTaskID", "-l",
                                                    help="List of all courses you want to select, separated by comma (,)."),
          CoursesDesc: str = typer.Option(None, "--coursesDesc",
                                          help="List of all course description you want to select, separated by comma (,)."),
          thread_number: int = typer.Option(3, "--thread", "-x",
                                            help="Number of threads to use for each course."),
          max_try: int = typer.Option(None, "--max-try", "-m",
                                      help="Maximum number of requests to send for all course. If not set, will try forever."),
          demo: bool = typer.Option(
              False, "--demo", help="Do a demonstration.")
          ):
    """
    Elect courses.
    """
    import os
    if os.path.exists('coursesel.json'):
        # Use this file to initialize
        with open('coursesel.json', 'r') as f:
            config = json.load(f)
        try:
            jsessionID = config['jsessionID']
            if demo:
                electTurnID = "demo"
                ElectTurnLessonTaskID = "test1,test2,test3,test4,test5"
                CoursesDesc = "test1,test2,test3,test4,test5"
            else:
                electTurnID = config['electTurnId']
                courses_eid = []
                courses_code = []
                for l in config['courses']:
                    courses_eid.append(l['electTurnLessonTaskId'])
                    courses_code.append(l['lessonClassCode'])
                ElectTurnLessonTaskID = ','.join(courses_eid)
                CoursesDesc = ','.join(courses_code)
        except:
            raise RuntimeError(
                "Invalid coursesel.json file, please add courses first.")
    if jsessionID is None:
        print("Please specify JSESSIONID")
        return
    if electTurnID is None:
        print("Please specify electTurnID")
        return
    if ElectTurnLessonTaskID is None:
        print("Please specify ElectTurnLessonTaskID")
        return
    JSESSIONID = jsessionID
    from courseselcli.single import ElectSingle

    my_elector = ElectSingle(JSESSIONID, electTurnID, ElectTurnLessonTaskID.split(
        ','), thread_number, max_try, CoursesDesc.split(','))
    my_elector.run()

if __name__ == "__main__":
    app()
