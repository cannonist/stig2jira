import re

def markdown_to_adf(md_text):
    
    lines = md_text.splitlines()
    
    content = []
    quote_buffer = []

    for line in lines:
        # line = line.strip()
    
        # if not line.startswith(">") and quote_buffer:
        #     quote_content = []
        #     for q in quote_buffer:
        #         text = q.strip()
        #         quote_content.append({
        #             "type": "paragraph",
        #             "content": [{"type": "text", "text": text}] if text else []
        #         })

        #     content.append({
        #         "type": "blockquote",
        #         "content": quote_content
        #     })
        #     quote_buffer = []

        if not line.startswith(">") and quote_buffer:
            paragraph_content = []
            for q in quote_buffer:
                text = q.rstrip()
                if not text:
                    paragraph_content.append({"type": "hardBreak"})
                else:
                    if paragraph_content:
                        paragraph_content.append({"type": "hardBreak"})
                    paragraph_content.append({"type": "text", "text": text})

            content.append({
                "type": "blockquote",
                "content": [{
                    "type": "paragraph",
                    "content": paragraph_content
                }]
            })
            quote_buffer = []

        if line.startswith(">"):
            quote_buffer.append(line[1:].lstrip())
            continue

        bold_match = re.search(r"\*\*(.+?)\*\*", line)
        if bold_match:
            before = line[:bold_match.start()]
            bold = bold_match.group(1)
            after = line[bold_match.end():]

            paragraph = {"type": "paragraph", "content": []}

            if before.strip():
                paragraph["content"].append({"type": "text", "text": before})

            paragraph["content"].append({
                "type": "text",
                "text": bold,
                "marks": [{"type": "strong"}]
            })

            if after.strip():
                paragraph["content"].append({"type": "text", "text": after})

            content.append(paragraph)
            continue

        # Default: plain paragraph
        content.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": line}]
        })

    if quote_buffer:
        content.append({
            "type": "blockquote",
            "content": [{
                "type": "paragraph",
                "content": [{"type": "text", "text": " ".join(quote_buffer)}]
            }]
        })

    return {
        "type": "doc",
        "version": 1,
        "content": content
    }