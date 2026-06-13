# MCP Tool Server 1 - Calculator
# Handles any Numerical Reasoning the Agent needs

import math

def calculate(expression: str) -> dict:

    """
    Safely evaluates a mathematical expression.
    Examples: "2 + 2", "sqrt(144)", "1500 * 0.07", "log(1000)"
    """
    try:
        # Safe Evaluation - only Math functions allowed, no exec/eval abuse
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        allowed["abs"] = abs
        allowed["round"] = round

        result = eval(expression, {"__builtins__": {}}, allowed)
        return {
            "tool": "calculator",
            "expression": expression,
            "result": result,
            "status": "success"
        }
    except Exception as e:
        return {
            "tool": "calculator",
            "expression": expression,
            "result": None,
            "satus": f"error: {str(e)}"
        }
    

def run(params: dict) -> dict:
    expression = params.get("expression", "")
    return calculate(expression)