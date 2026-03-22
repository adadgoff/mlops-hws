## API Documentation

### Overview

This document describes the REST API endpoints for the MLOps system. The API provides functionality for managing datasets, training and inference of machine learning models, and monitoring model performance.

### Endpoints

#### Health Check

- **Path**: `/health`
- **Method**: `GET`
- **Description**: Returns a simple health check response indicating the system is running
- **Response**: `{"status": "healthy"}`

#### Datasets

##### List Datasets

- **Path**: `/datasets`
- **Method**: `GET`
- **Description**: Returns a list of all available datasets
- **Response**: `[{"id": "string", "name": "string", "size": "number", "created_at": "string"}]`

##### Create Dataset

- **Path**: `/datasets`
- **Method**: `POST`
- **Description**: Creates a new dataset with the provided data
- **Request Body**: `{"name": "string", "data": "string"}`
- **Response**: `{"id": "string", "name": "string"}`

##### Get Dataset

- **Path**: `/datasets/{dataset_id}`
- **Method**: `GET`
- **Description**: Returns a specific dataset by ID
- **Response**: `{"id": "string", "name": "string", "size": "number", "created_at": "string"}`

##### Update Dataset

- **Path**: `/datasets/{dataset_id}`
- **Method**: `PUT`
- **Description**: Updates an existing dataset
- **Request Body**: `{"name": "string", "data": "string"}`
- **Response**: `{"id": "string", "name": "string"}`

##### Delete Dataset

- **Path**: `/datasets/{dataset_id}`
- **Method**: `DELETE`
- **Description**: Deletes a specific dataset
- **Response**: `{"message": "Dataset deleted successfully"}`

#### Model Training

##### Train Model

- **Path**: `/ml/train`
- **Method**: `POST`
- **Description**: Trains a machine learning model using the specified dataset and parameters
- **Request Body**: `{"dataset_id": "string", "model_type": "string", "parameters": {"key": "value"}}`
- **Response**: `{"model_id": "string", "status": "string", "training_log": "string"}`

##### Get Model

- **Path**: `/ml/models/{model_id}`
- **Method**: `GET`
- **Description**: Returns a specific model by ID
- **Response**: `{"id": "string", "name": "string", "type": "string", "status": "string", "created_at": "string"}`

##### List Models

- **Path**: `/ml/models`
- **Method**: `GET`
- **Description**: Returns a list of all available models
- **Response**: `[{"id": "string", "name": "string", "type": "string", "status": "string"}]`

#### Model Inference

##### Inference

- **Path**: `/ml/inference`
- **Method**: `POST`
- **Description**: Performs inference using a trained model with the provided input data
- **Request Body**: `{"model_id": "string", "input_data": "string"}`
- **Response**: `{"model_id": "string", "prediction": "string", "confidence": "number"}`

#### Metrics

##### Get Metrics

- **Path**: `/ml/metrics`
- **Method**: `GET`
- **Description**: Returns performance metrics for a specific model
- **Request Query Parameters**: `model_id=string`
- **Response**: `{"model_id": "string", "metrics": {"accuracy": "number", "precision": "number", "recall": "number", "f1_score": "number"}}`

##### Update Metrics

- **Path**: `/ml/metrics`
- **Method**: `PUT`
- **Description**: Updates model metrics with new values
- **Request Body**: `{"model_id": "string", "metrics": {"accuracy": "number", "precision": "number", "recall": "number", "f1_score": "number"}}`
- **Response**: `{"model_id": "string", "metrics": {"accuracy": "number", "precision": "number", "recall": "number", "f1_score": "number"}}`

### Error Handling

All endpoints return standardized error responses in JSON format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "string"
  }
}
```

Common error codes:

- `400`: Bad request - invalid input data
- `404`: Not found - requested resource doesn't exist
- `409`: Conflict - resource already exists
- `500`: Internal server error - unexpected server error

### Request/Response Examples

#### Example: Train Model

**Request**:

```json
{
  "dataset_id": "ds_123",
  "model_type": "classification",
  "parameters": {
    "max_depth": 5,
    "min_samples_split": 2
  }
}
```

**Response**:

```json
{
  "model_id": "ml_456",
  "status": "training",
  "training_log": "Training started at 2026-03-22T09:00:00Z"
}
```

#### Example: Inference

**Request**:

```json
{
  "model_id": "ml_456",
  "input_data": "[1.2, 3.4, 5.6]"
}
```

**Response**:

```json
{
  "model_id": "ml_456",
  "prediction": "1",
  "confidence": 0.98
}
```

### Security

- All endpoints require authentication via Bearer token in the Authorization header
- Token is generated upon user login and expires after 30 minutes
- Rate limiting is applied to prevent abuse (100 requests per minute per user)

### Versioning

The API is versioned at the path level. The current version is v1.

**Base URL**: `https://api.mlops.example.com/v1`

### Future Endpoints

- `/ml/versions` - Get model version history
- `/ml/compare` - Compare two models
- `/ml/evaluation` - Perform model evaluation with custom metrics

### Notes

- All data is stored in MinIO with version control via DVC
- Model training logs are stored in ClearML
- All responses are returned with appropriate HTTP status codes
- The system supports both JSON and CSV data formats for datasets
- Model parameters can be customized per model type
- Training status is updated in real-time via webhooks
- Metrics are automatically collected during training and inference

### New /metrics Endpoint

The new `/metrics` endpoint provides real-time performance metrics for models.

- **Path**: `/ml/metrics`
- **Method**: `GET`
- **Description**: Returns real-time performance metrics for a specific model
- **Request Query Parameters**: `model_id=string` (required)
- **Response**: `{"model_id": "string", "metrics": {"accuracy": "number", "precision": "number", "recall": "number", "f1_score": "number"}, "timestamp": "string"}`
- **Rate Limit**: 1 request per second per model
- **Use Case**: Real-time monitoring of model performance during inference
- **Implementation**: Metrics are collected from the model's inference pipeline and stored in a real-time database
- **Data Source**: Metrics are derived from the model's internal state during inference
- **Error Handling**: Returns 404 if model_id is invalid or 500 if there's a database error
- **Security**: Requires authentication and authorization to access metrics
- **Caching**: Results are cached for 30 seconds to reduce database load
- **Scalability**: Designed to handle thousands of concurrent requests
- **Monitoring**: System logs all metric collection attempts and failures

This endpoint enables real-time monitoring of model performance, allowing operators to detect performance degradation or anomalies immediately.
