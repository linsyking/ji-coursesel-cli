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
    print("Getting your JSESSIONID...")
    try:
        res = asyncio.run(coursesel.get_coursesel_jsid(True))
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
        get_jsession()
        return get_conf()

@app.command()
def update(use_realtime: bool = typer.Option(
        False, "--realtime", "-r", help="Use realtime request instead of preview request.")):
    """
    Update courses from server.
    """
    js = get_jsession()
    from courseselcli.elector import JIEelector
    elector = JIEelector(js, use_realtime)
    try:
        elector.run_save()
    except:
        get_jsession(True)
        update(use_realtime)

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
    except:
        get_jsession(True)
        autoadd(use_realtime)

@app.command()
def search(keyword: str = typer.Argument(..., help="Keyword to search.")):
    """
    Pull electurns and courses from server.
    """
    from courseselcli.elector import JIEelector
    js = get_jsession()
    elector = JIEelector(js)
    try:
        elector.search_courses(keyword)
    except:
        get_jsession(True)
        search(keyword)

@app.command()
def elect(jsessionID: str = typer.Option(None, "--jsessionID", "-j", help="Your JSESSIONID"),
          electTurnID: str = typer.Option(None, "--electTurnID", "-e"),
          ElectTurnLessonTaskID: str = typer.Option(None, "--electTurnLessonTaskID", "-l",
                                                    help="List of all courses you want to select, separated by comma (,)."),
          thread_number: int = typer.Option(10, "--thread", "-x",
                                            help="Number of threads to use for each course."),
          max_try: int = typer.Option(None, "--max-try", "-m",
                                      help="Maximum number of requests to send for each course. If not set, will try forever.")
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
            electTurnID = config['electTurnId']
            courses_eid = []
            for l in config['courses']:
                courses_eid.append(l['electTurnLessonTaskId'])
            ElectTurnLessonTaskID = ','.join(courses_eid)
        except:
            raise RuntimeError("Invalid coursesel.json file, please update first.")
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
        ','), thread_number, max_try)
    my_elector.run()


if __name__ == "__main__":
    app()
