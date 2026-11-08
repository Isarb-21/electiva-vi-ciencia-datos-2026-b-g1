"""
Actividad opcional - Semana 13: Diseña un dashboard
Ciencia de Datos (CORHUILA) - Isabella Ramos Betancourt

Genera boceto_dashboard.png: boceto (wireframe) del tablero de producción y
calidad de una planta de marroquinería.

IMPORTANTE: es un BOCETO. Las formas y cifras dentro de los gráficos son
ILUSTRATIVAS (simuladas) y sólo muestran el tipo de gráfico y su ubicación;
no son registros reales de ninguna empresa.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

TEXTO, GRIS, GRIS_CLARO, FONDO = "#222222", "#b8bcc2", "#e6e8eb", "#f6f7f9"
ACENTO, BIEN, MAL = "#e8710a", "#2e7d32", "#c62828"

fig = plt.figure(figsize=(14, 8.6), dpi=150, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.axis("off")

def caja(x, y, w, h, fc=FONDO, ec=GRIS_CLARO):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.8",
                                fc=fc, ec=ec, lw=1.2))

# --- Encabezado y filtros (zona 1)
ax.text(2, 96.5, "Producción y calidad · Planta de marroquinería",
        fontsize=17, fontweight="bold", color=TEXTO, va="center")
ax.text(2, 92.8, "BOCETO · datos ilustrativos · meta y estado frente a la meta en cada KPI",
        fontsize=10, color="#555555", va="center")
for i, (et, val) in enumerate([("Fecha", "Últimas 12 semanas ▾"),
                               ("Planta", "Todas ▾"),
                               ("Producto", "Bolsos · Billeteras · Cinturones ▾")]):
    x = 2 + i * 31.5
    caja(x, 85.5, 30, 5, fc="white", ec=GRIS)
    ax.text(x + 1, 88, f"{et}:  {val}", fontsize=10, color=TEXTO, va="center")
ax.text(2, 83.6, "①  Filtros (segmentadores): afectan todos los elementos del tablero",
        fontsize=8.5, color="#777777", va="center")

# --- KPIs (zona 2)
kpis = [
    ("KPI 1 · Cumplimiento del plan", "96,4 %", "Meta ≥ 95 %", "▲ Cumple", BIEN),
    ("KPI 2 · Tasa de defectos", "4,1 %", "Meta ≤ 3 %", "▼ No cumple", MAL),
    ("KPI 3 · OEE (eficiencia global)", "72 %", "Meta ≥ 75 %", "▼ No cumple", MAL),
]
for i, (nom, val, meta, est, col) in enumerate(kpis):
    x = 2 + i * 32.7
    caja(x, 63, 31, 19, fc="white", ec=GRIS)
    ax.add_patch(plt.Rectangle((x, 63), 0.9, 19, fc=col, ec="none"))
    ax.text(x + 2.5, 79.2, nom, fontsize=10.5, color="#555555", va="center")
    ax.text(x + 2.5, 72, val, fontsize=30, fontweight="bold", color=TEXTO, va="center")
    ax.text(x + 2.5, 66, meta, fontsize=10, color="#555555", va="center")
    ax.text(x + 29, 66, est, fontsize=10, fontweight="bold", color=col, va="center", ha="right")
ax.text(2, 61, "②  Fila superior: KPIs en números grandes, cada uno con su meta y su estado",
        fontsize=8.5, color="#777777", va="center")

# --- Gráficos (zona 3), cada uno con su eje propio
def panel(x, y, w, h, titulo):
    caja(x, y, w, h, fc="white", ec=GRIS)
    ax.text(x + 1.5, y + h - 2.6, titulo, fontsize=10.5, fontweight="bold",
            color=TEXTO, va="center")
    a = fig.add_axes([(x + 4) / 100, (y + 8) / 100, (w - 6.5) / 100, (h - 14) / 100])
    for s in ("top", "right"):
        a.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        a.spines[s].set_color("#999999")
    a.tick_params(labelsize=8, colors="#555555")
    return a

sem = list(range(1, 13))
cumpl = [93, 94, 92, 95, 96, 94, 97, 95, 96, 98, 96, 96.4]
a1 = panel(2, 6, 36, 51, "Cumplimiento del plan por semana (KPI 1)")
a1.plot(sem, cumpl, color=ACENTO, lw=2.4, marker="o", ms=4, zorder=3)
a1.axhline(95, color="#777777", ls="--", lw=1.2); a1.text(12.2, 95.3, "Meta 95 %", fontsize=8, color="#555555", ha="right", va="bottom")
a1.set_ylim(88, 100); a1.set_xticks([1, 4, 8, 12]); a1.set_xlabel("Semana", fontsize=8.5)
a1.set_ylabel("% del plan", fontsize=8.5)

defectos = [("Costuras", 38), ("Acabado", 27), ("Color", 18), ("Herrajes", 11), ("Otros", 6)]
a2 = panel(39.5, 6, 29, 51, "Defectos por tipo (KPI 2)")
ys = list(range(len(defectos)))
a2.barh(ys, [v for _, v in defectos], color=[ACENTO, ACENTO, GRIS, GRIS, GRIS], height=0.65)
a2.set_yticks(ys); a2.set_yticklabels([n for n, _ in defectos], fontsize=9); a2.invert_yaxis()
a2.set_xlabel("Unidades con defecto", fontsize=8.5); a2.tick_params(axis="y", length=0)
a2.spines["left"].set_visible(False)

plantas = [("Planta A", 78), ("Planta B", 73), ("Planta C", 65)]
a3 = panel(71, 6, 27, 51, "OEE por planta (KPI 3)")
a3.bar([n for n, _ in plantas], [v for _, v in plantas],
       color=[GRIS, GRIS, ACENTO], width=0.55)
a3.axhline(75, color="#777777", ls="--", lw=1.2); a3.text(2.45, 75.8, "Meta 75 %", fontsize=8, color="#555555", ha="right")
a3.set_ylim(0, 100); a3.set_ylabel("OEE (%)", fontsize=8.5)

ax.text(2, 3.2, "③  Centro: una tendencia, una comparación por causa y una comparación por planta (una historia: "
        "¿cumplimos? ¿dónde falla la calidad? ¿dónde se pierde eficiencia?)",
        fontsize=8.5, color="#777777", va="center")
fig.savefig("/home/claude/13-week/boceto_dashboard.png", facecolor="white")
print("ok")
