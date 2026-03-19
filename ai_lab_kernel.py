# =========================================================
# AI LAB KERNEL v1 — DOCTRINE-EMBEDDED
# Self-contained • Portable • Deterministic
# =========================================================


import os
import json
import uuid
from datetime import datetime


# =========================================================
# 🧠 CORE SPEC
# =========================================================


AI_LAB_KERNEL = {
    "identity": {
        "name": "AI Lab",
        "version": "v1",
        "purpose": "Artifact generation engine"
    },
    "directories": [
        "agents",
        "generators",
        "renderers",
        "acquisition",
        "llm",
        "memory",
        "cli",
        "artifacts",
        "config"
    ],
    "pipeline": [
        "query",
        "enrichment",
        "llm_drafting",
        "content_structuring",
        "rendering",
        "memory",
        "delivery"
    ],
    "llm": {
        "providers": ["openrouter", "nim", "openai"],
        "default": "openrouter"
    }
}


# =========================================================
# ⚖️ DOCTRINE (ENFORCED INTERNALLY)
# =========================================================


DOCTRINE = {
    "EXECUTE_OVER_EXPLAIN": True,
    "REQUIRE_ARTIFACT": True,
    "REQUIRE_MEMORY_WRITE": True,
    "GRACEFUL_DEGRADATION": True,
    "LOG_ALL_STEPS": True
}


# =========================================================
# 📁 BOOTSTRAP
# =========================================================


def log(msg):
    print(f"[AI-LAB] {msg}")


def bootstrap_system(base_path="."):
    log("Bootstrapping system...")


    for d in AI_LAB_KERNEL["directories"]:
        path = os.path.join(base_path, d)
        os.makedirs(path, exist_ok=True)
        log(f"Ensured directory: {path}")


    # artifacts/generated
    gen_path = os.path.join(base_path, "artifacts", "generated")
    os.makedirs(gen_path, exist_ok=True)


    # memory file
    mem_path = os.path.join(base_path, "memory", "template_cards.json")
    if not os.path.exists(mem_path):
        with open(mem_path, "w") as f:
            json.dump([], f)
        log("Created memory/template_cards.json")


    log("Bootstrap complete.")


# =========================================================
# 🧠 TASK CLASSIFICATION
# =========================================================


def classify_task(task):
    t = task.lower()


    if "pdf" in t or "guide" in t:
        return "pdf_guide"
    if "affidavit" in t or "legal" in t:
        return "legal_document"
    if "invoice" in t:
        return "invoice"
    if "slide" in t or "ppt" in t:
        return "pptx_slides"
    if "html" in t or "page" in t:
        return "html_page"


    return "report"


# =========================================================
# 🤖 LLM ADAPTER (OPTIONAL)
# =========================================================


def call_llm(prompt):
    try:
        import requests
        api_key = os.environ.get("OPENROUTER_API_KEY")


        if not api_key:
            raise Exception("No API key")


        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "openrouter/auto",
                "messages": [{"role": "user", "content": prompt}]
            }
        )


        return response.json()["choices"][0]["message"]["content"]


    except Exception as e:
        log(f"LLM fallback triggered: {e}")
        return f"[FALLBACK CONTENT]\n\n{prompt}"


# =========================================================
# 🏗 CONTENT STRUCTURING
# =========================================================


def structure_content(task, content):
    return {
        "id": str(uuid.uuid4()),
        "type": classify_task(task),
        "title": task[:60],
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }


# =========================================================
# 🎨 RENDERERS (STANDARD LIB ONLY BASELINE)
# =========================================================


def render_markdown(artifact):
    return f"# {artifact['title']}\n\n{artifact['content']}"


def render_html(artifact):
    return f"""
    <html>
    <head><title>{artifact['title']}</title></head>
    <body>
    <h1>{artifact['title']}</h1>
    <p>{artifact['content']}</p>
    </body>
    </html>
    """


def render_file(artifact, base_path="."):
    artifact_type = artifact["type"]


    filename = f"{artifact['id']}"


    if artifact_type == "html_page":
        content = render_html(artifact)
        ext = "html"
    else:
        content = render_markdown(artifact)
        ext = "md"


    path = os.path.join(base_path, "artifacts", "generated", f"{filename}.{ext}")


    with open(path, "w") as f:
        f.write(content)


    log(f"Artifact created: {path}")
    return path


# =========================================================
# 🧠 MEMORY SYSTEM
# =========================================================


def load_memory(base_path="."):
    path = os.path.join(base_path, "memory", "template_cards.json")
    with open(path, "r") as f:
        return json.load(f)


def save_memory(card, base_path="."):
    path = os.path.join(base_path, "memory", "template_cards.json")
    data = load_memory(base_path)
    data.append(card)


    with open(path, "w") as f:
        json.dump(data, f, indent=2)


    log("Memory updated.")


# =========================================================
# 🔄 AGENT LOOP (DOCTRINE ENFORCED)
# =========================================================


def run_agent(task, base_path="."):
    log(f"Starting task: {task}")


    # Query
    query_data = task


    # Enrichment (placeholder)
    enriched = query_data


    # LLM Drafting
    draft = call_llm(enriched)


    # Structuring
    artifact = structure_content(task, draft)


    # Rendering
    output_path = render_file(artifact, base_path)


    # Memory
    save_memory(artifact, base_path)


    # Delivery (placeholder)
    log("Delivery stage complete.")


    # Doctrine enforcement
    if DOCTRINE["REQUIRE_ARTIFACT"] and not os.path.exists(output_path):
        raise Exception("Doctrine violation: No artifact produced")


    return output_path


# =========================================================
# 🚀 CLI ENTRY
# =========================================================


if __name__ == "__main__":
    bootstrap_system()


    task = input("Enter task: ").strip()


    result = run_agent(task)


    log(f"Completed. Output: {result}")
