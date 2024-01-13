import unittest
from job import Job
from scheduler import Scheduler

class SchedulerTesting(unittest.TestCase):

    TESTING_INPUT = r"input\test_cases.txt"

    def check_case(
                self,
                jobs: list[Job],
                expected: tuple[float, float, float, float]
            ) -> None:
        """
        Checks any general case given an input Jobs list and expected turnaround
        times

        Parameters
        ----------
        jobs: list[Job]
            The input list to pass to all the selection methods
        expected: list[float, float, float, float]
            The value that each method should retrieve
        """

        scheduler = Scheduler(jobs)

        fcfs = scheduler.order_first_serve().process()
        sjf = scheduler.order_shortest().process()
        rr2 = scheduler.order_round_robin(2).process()
        rr5 = scheduler.order_round_robin(5).process()

        self.assertTrue(
            (
                fcfs,
                sjf,
                rr2,
                rr5
            ) == expected
        )

    def testcase_input(self) -> None:
        """
        Reads an input file for testcases.

        # comments and \n newlines will be ignored.

        The file must be structured as follows:

        BEGIN
        JobName JobTimeRequired
        JobName JobTimeRequired
        ...
        TURNAROUND fcfs sjf rr2 rr5
        END
        BEGIN
        ...
        ...

        When the "END" keyword is found, the collected Jobs will be tested on
        each scheduling algorithm

        Raises
        ------
        ValueError
            If any issues are found in the input file

        """
        # Read the file
        with open(self.TESTING_INPUT, 'r', encoding='utf-8') as f:
            file_contents = f.read().split("\n")

        # We do some typehinting
        jobs: list[Job] = []
        expected: tuple[float, float, float, float] | None = None
        for curr_identifier in file_contents:

            # Ignore comments and newlines
            if curr_identifier.startswith("#") or not curr_identifier:
                continue

            # Clear the input variables
            if curr_identifier == "BEGIN":
                jobs = []
                expected = None
                continue

            # An expected value has been found
            if curr_identifier.startswith("TURNAROUND"):
                try:
                    # The parsed values are turned into floats
                    _, p_fcfs, p_sjf, p_rr2, p_rr5 = curr_identifier.split(" ")
                    parsed = [p_fcfs, p_sjf, p_rr2, p_rr5]

                    # Round each float to 3 decimal places
                    fcfs, sjf, rr2, rr5 = list(
                        map(lambda x: round(float(x), 3), parsed)
                    )
                except:
                    raise ValueError(
                        "Something is wrong with the input file " +
                        "(hint: TURNAROUND)"
                    )

                expected = (fcfs, sjf, rr2, rr5)
                continue

            # Perform the testing
            if curr_identifier == "END":
                if not expected or not jobs:
                    raise ValueError(
                        "Something is wrong with the input file. " +
                        "(hint: Incomplete BEGIN or END)"
                    )
                self.check_case(jobs, expected)
                continue

            # Must be a job
            try:
                time_required: str | int
                job_name, time_required = curr_identifier.split(" ")
                time_required = int(time_required)
                jobs.append(Job(job_name, time_required))
            except:
                raise ValueError(
                    "Something is wrong with the input file. " +
                    "(hint: Incomplete Job Identifier)"
                )

        # If we still have unhandled values
        if not jobs or not expected:
            raise ValueError(
                "Something is wrong with the input file. " +
                "(hint: Incomplete BEGIN)"
            )


if __name__ == "__main__":
    unittest.main()