# ADF boilerplate for STIG checklist data

# **bold**, regular text
def adf_tuple(lines):
    content = []

    for i, (label, value) in enumerate(lines):
        if i > 0:
            content.append({"type": "hardBreak"})
        
        content.append({
            "type": "text",
            "text": f"{label} ",
            "marks": [{"type": "strong"}]
        })
        content.append({
            "type": "text",
            "text": value
        })

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


# Could have config for multiple boilerplates
def stig_check_to_adf(fields):
    metadata = adf_tuple([
        ("STIG", fields.get('stig_name', '')),
        ("Group ID", fields.get('group_id', '')),
        ("Severity", fields.get('severity', '')),
        ("Status", fields.get('status', ''))
    ])

    finding_header = adf_tuple([("Finding Details","")])
    finding_block = adf_blockquote(fields.get("finding_details", ""))

    fix_header = adf_tuple([("Fix", "")])
    fix_block = adf_blockquote(fields.get("fix_text", ""))

    check_header = adf_tuple([("Check", "Check the fix with:")])
    check_block = adf_blockquote(fields.get("check_content", ""))

    return {
        "type": "doc",
        "version": 1,
        "content": [
            metadata,
            finding_header, finding_block,
            fix_header, fix_block,
            check_header, check_block
            ]
    }