"""
Actividad opcional - Semana 12: Rediseña un gráfico
Ciencia de Datos (CORHUILA) - Isabella Ramos Betancourt

Genera las dos imágenes de la entrega:
  antes.png   -> gráfico deficiente (torta 3D, 8 porciones, sin título)
  despues.png -> gráfico rediseñado (barras ordenadas, título con conclusión)

DATOS ILUSTRATIVOS (simulados): fallas de motores de una planta por causa,
12 meses, n = 140. No corresponden a registros de una empresa real.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

causas = [
    ("Rodamientos", 44),
    ("Sobrecalentamiento", 33),
    ("Desalineación del eje", 22),
    ("Aislamiento eléctrico", 15),
    ("Lubricación deficiente", 11),
    ("Sobrecarga", 7),
    ("Desbalance", 5),
    ("Otras", 3),
]
nombres = [c for c, _ in causas]
valores = [v for _, v in causas]
total = sum(valores)
assert total == 140

# ---------------------------------------------------------------- ANTES
colores_arcoiris = ["#ff0000", "#00c000", "#0000ff", "#ffff00",
                    "#ff00ff", "#00ffff", "#ff8000", "#8000ff"]
fig, ax = plt.subplots(figsize=(9, 6), dpi=150)
profundidad = 0.12
for k in range(12, 0, -1):           # capas oscuras = efecto 3D
    ax.pie(valores, colors=["#333333"] * len(valores), startangle=30,
           center=(0, -profundidad * k / 12), radius=1.0,
           wedgeprops=dict(edgecolor="#333333", linewidth=0.3))
wedges, _, autotexts = ax.pie(
    valores, colors=colores_arcoiris, startangle=30, autopct="%1.0f%%",
    pctdistance=0.7, explode=[0.06] * len(valores),
    wedgeprops=dict(edgecolor="black", linewidth=1),
    textprops=dict(fontsize=9, color="black"))
ax.set_aspect(0.6)                    # aplastar = perspectiva
ax.legend(wedges, nombres, loc="center left", bbox_to_anchor=(1.0, 0.5),
          fontsize=9)
fig.savefig("antes.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

# -------------------------------------------------------------- DESPUÉS
GRIS, NARANJA, TEXTO = "#b8bcc2", "#e8710a", "#222222"
fig, ax = plt.subplots(figsize=(10, 5.8), dpi=150)
y = list(range(len(causas)))
cols = [NARANJA if i < 2 else GRIS for i in y]
ax.barh(y, valores, color=cols, height=0.65, zorder=3)
ax.set_yticks(y)
ax.set_yticklabels(nombres, fontsize=11, color=TEXTO)
ax.invert_yaxis()                     # mayor arriba
ax.set_xlim(0, 52)                    # escala honesta: desde 0
for i, v in enumerate(valores):
    ax.text(v + 0.6, i, f"{v}  ({v / total:.0%})", va="center",
            fontsize=11, color=TEXTO,
            fontweight="bold" if i < 2 else "normal")
ax.set_xlabel("Número de fallas registradas (12 meses)", fontsize=10,
              color="#555555")
ax.xaxis.grid(True, color="#e6e6e6", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.spines["bottom"].set_color("#999999")
ax.tick_params(axis="y", length=0)
ax.tick_params(axis="x", colors="#555555")
fig.text(0.02, 0.96,
         "Rodamientos y sobrecalentamiento causan el 55 % de las fallas de motores",
         fontsize=15, fontweight="bold", color=TEXTO, ha="left", va="top")
fig.text(0.02, 0.905,
         "Fallas de motores por causa, últimos 12 meses (n = 140). "
         "Datos ilustrativos.",
         fontsize=10.5, color="#555555", ha="left", va="top")
fig.subplots_adjust(left=0.24, right=0.97, top=0.84, bottom=0.12)
fig.savefig("despues.png", facecolor="white")
plt.close(fig)

print("Total:", total,
      "| Top 2:", sum(valores[:2]), f"({sum(valores[:2]) / total:.1%})",
      "| Top 3:", sum(valores[:3]), f"({sum(valores[:3]) / total:.1%})")
