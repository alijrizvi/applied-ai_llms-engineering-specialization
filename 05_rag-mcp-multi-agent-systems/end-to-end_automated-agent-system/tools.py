# Here, we Define the practical actions that our Agent can perform during a Workflow
# Side Effects (fetch, store)

import requests

## Sends an HTTP Request to a Website and Returns the first part of the page's Content
def fetch_tool(url: str):
    try:
        r = requests.get(url, timeout = 5)
        return r.text[:300]
    except Exception:
        return "ERROR: Fetch failed."

## Creates a short, placeholder Summary by Trimming the text
def summarize_tool(text: str):
    return "SUMMARY: " + text[:150]

## Writes any Generated Content to a file, so that the Results can be saved
def store_tool(content: str, filename = "output.txt"):
    with open(filename, "w", encoding = "utf-8") as f:
        f.write(content)
    return f"Stored Output in {filename}"


# TOOLS = {
#     "fetch": fetch_tool,
#     "summarize": summarize_tool,
#     "store": store_tool
# }

# tool_name = "summarize"

# result = TOOLS[tool_name]()