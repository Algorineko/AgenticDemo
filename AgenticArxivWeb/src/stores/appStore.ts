import { defineStore } from "pinia";
import { api, getApiBase } from "@/api/client";
import type { ChatResponse, Paper, PdfAsset, TranslateAsset, Role, ReactStep } from "@/api/types";

export interface ChatMessage {
  role: Role;
  content: string;
  ts: number;
}

function nowTs() {
  return Date.now();
}

export const useAppStore = defineStore("app", {
  state: () => ({
    apiBase: getApiBase(),
    sessionId: (localStorage.getItem("session_id") || "demo1") as string,

    loading: false,
    lastError: "" as string,

    messages: [] as ChatMessage[],

    papers: [] as Paper[],
    pdfAssets: [] as PdfAsset[],
    translateAssets: [] as TranslateAsset[],

    lastHistory: [] as ReactStep[],

    // 论文列表按钮操作：true=走 /chat 让 agent 决定调用工具；false=直调 /pdf/* 工具接口
    preferAgent: true,
  }),

  getters: {
    pdfMap(state) {
      const m = new Map<string, PdfAsset>();
      state.pdfAssets.forEach((a) => m.set(a.paper_id, a));
      return m;
    },
    translateMap(state) {
      const m = new Map<string, TranslateAsset>();
      state.translateAssets.forEach((a) => m.set(a.paper_id, a));
      return m;
    },
  },

  actions: {
    setSessionId(id: string) {
      this.sessionId = id.trim() || "demo1";
      localStorage.setItem("session_id", this.sessionId);
    },

    pushUser(content: string) {
      this.messages.push({ role: "user", content, ts: nowTs() });
    },
    pushAssistant(content: string) {
      this.messages.push({ role: "assistant", content, ts: nowTs() });
    },

    async refreshSnapshot() {
      // 论文是 session 维度；assets 是全局缓存列表
      try {
        const [papersRes, pdfRes, trRes] = await Promise.all([
          api.get(`/sessions/${encodeURIComponent(this.sessionId)}/papers`),
          api.get(`/pdf/assets`),
          api.get(`/translate/assets`),
        ]);

        this.papers = papersRes.data?.papers || [];
        this.pdfAssets = pdfRes.data?.assets || [];
        this.translateAssets = trRes.data?.assets || [];
      } catch (e: any) {
        this.lastError = e?.response?.data?.detail || e?.message || String(e);
      }
    },

    async sendChat(message: string) {
      const text = message.trim();
      if (!text) return;

      this.loading = true;
      this.lastError = "";
      this.pushUser(text);

      try {
        const res = await api.post<ChatResponse>("/chat", {
          session_id: this.sessionId,
          message: text,
        });

        const data = res.data;
        this.pushAssistant(data.reply || "(空回复)");
        this.lastHistory = data.history || [];

        this.papers = data.papers || [];
        this.pdfAssets = data.pdf_assets || [];
        this.translateAssets = data.translate_assets || [];
      } catch (e: any) {
        const msg = e?.response?.data?.detail || e?.message || String(e);
        this.lastError = msg;
        this.pushAssistant(`请求失败：${msg}`);
      } finally {
        this.loading = false;
      }
    },

    async downloadPaper(refIndex1based: number) {
      if (this.preferAgent) {
        await this.sendChat(`下载第${refIndex1based}篇论文PDF`);
        return;
      }

      // 直调工具接口（更确定）
      this.loading = true;
      this.lastError = "";
      try {
        const res = await api.post("/pdf/download", {
          session_id: this.sessionId,
          ref: refIndex1based,
          force: false,
        });
        this.pushAssistant(`下载结果：${JSON.stringify(res.data)}`);
        await this.refreshSnapshot();
      } catch (e: any) {
        const msg = e?.response?.data?.detail || e?.message || String(e);
        this.lastError = msg;
        this.pushAssistant(`下载失败：${msg}`);
      } finally {
        this.loading = false;
      }
    },

    async translatePaper(refIndex1based: number) {
      // 前端提示：没下载也能翻译（后端 translate_arxiv_pdf 会确保 raw pdf 存在）
      // 这里仍然给出“将自动下载后翻译”的提示语，符合你的需求
      const tip = `准备翻译第${refIndex1based}篇论文（若未下载将自动先下载再翻译）`;

      if (this.preferAgent) {
        await this.sendChat(`${tip}。请开始翻译并输出中文PDF。`);
        return;
      }

      this.loading = true;
      this.lastError = "";
      try {
        this.pushAssistant(tip);
        const res = await api.post("/pdf/translate", {
          session_id: this.sessionId,
          ref: refIndex1based,
          force: false,
          service: "bing",
          threads: 4,
          keep_dual: false,
        });
        this.pushAssistant(`翻译结果：${JSON.stringify(res.data)}`);
        await this.refreshSnapshot();
      } catch (e: any) {
        const msg = e?.response?.data?.detail || e?.message || String(e);
        this.lastError = msg;
        this.pushAssistant(`翻译失败：${msg}`);
      } finally {
        this.loading = false;
      }
    },

    clearChat() {
      this.messages = [];
      this.lastHistory = [];
      this.lastError = "";
    },
  },
});
