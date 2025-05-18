## Documentació del flux complet: Sol·licitud → Obtenció de ruta → Enviament d’instruccions → Tracking

### 🌟 Objectiu

Documentar el flux complet que permet al Controller sol·licitar una ruta, rebre-la, transmetre les instruccions al vehicle i fer-ne el seguiment, garantint robustesa, rendiment i traçabilitat.

---

### ✉️ 1. Sol·licitud de ruta

#### ▶ Iniciador: Controller

#### ▶ Destinatar: Servei de Rutes (API REST o Microservei)

**Dades enviades:**

* Origen: coordenades (X,Y)
* Destí: coordenades (X,Y)

**Exemple de petició HTTP:**

```http
POST /api/routes
Content-Type: application/json
{
  "origin": { "X": 41.223, "Y": 1.726 },
  "destination": { "X": 41.225, "Y": 1.729 }
}
```

**Resposta esperada (<500ms):**

```json
{
  "route": [
    {"X": 41.223, "Y": 1.726},
    {"X": 41.224, "Y": 1.727},
    {"X": 41.225, "Y": 1.729}
  ],
  "status": "ok"
}
```

#### Logs:

* `INFO [Controller] Sol·licitada ruta ORIGEN -> DESTI`
* `DEBUG [RoutesService] Ruta generada en 412ms`

---

### 🚗 2. Enviament d'instruccions al vehicle

#### ▶ Iniciador: Controller

#### ▶ Destinatar: Vehicle (via MQTT o API de comunicació directa)

**Contingut:**

* Llista de punts amb coordenades
* Opcional: paràmetres de velocitat o temps

**Format exemple:**

```json
{
  "_id": "C3",
  "instructions": [
    {"X": 41.223, "Y": 1.726},
    {"X": 41.224, "Y": 1.727},
    {"X": 41.225, "Y": 1.729}
  ]
}
```

**Logs:**

* `INFO [Controller] Instruccions enviades a vehicle C3`
* `DEBUG [MQTT] Missatge publicat a topic /vehicle/C3/route`

---

### 📊 3. Seguiment i tracking

#### ▶ Iniciador: Vehicle

#### ▶ Destinatar: Controller + Sistema de monitorització (Prometheus / Grafana)

**Tracking en temps real:**

* Coordenades actuals cada X segons
* Estat (en ruta, aturat, desviat, error)

**Exemple de dades publicades:**

```json
{
  "_id": "C3",
  "status": "Solicitat",
  "current_position": {"X": 41.224, "Y": 1.727}
}
```

**Logs:**

* `INFO [Tracking] Vehicle C3 passant per punt 2/3`
* `WARN [Tracking] Desviació detectada. Distància > 10m`

---

### ⚠️ 4. Gestó d'errors

**Si el servei de rutes falla:**

* El Controller rep un error:

```json
{
  "error": "no_route_found",
  "message": "No s'ha pogut generar una ruta vàlida."
}
```

* **Accions:**

  * Mostrar error a interfície
  * Reintentar amb ruta alternativa
  * Registrar l'error per a depuració

**Logs:**

* `ERROR [RoutesService] Error generant ruta: no_route_found`
* `INFO [Controller] Ruta alternativa sol·licitada`

---

### 📑 5. Registre i traçabilitat

* Totes les peticions/respostes es guarden (DB o fitxer log)
* Es generen **traces Prometheus/Grafana** per:

  * Temps de resposta del servei de rutes
  * Moviments de cada vehicle
  * Errors i desviacions

**Logs:**

* `METRIC route_request_duration_seconds{status="ok"} 0.412`
* `METRIC vehicle_tracking_events_total{vehicle="C3"} 12`

---

### 🔹 Conclusions

Aquest flux assegura:

* Integració robusta entre Controller i sistema de rutes
* Moviment precís dels vehicles segons instruccions
* Traçabilitat completa amb logs i mètriques
* Preparació per a demo amb petició i seguiment en temps real

