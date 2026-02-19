# AgenticArxiv/tools/cache_status_tool.py
from __future__ import annotations
from typing import Any, Dict, Optional, Union

from tools.tool_registry import registry
from models.store import store

def get_paper_cache_status(
    session_id: str = "default",
    ref: Union[str, int, None] = None,
    paper_id: Optional[str] = None,
) -> Dict[str, Any]:
    # 解析 paper_id
    if not paper_id:
        if ref is None:
            last = store.get_last_active_paper_id(session_id)
            if not last:
                raise ValueError("请提供 ref 或 paper_id，或先下载/选择一篇论文以产生 last_active_paper_id")
            paper_id = last
        else:
            paper = store.resolve_paper(session_id, ref)
            if paper is None:
                raise ValueError("未找到论文：请先 /arxiv/recent 写入 session 记忆，或直接传 paper_id")
            paper_id = paper.id

    pdf = store.get_pdf_asset(paper_id)
    tr = store.get_translate_asset(paper_id)

    return {
        "paper_id": paper_id,
        "pdf": (pdf.dict() if pdf else None),
        "translate": (tr.dict() if tr else None),
        "pdf_ready": bool(pdf and pdf.status == "READY"),
        "translated_ready": bool(tr and tr.status == "READY"),
    }

SCHEMA = {
    "type": "object",
    "properties": {
        "session_id": {"type": "string", "default": "default"},
        "ref": {"anyOf": [{"type": "integer"}, {"type": "string"}]},
        "paper_id": {"type": "string"},
    },
    "required": [],
}

registry.register_tool(
    name="get_paper_cache_status",
    description="查询某篇论文的本地缓存状态（是否已下载raw、是否已翻译mono），用于避免重复下载/翻译",
    parameter_schema=SCHEMA,
    func=get_paper_cache_status,
)
