# pyright: reportUndefinedVariable=false
# EXEMPLE 10 · Ingredients que falten a la llista de compra
# Fitxer original: ../src/10_shopping_list_weaviate_opik_hermes.py
# Què mostra: calcular, guardar i afegir els ingredients pendents.
# LLM: NO intervé en aquesta funció; Hermes ja ha generat el menú.
# Python: normalitza, evita duplicats i calcula missing / included.
# Important: "missing" vol dir absent de la LLISTA, no absent del rebost.
# Fragment de lectura: les accions contextuals i els nodes complets són a src/.

@track(name="calculate_missing_ingredients", type="tool", capture_input=False, capture_output=False)
def calculate_missing_ingredients(plan: dict, shopping_list: list[str]) -> dict:
    """Compara ingredientesClave con productos YA apuntados en la lista de compra.

    No estima existencias en la despensa ni cantidades; solo presencia en la lista.
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


# 2. CONSULTA: fragment de missing_ingredients_node().
# Consultar no modifica shopping_list: només prepara la resposta i guarda
# els elements mostrats perquè el següent missatge hi pugui fer referència.
info = calculate_missing_ingredients(plan, state.get("shopping_list", []))
last_shown_products = info["missing"].copy()
# El node retorna aquesta informació a LangGraph:
# {"last_shown_products": last_shown_products, "last_context": "missing_ingredients", ...}


# 3. ACCIÓ POSTERIOR: fragment d'add_missing_node().
# El codi original comprova que l'usuari es refereix als productes mostrats
# i torna a validar quins encara falten abans de cridar l'eina. Si l'usuari
# demana directament completar el menú, el node usa info["missing"].
shown = state.get("last_shown_products", [])
current_missing = {normalize_words(p) for p in info["missing"]}
to_add = [p for p in shown if normalize_words(p) in current_missing]

# Només si l'usuari demana afegir-los, el node executa:
updated = add_products.invoke({
    "shopping_list": state.get("shopping_list", []),
    "products": to_add,
    "last_product": state.get("last_product", ""),
})
