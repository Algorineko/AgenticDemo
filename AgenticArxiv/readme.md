# Agentic Arxiv
本项目实现了受Model Context Protocol（MCP）启发的工具系统，允许LLM Agent发现和使用外部工具，包括ArXiv论文检索等能力。

.env文件放置
```txt
LLM_BASE_URL=<base-url>
LLM_API_KEY=<token>
```

### PDFMathTranslate
```sh
# 下载 ArXiv 论文PDF
export PDF_RAW_PATH=/home/dev/AgenticDemo/AgenticArxiv/output/pdf_raw 
wget -P $PDF_RAW_PATH https://arxiv.org/pdf/2601.22156v1.pdf
```
```sh
# 进入GUI
pdf2zg -i
# 默认是英译中,-t为使用CPU核数
pdf2zh ./pdf-raw/3690624.3709231.pdf -s bing -o ./pdf-translated/ [-p 1] [--debug] [-t 4]
# case
pdf2zh /home/dev/AgenticDemo/AgenticArxiv/output/pdf_raw/2601.22156v1.pdf -s bing -o /home/dev/AgenticDemo/AgenticArxiv/output/pdf_translated -t 3
``` 