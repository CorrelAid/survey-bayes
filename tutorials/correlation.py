# %% [markdown] In diesem Tutorial wollen wir herausfinden ob es eine
# Korrelation zwischen der Variable Wohlfühlen ("Ich
# fühle mich bei TestWerk wohl und akzeptiert") und dem Net Promoter Score ("Würdest du Testwerk Freund*innen empfehlen") gibt.
# Wohlfühlen messen wir auf einer Skala von 1 ("Stimme gar nicht zu") bis 5 ("Stimme voll zu") und den Net Promoter Score (NPS) von 0 bis 10.

# %%
import arviz as az
import bambi as bmb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
data = pd.read_csv("../testwerk_responses.csv", delimiter=";")

# %%
#
# Als erstes schauen wir uns unsere Daten genauer an. Plotting ist hier oft die
# intuitivste Wahl.
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(data["wohlfuehlen"], bins=np.arange(6) + 0.5, edgecolor="white")
axes[0].set(
    xlabel="Wohlfühlen",
    ylabel="Anzahl",
    title="Verteilung Wohlfühlen",
    xticks=range(1, 6),
)
axes[1].hist(data["nps_score"], bins=np.arange(12) - 0.5, edgecolor="white")
axes[1].set(xlabel="NPS Score (0–10)", ylabel="Anzahl", title="Verteilung NPS Score")
plt.tight_layout()

# Wir sehen, dass sowohl Wohlfühlen als auch der NPS Score in diesem Datensatz eine
# kleine Varianz aufweisen und zu den positiven Werten neigen.

# %%
# Nun schauen wir uns den Zusammenhang zwischen den beiden an. (Jitter entlang beider
# Achsen, damit überlappende Punkte sichtbar werden)
fig, ax = plt.subplots()
ax.scatter(
    data["wohlfuehlen"] + np.random.uniform(-0.15, 0.15, size=len(data)),
    data["nps_score"] + np.random.uniform(-0.15, 0.15, size=len(data)),
    alpha=0.3,
)
ax.set(
    xlabel="Wohlfühlen (1–5)",
    ylabel="NPS Score (0–10)",
    title="Wohlfühlen vs. NPS Score",
)

# Auch wenn die Daten wenig Varianz aufzeigen, scheint es hier einen klaren, positiven
# Zusammenhang zwischen den beiden Variablen zu geben. Wer sich wohler fühlt, neigt eher
# dazu TestWerk weiter zu empfehlen, was ja auch nicht überraschend ist.


# %% [markdown]
# ## Statistisches Modell.
# Wie können wir diesen Zusammenhang nun statistisch modellieren und nachweisen?
# Zunächst brauchen wir ein statistisches Modell, das die beiden Variablen in Beziehung
# setzt.
#
# In diesem Fall bietet sich ein lineares Modell an, das beschreibt, dass der
# NPS Score ($n$) einer*s Teilnehmer*in sich aus dem Wert der Variable Wohlfühlen ($w$)
# und zufälligem Rauschen ($\epsilon$) berechnen lässt.
#
# $n = \beta_0 + \beta_1 w + \epsilon$
#
# Im Detail sagen wir, dass sich jeder NPS Wert $n$ zusammensetzt aus einer Konstante
# $\beta_0$, dem Wohlfühl Effekt $\beta_1 w$ und einem zufälligen Rauschen $\epsilon$.
# Die Werte pro Teilnehmer*in für $n$ und $w$ kennen wir aus unseren Daten. Die
# Variablen $\beta_0$ und $beta_1$ kennen wir nicht. Wir wollen deren Werte
# herausfinden. Da wir diese Werte in unserem kleinen Datensatz von 100 Teilnehmer*innen
# nicht mit Sicherheit bestimmen können, bekommen wir eine Schätzung dazu welche dieser
# Werte wahrscheinlich sind. Das ist die Posterior Verteilung.
#
# Uns interessiert insbesondere der Wert $\beta_1$. Er beschreibt welchen Einfluss
# Wohlfühlen auf den NPS Score hat.
#
# ToDo:  Prior werden ausgewählt
#
#

# %%
#
model = bmb.Model("nps_score ~ wohlfuehlen", data)
model.build()


# %%
idata = model.fit()

# %%
az.summary(idata, group="posterior")
