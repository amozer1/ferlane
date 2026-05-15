from utils.loader import load_programme_data
from utils.classifications import classify_float
from utils.analytics import compute_kpis
from core.commentary_engine import generate_commentary

def build_dashboard():

    cl31, cl32 = load_programme_data()

    cl32 = classify_float(cl32)

    kpis = compute_kpis(cl32)

    commentary = generate_commentary(cl31, cl32, kpis)

    return {
        "cl31": cl31,
        "cl32": cl32,
        "kpis": kpis,
        "commentary": commentary
    }