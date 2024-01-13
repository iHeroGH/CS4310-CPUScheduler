from __future__ import annotations
from enum import Enum
from job import Job

class Ordering(Enum):
    """
    A simple enumeration denoting the 3 different ways a list of Jobs can
    be processed

    The available Ordering methods are First-Come-First-Serve, Shortest-Job-First
    and Round-Robin (which will require an additional field for the time-slice).
    """

    FCFS = 0
    SJF = 1
    RR = 2

class Scheduler:
    """
    Definitions and implementations for everything it takes to be a Schedule

    The general workflow of using this Scheduler is as follows:
    A list of jobs will be provided, an ordering method will be chosen (via
    the order_* methods), and the jobs will be process()-ed

    It is dangerous to manually adjust the schedule or ordering_method field
    without going through the proper order_* method.
    """

    def __init__(self, jobs: list[Job] = []) -> None:
        """
        Initializes a Scheduler with a list of jobs.

        Initially, the schedule will be composed of the jobs list given in the
        order they are given, and the ordering method used will be FCFS.

        This can be changed by calling each ordering method's respective
        order_* method.

        Parameters
        ----------
        jobs: list[Job] = []
            Either an empty list or a list of Jobs
        """
        self.jobs: list[Job] = jobs
        self.schedule: list[Job] = [job for job in jobs]
        self.ordering_method: Ordering = Ordering.FCFS
        self.rr_time: int = 0 # Must be provided if we are using Ordering.RR

    @classmethod
    def create_random(cls, num_jobs: int = 5) -> Scheduler:
        """
        Creates num_jobs random jobs and creates a Scheduler out of it

        This relies on the Job.create_random() classmethod and its respective
        default parameters

        Parameters
        ----------
        num_jobs: int = 5
            The number of random jobs to create

        Returns
        -------
        Scheduler
            The Scheduler object created
        """
        jobs = [Job.create_random() for _ in range(num_jobs)]
        return cls(jobs)

    def add_job(self, job: Job) -> None:
        """
        Adds a Job to the existing list of Jobs. Adding a Job to the Jobs list
        twice has unpredictable behavior, but is not disallowed.

        Whatever order_* method is requested will not need to be recalled.

        Parameters
        ----------
        job: Job
            The Job to add to the list
        """
        self.jobs.append(job)

        match(self.ordering_method):
            case Ordering.FCFS:
                self.order_first_serve()
                return
            case Ordering.SJF:
                self.order_shortest()
                return
            case Ordering.RR:
                self.order_round_robin(self.rr_time)
                return

    def order_first_serve(self) -> Scheduler:
        """
        Orders the schedule by first-come-first-serve

        This just sets the schedule to the exact order given by the jobs list

        Returns
        -------
        Scheduler
            This scheduler object. Helpful for chaining the process method onto
            the ordering method
        """
        self.schedule = [job for job in self.jobs]
        self.ordering_method = Ordering.FCFS

        return self

    def order_shortest(self) -> Scheduler:
        """
        Orders the schedule by sorting the jobs by their time required

        Returns
        -------
        Scheduler
            This scheduler object. Helpful for chaining the process method onto
            the ordering method
        """
        self.schedule.sort(key = lambda job: job.time_required)
        self.ordering_method = Ordering.SJF

        return self

    def order_round_robin(self, time_slice: int) -> Scheduler:
        """
        Orders the schedule by first-come-first and sets a round-robin
        time-slice

        Parameters
        ----------
        time_slice: int
            The time_slice to give each Job

        Returns
        -------
        Scheduler
            This scheduler object. Helpful for chaining the process method onto
            the ordering method
        """
        self.schedule = [job for job in self.jobs]
        self.rr_time = time_slice
        self.ordering_method = Ordering.RR

        return self

    def _pre_process(self, log: bool = False) -> None:
        """
        Does some pre-processing on the schedule to ensure everything is
        in order before fully processing.

        Mainly, we ensure that a valid time-slice is provided for round-robin
        scheduling, and reset the counts of every Job

        Parameters
        ----------
        log: bool = False
            Whether or not to log (print) the pre-processing process

        Raises
        ------
        ValueError
            If the ordering method is round-robin but the time-slice is 0
        """

        # Time-Slice check
        if self.ordering_method == Ordering.RR:
            if not self.rr_time:
                raise ValueError("A valid Round-Robin time-slice was not set.")

        if log:
            print("Scheduling Jobs (in this order):")

        # Job checks
        for job in self.schedule:
            job.reset_job()
            if log:
                print(job)

        if log:
            print()

    def process(self, log: bool = False) -> float:
        """
        Does the actual processing for each job, and returns the average
        turnaround time

        Parameters
        ----------
        log: bool = False
            Whether or not to log (print) the processing process

        Returns
        -------
        float
            The average turn-around time for all the jobs
        """

        self._pre_process(log)

        total_time_elapsed = 0
        jobs_complete: set[Job] = set()
        while len(jobs_complete) != len(self.schedule):
            for job in self.schedule:

                # Skip complete job
                if job.is_complete:
                    continue

                # Before processing
                if log:
                    print(repr(job))

                # Process this job
                # We either spend the duration of the time needed by the process
                # or the round-robin time slice if we're using that ordering
                # method. However, a job cannot take longer than it needs to
                # so the minimum of those two values is chosen
                time_to_spend = min(
                    self.rr_time if self.ordering_method == Ordering.RR
                    else job.time_remaining,
                    job.time_remaining
                )
                job.spend_time(time_to_spend)
                total_time_elapsed += time_to_spend

                # After processing
                if log:
                    print(repr(job), "Total time so far: ", total_time_elapsed)
                    print("------")

                # If the job becomes complete
                # set_turnaround_time will not set the turnaround time if it's
                # already been set before, so this is safe
                if job.is_complete:
                    jobs_complete.add(job)
                    job.set_turnaround_time(total_time_elapsed)

        average_turnaround = sum(
            [j.turnaround_time for j in self.jobs]
        )/len(self.jobs)

        # Print the statistics
        if log:
            print("Jobs Complete.")
            print(f"Total Time Spent: {total_time_elapsed}ms")
            print(
                "Average Turnaround Time: " +
                f"{average_turnaround:.4}ms"
            )

        return average_turnaround