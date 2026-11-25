# pyright: reportUndefinedVariable=false
# EXAMPLE 10 · Ingredients missing from the shopping list
# Original file: ../src/10_shopping_list_weaviate_opik_hermes.py
# What it shows: Calculate, save and add pending ingredients.
# LLM: NOT involved in this function; Hermes has already generated the menu.
# Python: normalize, avoid duplicates and calculate missing / included.
# Important: "missing" means absent from the LIST, not absent from the pantry.
# Read Snippet: Context actions and full nodes are in src/.

@track(name="calculate_missing_ingredients", type="tool", capture_input=False, capture_output=False)
def calculate_missing_ingredients(plan: dict, shopping_list: list[str]) -> dict:
    """Compare key ingredients with YA products listed in the shopping list.

    He does not estimate stocks in the pantry or quantities; only presence in the list.
    """
    by_key = {}
    listed = {normalize_words(p) for p in shopping_list}
    for day in DAYS:
        for meal in MEALS:
            recipe = plan.get("days", {}).get(day, {}).get(meal)
            if not recipe:
                continue
            for item in recipe.get("ingredientesClave", "").split(";"):
                name = item.strip().lower()
                normalized = normalize_words(name)
                if normalized and normalized not in by_key:
                    by_key[normalized] = name
    missing = [v for k, v in by_key.items() if k not in listed]
    included = [v for k, v in by_key.items() if k in listed]
    opik_context.update_current_span(
        metadata={"required_products": len(by_key), "missing_from_list": len(missing)}
    )
    return {"missing": missing, "included": included, "total": len(by_key)}


# 2. QUERY: Fragment of missing_ingredients_node().
# Query does not modify shopping_list - just prepare the response and save
# the displayed items so that the next message can reference them.
info = calculate_missing_ingredients(plan, state.get("shopping_list", []))
last_shown_products = info["missing"].copy()
# The node returns this information to LangGraph:
# {"last_shown_products": last_shown_products, "last_context": "missing_ingredients", ...}


# 3. FOLLOW-UP: Fragment of add_missing_node().
# The original code verifies that the user refers to the displayed products
# and revalidate which ones are still missing before calling the tool. If the user
# directly asks to complete the menu, the node uses info["missing"].
shown = state.get("last_shown_products", [])
current_missing = {normalize_words(p) for p in info["missing"]}
to_add = [p for p in shown if normalize_words(p) in current_missing]

# Only if the user asks to add them, the node executes:
updated = add_products.invoke({
    "shopping_list": state.get("shopping_list", []),
    "products": to_add,
    "last_product": state.get("last_product", ""),
})
