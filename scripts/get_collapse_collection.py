from bioblend.galaxy import GalaxyInstance
import os

gi = GalaxyInstance(
    url="https://galaxy.hpc.ut.ee", key=os.environ.get("GALAXY_API_KEY")
)
histories = gi.histories.get_histories()

for h in histories:
    if "sarscov2" in h["name"] and gi.histories.get_status(h["id"])["state"] == "ok":
        print(f'{h["name"]}: {h["id"]}')
        cont = gi.histories.show_history(h["id"], contents=True)
        for dataset in cont:
            if "Collapse Collection" in dataset["name"] and dataset["state"] == "ok":
                name = h["name"].replace(" ", "_")
                gi.datasets.download_dataset(
                    dataset["id"],
                    file_path=f"output/artic_{name}.tsv",
                    use_default_filename=False,
                )
