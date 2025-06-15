# ADF boilerplate for STIG checklist data

def adf_paragraph(lines):
    content = []
    for i, line in enumerate(lines):
        if i > 0:
            content.append({"type": "hardBreak"})
        content.append({"type": "text", "text": line})
    return {"type": "paragraph", "content": content}


def adf_blockquote(text):
    lines = text.strip().splitlines()
    para = {
        "type": "paragraph",
        "content": []
    }
    for i, line in enumerate(lines):
        if i > 0:
            para["content"].append({"type": "hardBreak"})
        para["content"].append({"type": "text", "text": line})
    return {
        "type": "blockquote",
        "content": [para]
    }


def stig_check_to_adf(fields):
    metadata = adf_paragraph([
        f"STIG: {fields.get('stig_name', '')}",
        f"Group ID: {fields.get('group_id', '')}",
        f"Severity: {fields.get('severity', '')}",
        f"Status: {fields.get('status', '')}"
    ])

    check_block = adf_blockquote(fields.get("check_content", ""))
    fix_block = adf_blockquote(fields.get("fix_text", ""))

    return {
        "type": "doc",
        "version": 1,
        "content": [metadata, check_block, fix_block]
    }