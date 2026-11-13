from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import time
from collections.abc import Generator

from .runner import Runner
from .. import logger


class ParallelRunner(Runner):
    def __init__(
        self, runner: callable, interval: float, timeout: float, num_parallel: int
    ) -> None:
        self.timeout = timeout
        self.interval = interval
        self.runner = runner
        self.num_parallel = num_parallel

    def _run_one(self, idx: int, message: str):
        try:
            results = list(self.runner(self, [message]))
            return results
        except BaseException as e:
            logger.log("Exception occured in runner {}: {}".format(idx, e))
            raise

    def _run_batched(self, messages: list[str]) -> Generator[list[str], None, None]:
        test_idxs = list(range(len(messages)))
        all_results = []
        retry_count = -1

        while len(test_idxs) > 0:
            num_requests = len(test_idxs)
            retry_count += 1
            if retry_count > 0:
                logger.log(
                    "Retrying {} failed tests: {}".format(num_requests, test_idxs)
                )

            if len(test_idxs) == 1:
                idx = test_idxs[0]
                try:
                    results = self._run_one(idx, messages[idx])
                    for result in results:
                        all_results.append({"idx": idx, "result": result})
                    test_idxs.remove(idx)
                except BaseException:
                    time.sleep(max(1.0, self.interval))
                continue

            futures = []
            with ThreadPoolExecutor(max_workers=len(test_idxs)) as executor:
                for idx in list(test_idxs):
                    prompt = messages[idx]
                    futures.append((idx, executor.submit(self._run_one, idx, prompt)))
                    if idx != test_idxs[-1]:
                        time.sleep(self.interval)

                for idx, future in futures:
                    try:
                        results = future.result(timeout=self.timeout)
                        for result in results:
                            all_results.append({"idx": idx, "result": result})
                        test_idxs.remove(idx)
                    except FuturesTimeoutError:
                        logger.log(f"Runner {idx} timed out after {self.timeout}s")
                    except BaseException:
                        pass

        all_results.sort(key=lambda r: r["idx"])
        for result in [r["result"] for r in all_results]:
            yield result

    def run(
        self,
        messages: list[str],
    ) -> Generator[list[str], None, None]:
        for start in range(0, len(messages), self.num_parallel):
            end = min(start + self.num_parallel, len(messages))
            batch = messages[start:end]

            for result in self._run_batched(batch):
                yield result
