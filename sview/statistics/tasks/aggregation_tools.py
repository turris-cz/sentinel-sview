from .periods import AGGREGATION_PERIODS
from .queries.sql.aggregation import aggregation_queries
from .tasks import TaskToolbox


class AggregationToolbox(TaskToolbox):
    REDIS_JOB_PREFIX = "sview_job_id_aggr"
    REDIS_REFRESH_TO_PREFIX = "sview_aggregation_timeout"
    AVAILABLE_QUERIES = aggregation_queries
    AVAILABLE_PERIODS = AGGREGATION_PERIODS

    def __init__(self, data_type, period, params={}):
        self.name = data_type
        self.period = period
        self.data_type = data_type
        self.query = {"query": aggregation_queries[data_type]}
        self.params = params  # to have compatible interface with ResourceToolbox

        super().__init__()

    def get_destination_table(self):
        return f"{self.data_type}_{self.period['handle']}".strip("_")

    def get_query(self):
        """Mainly to insert table name"""
        return self.query["query"].format(
            source_table=self.get_source_table(),
            destination_table=self.get_destination_table(),
        )
