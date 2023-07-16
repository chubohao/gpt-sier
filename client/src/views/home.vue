<script lang="ts">
import type { ChatMessage } from "@/types";
import { reactive, ref, watch, nextTick, onMounted } from "vue";
import Loding from "@/components/Loding.vue";
import Copy from "@/components/Copy.vue";
import { md } from "@/api/markdown";
import axios from 'axios';
import { TheSingleShoulderBag } from "@icon-park/vue-next";

export default {
  data() {
    return {
      id: Math.floor(Math.random() * 100) + 1,
      isTalking: false,
      messageContent: "",
      roleAlias: { user: "ME", assistant: "GPT SIER", system: "System" },
      md: md,
      messageList: [
        {
          role: "system",
          content: "你是 ChatGPT，OpenAI 训练的大型语言模型，尽可能简洁地回答。",
        },
        {
          role: "assistant",
          content: `你好，我是AI语言模型，我可以提供一些常用服务和信息。`,
        },
      ],
    };
  },
  watch: {
    messageList : {
      handler(newVal, oldVal) {
        this.scrollToBottom()
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    send() {
      if (!this.messageContent.length) return;
      this.sendChatMessage();
    },
    appendLastMessageContent(content: string){
      this.messageList[this.messageList.length - 1].content += content;
    },
    sendChatMessage() {
      try {
        const question = this.messageContent;
        this.isTalking = true;
        if (this.messageList.length === 2) {
          this.messageList.pop();
        }
        this.messageList.push({ role: "user", content: question});
        this.clearMessageContent();
        this.messageList.push({ role: "assistant", content: "" });
        
        fetch('/api', {
            method: 'POST',
            body: JSON.stringify({"id": this.id, question: question}),
            headers: {'Content-Type': 'application/json'}
          }).then(response => {
            const reader = response.body.getReader();
            const processChunk = async () => {
              const { done, value } = await reader.read();
              if (done) {return;}
              this.appendLastMessageContent(new TextDecoder('utf-8').decode(value))
              processChunk();
            };

            processChunk();
            }
          ).catch(error => {
            console.error('Error:', error);
          });
          this.isTalking = false;
      } catch (error: any) {
        this.appendLastMessageContent(error);
      } finally {
        this.isTalking = false;
      }
    },

    clearMessageContent() {
      this.messageContent = ""
    },
    scrollToBottom() {
      let scrollElem = this.$refs.chatListDom;
      if (!scrollElem) return
      console.log("scroll", scrollElem.scrollHeight)
      window.scrollTo({
        top: scrollElem.scrollHeight, behavior: "smooth"
      })
    }
  }

};


</script>

<template>

  <div class="flex flex-col h-screen">
    <div class="flex flex-nowrap fixed w-full items-baseline top-0 px-6 py-4 bg-gray-100">
      
      <div class="text-2xl font-bold">GPT SIER</div>
      <div class="text-sm text-gray-500 ml-3">基于 GPT-3.5-TURBO 模型</div>
      
      <div class="ml-auto px-3 py-2 text-sm cursor-pointer hover:bg-white rounded-md" @click="">设置</div>
    </div>

    <div class="flex-1 mx-2 mt-20 mb-2" ref="chatListDom">
      <div class="group flex flex-col px-4 py-3 hover:bg-slate-100 rounded-lg" v-for="item of messageList.filter((v) => v.role !== 'system')">
        <div class="flex justify-between items-center mb-2">
          <div class="font-bold">{{ roleAlias[item.role] }}：</div>
          <Copy class="invisible group-hover:visible" :content="item.content" />
        </div>
        <div>
          <div class="prose text-sm text-slate-600 leading-relaxed" v-if="item.content" v-html="md.render(item.content)"></div>
          <Loding v-else />
        </div>
      </div>
    </div>

    <div class="sticky bottom-0 w-full p-6 pb-8 bg-gray-100">
      <div class="flex">
        <input class="input" type="text'" placeholder="请输入" v-model="messageContent" @keydown.enter="isTalking || send()"/>
        <button class="btn" :disabled="isTalking" @click="send()">Send</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
pre {
  font-family: -apple-system, "Noto Sans", "Helvetica Neue", Helvetica,
    "Nimbus Sans L", Arial, "Liberation Sans", "PingFang SC", "Hiragino Sans GB",
    "Noto Sans CJK SC", "Source Han Sans SC", "Source Han Sans CN",
    "Microsoft YaHei", "Wenquanyi Micro Hei", "WenQuanYi Zen Hei", "ST Heiti",
    SimHei, "WenQuanYi Zen Hei Sharp", sans-serif;
}
</style>