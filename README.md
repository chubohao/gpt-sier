# GPT SIER
基于Vue3 + vite + Typescript + Tailwind CSS 纯前端框架，调用 OpenAI 的 `gpt-3.5-turbo` 模型 API 实现的简单聊天对话，支持连续对话。7月底可以支持 `GPT-4` 模型。

参考 [CHATGPT-VUE](https://github.com/lianginx/chatgpt-vue)
## 开始

> 注意：本项目没有使用任何代理，API 在前端发送请求，能否连通基于你当前浏览器的所处的网络环境。

在开始之前，请确保您已正确安装 Node.js 运行时环境，本案例是 `Nodejs 18.16.0` 。如果您还没有安装 Node.js，请 [点击这里下载](https://nodejs.org/)。

使用 ChatGPT 需要先申请 API Key，已注册但还没有 API Key 的用户可以 [前往这里生成](https://platform.openai.com/account/api-keys)。

准备就绪后，进入项目根目录执行以下命令运行项目：

```bash
npm i
npm run dev
```

运行成功时通常显示（请以具体为准）：

```bash
VITE v3.2.5  ready in 294 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

按住 `Ctrl` 或 `command` 点击 Local 链接，在浏览器中打开项目，然后在页面底部输入框中填入您的 API Key，然后点击保存，即可开始使用！

如果想要更改 API Key，点击页面右上角 `设置`，重新输入并保存即可。

## 许可证

本项目使用 [MIT](LICENSE) 协议
