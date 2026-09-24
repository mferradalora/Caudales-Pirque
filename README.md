# 📊 Monitoreo de Caudales Canal Pirque

Visualización de caudales reportados en las estaciones del Canal Pirque.

```mermaid
graph LR
    Sirene["Canal Matriz Sirene"] --> LC

    %% Marcos (Encasillados)
    LC["┌──────────────┐<br>│  La Cuncuna  │<br>└──────────────┘"]
    MB["┌──────────┐<br>│  Marco B │<br>└──────────┘"]
    MC["┌──────────┐<br>│  Marco C │<br>└──────────┘"]

    %% Derivaciones desde La Cuncuna
    LC -- "Caida Puntilla" --> MB
    LC -- "MSR01 → MSR02 → MSR03 → MSR19" --> CSR["Canal Santa Rita"]

    %% Derivaciones desde Marco B
    MB -- "Canal Cruceral - El Llano" --> MC
    MB -- "MLI01 → MLI15" --> CLI["Canal La Isla"]

    %% Derivaciones desde Marco C
    MC -- "MCL01 → MCL07" --> CEC["Canal El Cruceral"]
    MC -- "MEL01 → MEL09" --> CEL["Canal El Llano"]
```

> *Los gráficos se actualizan diariamente.*

---

## Clon MarcoB

![Clon MarcoB](graficos/Clon_MarcoB.png)

---

## MEL 1

![MEL 1](graficos/MEL_1.png)

---

## MEL 4

![MEL 4](graficos/MEL_4.png)

---

## MEL 6

![MEL 6](graficos/MEL_6.png)

---

## MLI 1

![MLI 1](graficos/MLI_1.png)

---

## MLI15

![MLI15](graficos/MLI15.png)

---

## MSR 12

![MSR 12](graficos/MSR_12.png)

---

## MSR 16

![MSR 16](graficos/MSR_16.png)

---

## MSR 17

![MSR 17](graficos/MSR_17.png)

---

## MSR 19

![MSR 19](graficos/MSR_19.png)

---

## Marco C

![Marco C](graficos/Marco_C.png)

---

## Marco La Cuncuna

![Marco La Cuncuna](graficos/Marco_La_Cuncuna.png)

---

## MarcoB

![MarcoB](graficos/MarcoB.png)

---

