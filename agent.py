from tools import fetch_contract, static_analysis, ai_analysis
from logger import setup_logger

logger = setup_logger()

def decide_next_step(state):
    if state["code"] is None:
        return "fetch_contract"
    if state["issues"] is None:
        return "run_static"
    if state["analysis"] is None:
        return "run_ai"
    return "done"

def decide_next_step_ai(state):
    prompt = f"""
You are an AI agent controlling a smart contract analyzer.

Current state:
- code exists: {state["code"] is not None}
- issues exist: {state["issues"] is not None}
- analysis exists: {state["analysis"] is not None}

Rules:
- If code does NOT exist → fetch_contract
- If code exists but issues do NOT → run_static
- If issues exist but analysis does NOT → run_ai
- If everything exists → done

IMPORTANT:
- Do NOT repeat a step if it is already completed
- Always move forward

Return ONLY one word:
fetch_contract | run_static | run_ai | done
"""
    action = ai_analysis(prompt).strip().lower()
    valid = ["fetch_contract", "run_static", "run_ai", "done"]
    return action if action in valid else decide_next_step(state)

def run_agent(address):
    state = {
        "address": address,
        "code": None,
        "issues": None,
        "analysis": None
    }

    logger.info("🚀 Starting agent")

    while True:
        action = decide_next_step_ai(state)
        logger.info(f"🧠 Agent decided: {action}")

        if action == "fetch_contract":
            logger.info("📡 Fetching contract...")
            state["code"] = fetch_contract(state["address"])
            logger.debug(f"Code length: {len(state['code'])}")

        elif action == "run_static":
            logger.info("🔍 Running static analysis...")
            state["issues"] = static_analysis(state["code"])
            logger.info(f"Issues found: {len(state['issues'])}")
            logger.debug(f"Issues detail: {state['issues']}")

        elif action == "run_ai":
            logger.info("🧠 Running AI analysis...")
            prompt = f"Analyze vulnerabilities: {state['issues']}"
            state["analysis"] = ai_analysis(prompt)
            logger.debug(f"AI output: {state['analysis']}")

        elif action == "done":
            logger.info("🏁 Agent finished")
            break

    return state

def display_result(state):
    print("\n" + "="*50)
    print("📊 FINAL REPORT\n")

    print("⚠️ Issues:")
    for issue in state["issues"]:
        print(f"- {issue['type']} ({issue['severity']})")

    print("\n🧠 AI Analysis:")
    print(state["analysis"])
    print("="*50)
