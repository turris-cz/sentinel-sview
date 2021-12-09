from ...extensions import redis

from .aggregation_tools import AggregationToolbox
from .jobs import aggregate
from .tasks import Task


class Aggregation(Task, AggregationToolbox):
    JOB_FUNCTION = aggregate

    def suggest_recursive_aggregation(self, dry_run=False):
        if not self.period["source_period"]:
            return

        preceding_aggregation = Aggregation(
            self.data_type, self.period["source_period"]
        )
        preceding_aggregation.suggest_recursive_aggregation(dry_run=dry_run)
        self.suggest_aggregation(dry_run=dry_run)

    def suggest_aggregation(self, dry_run=False):
        """Enqueue a job when refresh is allowed or check its result when it is
        already enqueued.
        """
        refresh_ttl = redis.ttl(self.refresh_timeout_key)
        is_time_to_refresh = refresh_ttl <= 0  # -1 for no key, -2 for key with no ttl

        job_state = self.get_job_state()
        if job_state.is_alive():
            return (
                f"Skipping aggregation {self.data_type:^24s} {self.period['handle']:>11s} "
                f"(refresh_ttl={refresh_ttl}, status={job_state.status}, "
                f"job_id={job_state.id})"
            )

        if self.blocked_by_preceding_aggregations():
            return (
                f"Skipping aggregation {self.data_type:^24s} {self.period['handle']:>11s} "
                f"(refresh_ttl={refresh_ttl}) (blocked by ongoing aggregations)"
            )

        if is_time_to_refresh or job_state.is_failed():
            job_id = None if dry_run else self._queue_job()
            if dry_run or job_id:
                return (
                    f"Queueing aggregation {self.data_type:^24s} {self.period['handle']:>11s} "
                    f"(refresh_ttl={refresh_ttl}) "
                    f"status={job_state.status}) with id={job_id}"
                )
            else:  # Unable to acquire job lock - job must just started from another thread
                job_state = self.get_job_state()
                return (
                    f"Skipping aggregation {self.data_type:^24s} {self.period['handle']:>11s} "
                    f"(refresh_ttl={refresh_ttl}, status={job_state.status}, "
                    f"job_id={job_state.id}) (race condition)"
                )

        return (
            f"Skipping aggregation {self.data_type:^24s} {self.period['handle']:>11s} "
            f"(refresh_ttl={refresh_ttl}, status={job_state.status}, "
            f"job_id={job_state.id})"
        )

    def is_pending(self):
        if self.period["source_period"] is None:  # native period
            return False  # aggregation is never pending for native period
        job_state = self.get_job_state()
        return job_state.is_alive() or job_state.is_failed()

    def blocked_by_preceding_aggregations(self):
        if self.period["source_period"] is None:
            return False

        if self.period["source_period"]["source_period"] is None:
            return False

        preceding_aggregation = Aggregation(
            self.data_type, self.period["source_period"]
        )
        if preceding_aggregation.is_pending():
            return True

        return preceding_aggregation.blocked_by_preceding_aggregations()


def suggest_aggregation(data_type, target, dry_run=False):
    aggregation = Aggregation(data_type, target)
    return aggregation.suggest_aggregation(dry_run=dry_run)
