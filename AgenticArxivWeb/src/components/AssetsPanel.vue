<template>
  <section class="card assets">
    <header class="card-header">
      <div class="title">下载/翻译缓存</div>
      <p class="muted">
        PDF: {{ pdfList.length }} 条 · 翻译: {{ trList.length }} 条
      </p>
    </header>

    <div class="lists">
      <!-- 已下载 -->
      <div class="block">
        <div class="block-title">已下载（READY）</div>
        <div class="list-scroll">
          <div v-if="!pdfList.length" class="empty">暂无已下载 PDF</div>

          <div v-for="a in pdfList" :key="a.paper_id" class="item">
            <div class="item-top">
              <div class="mono id">{{ a.paper_id }}</div>
              <span class="pill ok">READY</span>
            </div>
            <div class="sub mono">path: {{ a.local_path }}</div>
            <div class="sub">
              size: {{ formatBytes(a.size_bytes) }} · updated: {{ a.updated_at }}
            </div>
          </div>
        </div>
      </div>

      <!-- 已翻译 -->
      <div class="block">
        <div class="block-title">已翻译（READY）</div>
        <div class="list-scroll">
          <div v-if="!trList.length" class="empty">暂无已翻译 PDF</div>

          <div v-for="t in trList" :key="t.paper_id" class="item">
            <div class="item-top">
              <div class="mono id">{{ t.paper_id }}</div>
              <span class="pill ok">READY</span>
            </div>
            <div class="sub mono">out: {{ t.output_mono_path }}</div>
            <div class="sub">
              threads: {{ t.threads }} · updated: {{ t.updated_at }}
            </div>
            <div class="sub" v-if="t.output_dual_path">
              dual: <span class="mono">{{ t.output_dual_path }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useAppStore } from "@/stores/appStore";

const store = useAppStore();

const pdfList = computed(() => {
  const arr = Array.from(store.pdfMap.values()).filter((x) => x.status === "READY");
  // 新的在前
  return arr.sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || ""));
});

const trList = computed(() => {
  const arr = Array.from(store.translateMap.values()).filter((x) => x.status === "READY");
  return arr.sort((a, b) => (b.updated_at || "").localeCompare(a.updated_at || ""));
});

function formatBytes(n: number) {
  if (!Number.isFinite(n) || n <= 0) return "0 B";
  const units = ["B", "KB", "MB", "GB", "TB"];
  let v = n;
  let i = 0;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(i === 0 ? 0 : 2)} ${units[i]}`;
}
</script>

<style scoped>
.assets {
  height: 100%;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.card-header {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

.title { font-weight: 700; margin-bottom: 6px; }
.muted { color: var(--muted); margin: 0; font-size: 12px; }

/* 两块列表：各占一半高度 */
.lists {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 12px;
}

.block {
  border: 1px solid var(--border);
  border-radius: 14px;
  background: rgba(255,255,255,0.02);
  padding: 10px;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

.block-title {
  font-weight: 650;
  color: var(--muted);
  font-size: 12px;
  margin-bottom: 8px;
}

/* ✅ 每个列表独立滚动条 */
.list-scroll {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding-right: 2px;
}

.item {
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 10px;
  background: rgba(255,255,255,0.015);
  margin-bottom: 8px;
}

.item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 4px;
}

.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.id { font-weight: 700; }
.sub { color: var(--muted); font-size: 12px; line-height: 1.35; margin-top: 2px; }

.pill {
  display: inline-flex;
  align-items: center;
  height: 20px;
  padding: 0 8px;
  border-radius: 999px;
  border: 1px solid var(--border);
  font-size: 12px;
  user-select: none;
}
.pill.ok { border-color: rgba(0,255,153,.35); }

.empty { color: var(--muted); font-size: 12px; padding: 6px 2px; }
</style>
