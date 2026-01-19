# AgenticArxiv/tools/arxiv_tool.py
import arxiv
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional

cs_categories = {
    "*": "All Computer Science",
    "AI": "Artificial Intelligence",
    "AR": "Hardware Architecture",
    "CC": "Computational Complexity",
    "CE": "Computational Engineering, Finance, and Science",
    "CG": "Computational Geometry",
    "CL": "Computation and Language",
    "CR": "Cryptography and Security",
    "CV": "Computer Vision and Pattern Recognition",
    "CY": "Computers and Society",
    "DB": "Databases",
    "DC": "Distributed, Parallel, and Cluster Computing",
    "DL": "Digital Libraries",
    "DM": "Discrete Mathematics",
    "DS": "Data Structures and Algorithms",
    "ET": "Emerging Technologies",
    "FL": "Formal Languages and Automata Theory",
    "GL": "General Literature",
    "GR": "Graphics",
    "GT": "Computer Science and Game Theory",
    "HC": "Human-Computer Interaction",
    "IR": "Information Retrieval",
    "IT": "Information Theory",
    "LG": "Machine Learning",
    "LO": "Logic in Computer Science",
    "MA": "Multiagent Systems",
    "MM": "Multimedia",
    "MS": "Mathematical Software",
    "NA": "Numerical Analysis",
    "NE": "Neural and Evolutionary Computing",
    "NI": "Networking and Internet Architecture",
    "OH": "Other Computer Science",
    "OS": "Operating Systems",
    "PF": "Performance",
    "PL": "Programming Languages",
    "RO": "Robotics",
    "SC": "Symbolic Computation",
    "SD": "Sound",
    "SE": "Software Engineering",
    "SI": "Social and Information Networks",
    "SY": "Systems and Control",
}


def get_recently_submitted_cs_papers(
    max_results: int = 50, aspect: str = "*", days: int = 7
) -> List[Dict]:
    """
    获取最近 days 天内提交的 cs.<aspect> 论文列表
    aspect: "*" 表示全部子领域，否则如 "LO" / "AI" 等
    """
    now_utc = datetime.now(timezone.utc)
    start_date = (now_utc - timedelta(days=days)).strftime("%Y%m%d")
    end_date = now_utc.strftime("%Y%m%d")

    if aspect == "*":
        query = f"cat:cs.* AND submittedDate:[{start_date} TO {end_date}]"
    else:
        query = f"cat:cs.{aspect} AND submittedDate:[{start_date} TO {end_date}]"

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    papers: List[Dict] = []
    for result in client.results(search):
        paper_info = {
            "id": result.get_short_id(),
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": (result.summary[:200] + "...") if len(result.summary) > 200 else result.summary,
            "published": result.published.strftime("%Y-%m-%d %H:%M:%S"),
            "updated": result.updated.strftime("%Y-%m-%d %H:%M:%S") if result.updated else None,
            "pdf_url": result.pdf_url,
            "primary_category": result.primary_category,
            "categories": result.categories,
            "comment": result.comment,
            "links": [link.href for link in result.links],
        }
        papers.append(paper_info)

    return papers


def format_papers_console(papers: List[Dict], top_authors: int = 3) -> str:
    if not papers:
        return "未获取到最近提交的论文\n"
    lines = []
    for i, paper in enumerate(papers, 1):
        lines.append(f"{i}. {paper['title']}")
        lines.append(f"   作者: {', '.join(paper['authors'][:top_authors])}")
        lines.append(f"   发布时间: {paper['published']}")
        lines.append(f"   PDF链接: {paper['pdf_url']}")
        lines.append(f"   注释: {paper.get('comment')}")
        lines.append("-" * 80)
    return "\n".join(lines)


if __name__ == "__main__":
    ASPECT = "LO"
    papers = get_recently_submitted_cs_papers(max_results=20, aspect=ASPECT)
    print(format_papers_console(papers))
