def check_duplicate_endpoints(bp):
    """Controleer of één blueprint dubbele endpoint-namen bevat."""
    seen = set()
    duplicates = []

    for rule in bp.deferred_functions:
        try:
            endpoint = rule.__closure__[1].cell_contents
        except Exception:
            continue

        if endpoint in seen:
            duplicates.append(endpoint)
        else:
            seen.add(endpoint)

    if duplicates:
        raise AssertionError(
            f"❌ Dubbele endpoints gevonden in blueprint '{bp.name}': {duplicates}\n"
            f"➡️ Hernoem de functies, want Flask vereist unieke endpoint-namen."
        )



