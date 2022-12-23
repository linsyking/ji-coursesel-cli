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
        self.error=0
        self.success=False
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ru;q=0.6',
            'Connection': 'keep-alive',
            'Referer': f'https://dailyreport.sjtu.edu.cn/{api_name}/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

    def getlist(self):
        while(1):
            res = requests.get(self.api_getlist,cookies=self.cookie, headers=self.headers)
            kop = res.content.decode(encoding='utf-8',errors='ignore')
            try:
                kks = json.loads(kop)['entities']
            except:
                print("GETLIST JSON PARSE ERROR, CHECK YOUR COOKIE")
                self.error=1
                return
            ans=[]
            if len(kks)<5:
                continue
            if(self.get):
                return
            print('-'*15)
            print('Get list')
            self.get=True
            for one in kks:
                ans.append((one['startTime'],one['id']))
                print(one['startTime'],one['id'])
            print('-'*15)
            # Success
            self.ans = ans
            with open('list.txt','a') as f:
                f.write('-'*15+'\n')
                for one in kks:
                    f.write(f"{one['startTime']}:{one['id']}\n")
                f.write('-'*15+'\n')
            return

    def save(self, id):
        # save
        files = {'busScheduleId': (None, id)}
        while(1):
            if self.success:
                return
            res = requests.post(self.api_save,cookies=self.cookie,files=files, headers=self.headers)
            kop = res.content.decode(encoding='utf-8',errors='ignore')
            print(kop)
            with open(f'{id}.txt','a', encoding='utf-8', errors='ignore') as f:
                f.write(kop+'\n')
            try:
                kks = json.loads(kop)
            except:
                print('Not good',id)
                continue
            if 'errno' in kks:
                if kks['errno']!=-2:
                    print('Success')
                    self.success=True
                    return
                else:
                    print(kks)
            # return
            

    def run(self):
        # First get list
        print('Waiting for the lists...')
        thread_box=[]
        for i in range(self.thread_num):
            thread_box.append(threading.Thread(target=self.getlist, args=()))
        for i in thread_box:
            i.start()
        # for i in thread_box:
        #     i.join()
        # First try preferred time
        while len(self.ans)==0:
            if(self.error):
                print('Give up')
                return
            pass
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
        sleep(0.1)
        if self.success:
            print('Done')
            return
        for i in range(1,len(arth_box)):
            arth_box[i].start()
        for one in arth_box:
            one.join()
        print('Done')

if __name__=="__main__":
    # robber=robFood('2A3A3186EB4D20F4E84A21D06F1F93B0','ffffffff097e1f5245525d5f4f58455e445a4a4229a0','haircut','bus','FOURTH','2022-04-14','18:30')
    robber=robFood('99BEEF94CDAA1FF5A715CD5C2CAD9906','ffffffff097e1f5245525d5f4f58455e445a4a4229a0','market','market','YLYLS','2022-04-14','15:30')
    robber.run()