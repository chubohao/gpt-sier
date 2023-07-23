
import openai
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import threading

# Set the context round to 5 round
quantity = 10

# Init user infomation
user_status = [{"id": 0, "start":time.time(), "time": time.time(), "messages": [{"role": "system", "content": "You are a intelligent assistant."}]}]

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):

        print(self.path)
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Get the quetsion and save
        id = json.loads(post_data)['id']
        question = json.loads(post_data)['question']

        # Query historical records,
        # if the user already exists, accumulate questions and update the time,
        # if the user does not exist, add and insert.
        if id in [item.get("id") for item in user_status]:
            data = [item for item in user_status if item["id"] == id]

            # If greater than 5 rounds, delete the oldest.
            if len(data[0]['messages']) > quantity:
                data[0]['messages'] = data[0]['messages'][-quantity:]

            # If the interval exceeds 10 minutes, clear the user's history.
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

        # Set response headers, enable streaming
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Transfer-Encoding', 'chunked')
        self.end_headers()

        # Call openai API
        openai.api_key = ""
        messages = [item for item in user_status if item["id"] == id][0]['messages']
        
        # Send the data stream chunk by chunk to the client
        print(messages)
        response_chunck_list = []
        for chunk in openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages, stream=True):
            # Determine if it is the last block
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

if __name__ == '__main__':
        print("# start sier server 8998")
        server = HTTPServer(("0.0.0.0", 8998), RequestHandler)
        server.serve_forever()   
  