import attr
from airflow.version import version as AIRFLOW_VERSION
from openlineage.airflow import __version__ as OPENLINEAGE_AIRFLOW_VERSION
from openlineage.client.facet import BaseFacet, DataQualityMetricsInputDatasetFacet
from typing import Optional, Dict


@attr.s
class AirflowVersionRunFacet(BaseFacet):
    operator: str = attr.ib()
    taskInfo: str = attr.ib()
    airflowVersion: str = attr.ib()
    openlineageAirflowVersion: str = attr.ib()

    @classmethod
    def from_task(cls, task):
        return cls(
            f'{task.__class__.__module__}.{task.__class__.__name__}',
            str(task.__dict__),
            AIRFLOW_VERSION,
            OPENLINEAGE_AIRFLOW_VERSION
        )


@attr.s
class AirflowRunArgsRunFacet(BaseFacet):
    externalTrigger: bool = attr.ib(default=False)


@attr.s
class ColumnMetric:
    nullCount: Optional[int] = attr.ib(default=None)
    distinctCount: Optional[int] = attr.ib(default=None)
    sum: Optional[float] = attr.ib(default=None)
    count: Optional[int] = attr.ib(default=None)
    min: Optional[float] = attr.ib(default=None)
    max: Optional[float] = attr.ib(default=None)
    quantiles: Optional[Dict[str, float]] = attr.ib(default=None)


@attr.s
class DataQualityDatasetFacet(BaseFacet):
    rowCount: Optional[int] = attr.ib(default=None)
    bytes: Optional[int] = attr.ib(default=None)
    columnMetrics: Dict[str, ColumnMetric] = attr.ib(factory=dict)

    def to_openlineage(self) -> DataQualityMetricsInputDatasetFacet:
        return DataQualityMetricsInputDatasetFacet(
            rowCount=self.rowCount,
            bytes=self.bytes,
            columnMetrics=self.columnMetrics
        )

    @staticmethod
    def _get_schema() -> str:
        return "https://github.com/OpenLineage/OpenLineage/tree/main/integration/airflow/openlineage/airflow/data-quality-dataset-facet.json"  # noqa
