from __future__ import annotations
from random import randint

class Job:
    """
    Definitions and implementations for everything it takes to be a Job

    Fields such as the name and time required to complete are available on
    initialization. Additional fields, like the time elapsed so far,
    the time remaining, and the turnaround time (time of completion) for the
    Job are available through property methods and adjusted through setter
    methods
    """

    # An ID that will be incremented every time a Job is created
    running_id = 0

    def __init__(self, name: str, time_required: int) -> None:
        """
        Creates a Job given its name and the time required to complete it

        The job's ID will also be assigned here as the current value of the
        running_id field, and it will be incremented.

        Finally, the time_elapsed and turnaround_time fields will be filled as 0

        Parameters
        ----------
        name: str
            The name of the Job
        time_required: int
            The time required to complete this job
        """
        self.job_id = Job.running_id
        Job.running_id += 1

        self.name = name
        self.time_required = time_required

        self.time_elapsed = 0
        self.turnaround_time = 0

    def reset_job(self) -> None:
        """
        Resets a job to be used again with another Scheduler. Meaning, we will
        set the time_elapsed and turnaround_time values back to 0
        """
        self.time_elapsed = 0
        self.turnaround_time = 0

    @classmethod
    def create_random(
                cls,
                min_required: int = 5,
                max_required: int = 35
            ) -> Job:
        """
        Creates a Job with a random required time based on the given min and
        max values.

        The job's name will be "Job{}" where {} is the current value of the
        running_id field. When the initialization method is called, this
        ID will be incremented.

        Parameters
        ----------
        min_required: int = 5
            The minimum time required for completion
        max_required: int = 35
            The maximum time required for completion
        """
        return cls(
            f"Job{cls.running_id}",
            randint(min_required, max_required)
        )

    def spend_time(self, time_spent: int) -> None:
        """
        Spend a given amount of time on this Job

        Parameters
        ----------
        time_spent: int
            The time to spend on this job

        Raises
        ------
        ValueError
            If we will spend more time than necessary on this Job
        """
        if self.time_elapsed + time_spent > self.time_required:
            raise ValueError(
                f"The time_spent value {time_spent} given will spend more " +
                f"time on this job ({self.time_required}) than necessary " +
                f"({self.time_required - self.time_elapsed})"
            )

        self.time_elapsed += time_spent

    def set_turnaround_time(self, turnaround_time: int) -> None:
        """
        Sets the turnaround time of this job (meaning the job is now complete)
        only if the turnaround time has not already been set

        Parameters
        ----------
        turnaround_time: int
            The turnaround time to set to this job

        Raises
        ------
        ValueError
            If the job was not yet complete

        """
        if not self.is_complete:
            raise ValueError("This Job is not yet complete!")

        if not self.turnaround_time:
            self.turnaround_time = turnaround_time

    @property
    def time_remaining(self) -> int:
        """An int denoting the time remaining before this Job is complete"""
        return self.time_required - self.time_elapsed

    @property
    def is_complete(self) -> bool:
        """A bool denoting whether or not this Job has been completed"""
        return self.time_remaining <= 0

    def __str__(self) -> str:
        """
        Returns a properly formatted string representation of this Job

        Returns
        -------
        str
            Name (time_required ms)
        """
        return f"{self.name} ({self.time_required}ms)"

    def __repr__(self) -> str:
        """
        Returns a properly formatted string representation of this Job

        Returns
        -------
        str
            Name (time_elapsed/time_required ms)
        """
        return f"{self.name} ({self.time_elapsed}ms/{self.time_required}ms)"

    def __hash__(self) -> int:
        """
        Returns a hash value of the 'NameID' of the Job

        Returns
        -------
        int
            The hash value
        """
        return hash(f"{self.name}{self.job_id}")

    def __eq__(self, o: object) -> bool:
        """
        Checks equality between two Jobs.

        We simply check if the two names and Job IDs are equivalent

        Returns
        -------
        bool
            Whether or not the two Jobs are equal
        """
        return (
            isinstance(o, Job) and
            o.name == self.name and
            o.job_id == self.job_id
        )