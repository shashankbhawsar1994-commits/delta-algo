from delta_rest_client import DeltaRestClient
from delta_rest_client.delta_rest_client import OrderType

print("🔥 MAIN.PY LOADED")

# ==============================
# CONFIG
# ==============================
API_KEY = "wnTYvQTIV3t2H5buidO1NXQv1fiiuY"
API_SECRET = "3YMRGm72AWa9SfgewppE49VeJhrYNAZ57zJd3gviQImu7c4uHy04JM6uhRo0"
BASE_URL = "https://cdn-ind.testnet.deltaex.org"

PRODUCT_ID = 84   # BTCUSD
ORDER_SIZE = 1    # keep small for testing

# ==============================
# INITIALIZE CLIENT
# ==============================
delta_client = DeltaRestClient(
    base_url=BASE_URL,
    api_key=API_KEY,
    api_secret=API_SECRET
)

# ==============================
# GET CURRENT POSITION
# ==============================
def get_position_type():
    try:
        position = delta_client.get_position(product_id=PRODUCT_ID)
        size = position.get("size", 0)

        if size > 0:
            return "long"
        elif size < 0:
            return "short"
        else:
            return "none"

    except Exception as e:
        print("❌ Position error:", str(e))
        return "none"


# ==============================
# PLACE ORDER
# ==============================
def place_order(side):
    print("🔥 REAL ORDER FUNCTION CALLED")

    try:
        order = delta_client.place_order(
            product_id=PRODUCT_ID,
            size=ORDER_SIZE,
            side=side,                     # ✅ string ("buy"/"sell")
            order_type=OrderType.MARKET    # ✅ enum (THIS WORKS)
        )

        print("✅ Order placed:", order)

    except Exception as e:
        print("❌ Order error:", str(e))


# ==============================
# CLOSE POSITION
# ==============================
def close_position(current_position):
    print("🔥 CLOSE FUNCTION CALLED")

    try:
        if current_position == "long":
            side = "sell"
        elif current_position == "short":
            side = "buy"
        else:
            return

        order = delta_client.place_order(
            product_id=PRODUCT_ID,
            size=ORDER_SIZE,
            side=side,
            order_type=OrderType.MARKET,
            reduce_only=True   # 🔥 ensures only closing
        )

        print("✅ Position closed:", order)

    except Exception as e:
        print("❌ Close error:", str(e))


# ==============================
# MAIN SIGNAL HANDLER
# ==============================
def handle_signal(signal):
    current_position = get_position_type()

    print(f"\n📩 Signal: {signal}")
    print(f"📊 Current Position: {current_position}")

    if signal == "buy":
        if current_position == "short":
            close_position("short")
            place_order("buy")

        elif current_position == "none":
            place_order("buy")

        else:
            print("⚠️ Already LONG")

    elif signal == "sell":
        if current_position == "long":
            close_position("long")
            place_order("sell")

        elif current_position == "none":
            place_order("sell")

        else:
            print("⚠️ Already SHORT")

    else:
        print("❌ Unknown signal")