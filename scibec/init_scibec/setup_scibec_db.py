import datetime
import getpass
import json

import requests
from scihub.scibec import SciBec
from tqdm import tqdm


class SciBecSetup:
    scibec_url = "http://localhost:3030"

    def __init__(self) -> None:
        self.scibec = SciBec()
        self.scibec.url = self.scibec_url

        self._scicat_proposals = []
        self.proposal_storage = []
        self.access_groups = set()
        self.location_storage = {}

    @staticmethod
    def get_scicat_proposals() -> list:
        """retrieve all proposals from scicat"""

        pwd = getpass.getpass()
        payload = {"username": "proposalIngestor", "password": pwd}
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        res = requests.post(
            "https://dacat.psi.ch/api/v3/Users/login", json=payload, headers=headers, timeout=10
        )

        res_json = json.loads(res.content)
        access_token_scicat = res_json["id"]

        headers = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": access_token_scicat,
        }
        res = requests.get("https://dacat.psi.ch/api/v3/Proposals", headers=headers, timeout=100)
        return json.loads(res.content)

    def _update_storage_with_proposals(self, max_time: int = None) -> None:
        current_time = datetime.datetime.now()

        for prop in self._scicat_proposals:
            if max_time is not None:
                time_delta = current_time - datetime.datetime.strptime(
                    prop["MeasurementPeriodList"][0]["start"][:-1], "%Y-%m-%dT%H:%M:%S.%f"
                )

                if time_delta.days > max_time:
                    continue

            self.location_storage[prop["MeasurementPeriodList"][0]["instrument"]] = {}

            self.location_storage[prop["MeasurementPeriodList"][0]["instrument"]] = {}
            self.proposal_storage.append(
                {
                    "ownerGroup": prop["ownerGroup"],
                    "abstract": prop["abstract"],
                    "title": prop["title"],
                    "location": prop["MeasurementPeriodList"][0]["instrument"],
                    "info": prop,
                }
            )
            for access_group in prop["accessGroups"]:
                self.access_groups.add(access_group)

    def _update_beamlines(self):
        existing_beamlines = {
            beamline["name"]: beamline["id"] for beamline in self.scibec.get_beamlines()
        }
        for location in tqdm(self.location_storage, desc="Updating beamlines..."):
            if not location.startswith("/PSI"):
                continue
            beamline_name = location.split("/")[-1]
            if beamline_name in existing_beamlines:
                target_id = existing_beamlines[beamline_name]
            else:
                res = self.scibec.add_beamline(beamline_name)
                existing_beamlines[beamline_name] = target_id = res["id"]
            self.location_storage[location] = target_id

    def _update_experiments(self):
        for proposal in tqdm(self.proposal_storage, desc="Updating proposals..."):
            title = proposal["title"]
            if not title:
                title = proposal["ownerGroup"]
            experiment = {
                "name": title,
                "readACL": [proposal["ownerGroup"]],
                "createACL": [proposal["ownerGroup"]],
                "updateACL": [proposal["ownerGroup"]],
                "beamlineId": self.location_storage[proposal["location"]],
                "writeAccount": proposal["ownerGroup"],
                "experimentInfo": proposal["info"],
            }

            res = self.scibec.get_experiment(name=title)
            if not res:
                self.scibec.add_experiment(experiment)

    def sync_proposals(self):
        """update / sync SciBec with SciCat proposals"""
        self._scicat_proposals = self.get_scicat_proposals()
        self._update_storage_with_proposals()
        self._update_beamlines()
        self._update_experiments()


if __name__ == "__main__":
    scibec_setup = SciBecSetup()
    scibec_setup.sync_proposals()
