### Dominio 4. Machine Learning
Objetivo: desarrollar, entrenar, evaluar y ejecutar los modelos que predicen el comportamiento de los precios agrícolas.

Microservicios:

04-machine-learning/
│
├── feature-engineering-service/
│
├── model-training-service/
│
└── prediction-service/

1. Feature Engineering Service

Transforma los datos en variables para los modelos:
- Medias móviles.
- Variaciones históricas.
- Volatilidad.
- Indicadores climáticos.
- Estacionalidad.
- Variables económicas.
2. Model Training Service

Se encarga de:
- Preparar datasets.
- Entrenar modelos.
- Optimizar hiperparámetros.
- Evaluar resultados.
- Registrar experimentos.
- Publicar nuevas versiones de modelos.
3. Prediction Service

Se encarga de:
- Recibir solicitudes de predicción.
- Obtener las variables necesarias.
- Cargar el modelo aprobado.
- Ejecutar inferencias.
- Guardar resultados.
- Exponer predicciones mediante API.
Utilizaría Scikit-learn, XGBoost, MLflow y Optuna.

Flujo:

GOLD DATA
    |
    v
FEATURE ENGINEERING
    |
    v
MODEL TRAINING
    |
    v
MODEL REGISTRY
    |
    v
PREDICTION SERVICE
    |
    v
PREDICTION DATABASE