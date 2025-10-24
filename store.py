# Shared in-memory store for orders and states.
ordini = {}   # user_id -> {pizza_name: qty}
stati = {}    # user_id -> state string (indirizzo, telefono, orario, None)
