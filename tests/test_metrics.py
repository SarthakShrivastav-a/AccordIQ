from accordiq.services.metrics_service import quality_metrics

def test_quality_metrics():
    metrics = quality_metrics(10, 8, 5, 5)
    assert metrics["precision_proxy"] == 0.8
    assert metrics["groundedness"] == 1
