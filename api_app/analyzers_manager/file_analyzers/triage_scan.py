# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import logging
import time

import requests

from api_app.analyzers_manager import classes
from api_app.exceptions import AnalyzerConfigurationException, AnalyzerRunException
from tests.mock_utils import MockResponse, if_mock_connections, patch

logger = logging.getLogger(__name__)


class TriageScanFile(classes.FileAnalyzer):
    # using public endpoint as the default url
    base_url: str = "https://api.tria.ge/v0/"
    private_url: str = "https://private.tria.ge/api/v0/"
    report_url: str = "https://tria.ge/"

    def set_params(self, params):
        self.endpoint = params.get("endpoint", "public")
        if self.endpoint == "private":
            self.base_url = self.private_url

        self.__api_key = self._secrets["api_key_name"]
        self.report_type = params.get("report_type", "overview")
        if self.report_type not in ["overview", "complete"]:
            raise AnalyzerConfigurationException(
                f"report_type must be 'overview' or 'complete' "
                f"but it is '{self.report_type}'"
            )
        self.max_tries = params.get("max_tries", 200)
        self.poll_distance = 3

    def run(self):
        final_report = {}
        self.headers = {"Authorization": f"Bearer {self.__api_key}"}

        name_to_send = self.filename if self.filename else self.md5
        binary = self.read_file_bytes()
        files = {
            "file": (name_to_send, binary),
            "_json": (None, b'{"kind": "file", "interactive": false}'),
        }

        logger.info(f"triage md5 {self.md5} sending sample for analysis")
        for _try in range(self.max_tries):
            logger.info(f"triage md5 {self.md5} polling for result try #{_try + 1}")
            response = requests.post(
                self.base_url + "samples", headers=self.headers, files=files
            )
            if response.status_code == 200:
                break
            time.sleep(self.poll_distance)

        if response.status_code != 200:
            raise AnalyzerRunException("max retry attempts exceeded")

        sample_id = response.json().get("id", None)
        if sample_id is None:
            raise AnalyzerRunException("error sending sample")

        requests.get(
            self.base_url + f"samples/{sample_id}/events", headers=self.headers
        )

        final_report["overview"] = self.get_overview_report(sample_id)

        if self.report_type == "complete":
            final_report["static_report"] = self.get_static_report(sample_id)

            final_report["task_report"] = {}
            for task in final_report["overview"]["tasks"].keys():
                status_code, task_report_json = self.get_task_report(sample_id, task)
                if status_code == 200:
                    final_report["task_report"][f"{task}"] = task_report_json

        analysis_id = final_report["overview"].get("sample", {}).get("id", "")
        if analysis_id:
            final_report["permalink"] = f"{self.report_url}{analysis_id}"

        return final_report

    def get_overview_report(self, sample_id):
        overview = requests.get(
            self.base_url + f"samples/{sample_id}/overview.json",
            headers=self.headers,
        )
        return overview.json()

    def get_static_report(self, sample_id):
        static = requests.get(
            self.base_url + f"samples/{sample_id}/reports/static",
            headers=self.headers,
        )
        return static.json()

    def get_task_report(self, sample_id, task):
        task_report = requests.get(
            self.base_url + f"samples/{sample_id}/{task}/report_triage.json",
            headers=self.headers,
        )
        return task_report.status_code, task_report.json()

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "requests.get",
                    return_value=MockResponse(
                        {"tasks": {"task_1": {}, "task_2": {}}}, 200
                    ),
                ),
                patch(
                    "requests.post",
                    return_value=MockResponse(
                        {"id": "sample_id", "status": "pending"}, 200
                    ),
                ),
            )
        ]
        return super()._monkeypatch(patches=patches)
