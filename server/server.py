
import openai
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import threading

quantity = 20
user_status = [{"id": 0, "start":time.time(), "time": time.time(), "messages": [{"role": "system", "content": "You are a intelligent assistant."}]}]

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        print(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 获取请求人信息并记录
        id = json.loads(post_data)['id']
        question = json.loads(post_data)['question']

        # 查询历史记录，存在则累计问题，并更新时间；新增则插入
        if id in [item.get("id") for item in user_status]:
            data = [item for item in user_status if item["id"] == id]
            # 最大限制10分钟
            '''
            if time.time() - data[0]['start'] >= 600:
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.send_header('Transfer-Encoding', 'chunked')
                self.end_headers()
                self.wfile.write(b'0\r\nOVER TIMER\r\n')
                self.wfile.flush()
                self.wfile.write(b'0\r\n\r\n')
                self.wfile.flush()
                return
            '''

            # 如果大于5个回合，则去除最久的
            if len(data[0]['messages']) > quantity:
                data[0]['messages'] = data[0]['messages'][-quantity:]

            # 如果间隔10分钟，则清空历史记录
            if time.time() - data[0]['time'] >= 300:
                data[0]['messages'] = [{"role": "user", "content": question}]
            else:
                data[0]['messages'].append({"role": "user", "content": question})

            data[0]['time'] = time.time()
        else:
            user_status.append({"id": id, 
                                "start": time.time(), 
                                "time": time.time(), 
                                "messages": [{"role": "system", "content": "You are a intelligent assistant."}, {"role": "user", "content": question}]})

        # 设置响应头，启用流式传输
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

        # 调API
        openai.api_key = "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"
        messages = [item for item in user_status if item["id"] == id][0]['messages']
        # 将数据流逐块发送给客户端
        print(messages)
        response_chunck_list = []
        for chunk in openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, stream=True):
            # 判断是否最后一块
            if chunk["choices"][0]['finish_reason'] == "stop": 
                self.wfile.write(b'0\r\n\r\n')
                self.wfile.flush()
            else:
                chunk_content = chunk["choices"][0]['delta']['content']
                response_chunck_list.append(chunk_content)

                if chunk_content != "":
                    chunk_content = chunk_content.encode('utf-8')
                    self.wfile.write(b'%X\r\n%s\r\n' % (len(chunk_content), chunk_content))
                    self.wfile.flush()

        if id in [item.get("id") for item in user_status]:
            data = [item for item in user_status if item["id"] == id]
            data[0]['messages'].append({"role": "assistant", "content": ''.join(response_chunck_list)})

        print(user_status)
if __name__ == '__main__':
        print("# start sier server 8998")
        server = HTTPServer(("0.0.0.0", 8998), RequestHandler)
        server.serve_forever()   
  