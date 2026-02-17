<template>
  <div class="app">
    <header class="topbar">
      <div class="brand">
        <div class="logo">🧩</div>
        <div>
          <div class="name">AgenticArxiv Web</div>
          <div class="desc">对话 + 论文临时记忆 + 下载/翻译缓存</div>
        </div>
      </div>
    </header>

    <main class="grid">
      <ChatPanel />
      <div class="right">
        <PapersPanel />
        <AssetsPanel />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import ChatPanel from "@/components/ChatPanel.vue";
import PapersPanel from "@/components/PapersPanel.vue";
import AssetsPanel from "@/components/AssetsPanel.vue";
</script>

<style scoped>
.app { min-height: 100vh; background: var(--bg); color: var(--fg); }
.topbar { position: sticky; top:0; z-index:10; backdrop-filter: blur(10px); background: rgba(10,10,12,0.75); border-bottom: 1px solid var(--border); }
.brand { display:flex; gap:12px; align-items:center; padding: 14px 18px; max-width: 1400px; margin: 0 auto; }
.logo { font-size: 24px; }
.name { font-weight: 800; }
.desc { color: var(--muted); font-size: 12px; margin-top: 2px; }

.grid { max-width: 1400px; margin: 0 auto; padding: 14px 18px; display:grid; grid-template-columns: 1.2fr 1fr; gap: 14px; height: calc(100vh - 64px); }
.right { display:grid; grid-template-rows: 1fr 1fr; gap: 14px; min-height: 0; }
@media (max-width: 1100px) {
  .grid { grid-template-columns: 1fr; height: auto; }
  .right { grid-template-rows: auto; }
}
</style>
