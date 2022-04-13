from time import sleep
import requests
import threading
import json

class robFood:
    def __init__(self, JSESSIONID, dailysjtu, api_name , frontend_name, line_type, date,preferred_time, thread_num = 10) -> None:
        self.api_save = f'https://dailyreport.sjtu.edu.cn/{api_name}/frontend/{frontend_name}/appointment/save'
        self.api_getlist = f'https://dailyreport.sjtu.edu.cn/{api_name}/frontend/{frontend_name}/schedule/list?lineType={line_type}&date={date}'
        self.cookie = {"JSESSIONID":JSESSIONID, "dailyreport.sjtu": dailysjtu}
        self.prefer_time = preferred_time
        self.get=False
        self.thread_num= thread_num
        self.ans=[]
        self.success=False

    def getlist(self):
        while(1):
            res = requests.get(self.api_getlist,cookies=self.cookie)
            kop = res.content.decode(encoding='utf-8',errors='ignore')
            kks = json.loads(kop)['entities']
            ans=[]
            if len(kks)==0:
                continue
            if(self.get):
                return
            self.get=True
            for one in kks:
                ans.append((one['startTime'],one['id']))
            # Success
            self.ans = ans
            return

    def save(self, id):
        # save
        files = {'busScheduleId': (None, id)}
        while(1):
            res = requests.post(self.api_save,cookies=self.cookie,files=files)
            kop = res.content.decode(encoding='utf-8',errors='ignore')
            kks = json.loads(kop)
            if 'errno' in kks:
                if kks['errno']!=-2:
                    print('Success')
                    self.success=True
                    return
                else:
                    print(kks)
            return
            

    def run(self):
        # First get list
        print('Waiting for the lists...')
        thread_box=[]
        for i in range(self.thread_num):
            thread_box.append(threading.Thread(target=self.getlist, args=()))
        for i in thread_box:
            i.start()
        for i in thread_box:
            i.join()
        # First try preferred time
        if len(self.ans)==0:
            print('Please check cookie')
            return
        print('Got List')
        arth_box=[]
        for i in self.ans:
            if i[0] == self.prefer_time:
                arth_box.append(threading.Thread(target=self.save, args=(i[1],)))
                break
        for i in self.ans:
            if i[0] != self.prefer_time:
                arth_box.append(threading.Thread(target=self.save, args=(i[1],)))
        arth_box[0].start()
        sleep(0.5)
        if self.success:
            print('Done')
            return
        for i in range(1,len(arth_box)):
            arth_box[i].start()
        for one in arth_box:
            one.join()
        print('Done')

if __name__=="__main__":
    # robber=robFood('A2131EF83AE59DE8CC93A9DD6E4CAB75','ffffffff097e1f5545525d5f4f58455e445a4a4229a0','haircut','bus','TWO','2022-04-13','16:00')
    robber=robFood('2FAF5B88AF35943962AECF48336FF18A','ffffffff097e1f5245525d5f4f58455e445a4a4229a0','market','market','YLYLS','2022-04-14','14:00')
    robber.run()