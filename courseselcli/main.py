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


def get_jsession():
    import courseselcli.coursesel as coursesel
    import asyncio
    print("Getting your JSESSIONID...")
    try:
        res = asyncio.run(coursesel.get_coursesel_jsid(True))
    except Exception:
        print("Failed to get JSESSIONID, please try again.")
        return
    return res


@app.command()
def init(use_realtime: bool = typer.Option(
        False, "--realtime", "-r", help="Use realtime request instead of preview request.")):
    """
    Initialize course elector
    """
    js = get_jsession()
    from courseselcli.elector import JIEelector
    elector = JIEelector(js, use_realtime)
    elector.run()
    print("Done. Please use command 'elect' to start electing.")


@app.command()
def refresh():
    """
    Refresh JSESSIONID in current configuration file
    """
    import os
    if not os.path.exists('.coursesel'):
        print('Not found .coursesel file. Please run init first')
        return
    js = get_jsession()
    with open('.coursesel', 'r') as f:
        config = json.load(f)
    config['jsessionID'] = js
    with open('.coursesel', 'w') as f:
        json.dump(config, f, indent=4)
    print("Done. Please use command 'elect' to start electing.")


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
    Elect courses
    """
    import os
    if os.path.exists('.coursesel'):
        # Use this file to initialize
        with open('.coursesel', 'r') as f:
            config = json.load(f)
        jsessionID = config['jsessionID']
        electTurnID = config['electTurnId']
        courses_eid = []
        for l in config['courses']:
            courses_eid.append(l['electTurnLessonTaskId'])
        ElectTurnLessonTaskID = ','.join(courses_eid)
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
