from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy import dataset_collections
import os
import re
import sys
import time


def get_files(library_name):
    libs = gi.libraries.get_libraries()
    run = {}
    for i in libs:
        if library_name in i["name"]:
            folders = gi.libraries.get_folders(i["id"])
            for f in folders if len(folders) == 1 else folders[1:]:
                folder_contents = gi.folders.show_folder(f["id"], contents=True)[
                    "folder_contents"
                ]
                plate_id = i["name"] if f["name"] == "/" else f["name"].replace("/", "")
                plate_id = (
                    f'{i["name"]}_{plate_id}'
                    if i["name"].strip() not in plate_id
                    else plate_id
                )
                files = [
                    {re.sub("_R[12].*$", "", c["name"]): c["id"]}
                    for c in folder_contents
                ]
                run.update({plate_id: files})
    return run


def parse_elements(files):
    pairs = {
        k: [i for i in [d.get(k) for d in files] if i] for k in set().union(*files)
    }
    return [
        dataset_collections.CollectionElement(
            name=k,
            type="paired",
            elements=[
                dataset_collections.LibraryDatasetElement(name="forward", id=v[0]),
                dataset_collections.LibraryDatasetElement(name="reverse", id=v[1]),
            ],
        )
        for k, v in pairs.items()
    ]


gi = GalaxyInstance(
    url="https://galaxy.hpc.ut.ee", key=os.environ.get("GALAXY_API_KEY")
)

# Copy of COVID-19: variation analysis on ARTIC PE data + collapse collection shared by user ulvit
WORKFLOW_ID = "301230389d3c5421"

files = get_files(sys.argv[1])
elements = {k: parse_elements(v) for k, v in files.items()}

# Create history
for run, element in elements.items():
    tag = re.sub("covid", "", run)
    history_id = gi.histories.create_history(f"sarscov2-{tag}")["id"]
    # Create dataset collection
    collection_desc = dataset_collections.CollectionDescription(
        name=run,
        type="list:paired",
        elements=element,
    )
    collection_id = gi.histories.create_dataset_collection(
        history_id=history_id, collection_description=collection_desc
    )["id"]
    # Run workflow
    inputs = {}
    inputs["0"] = {"src": "hda", "id": "c8960aaeee5e5b0c"}
    inputs["1"] = {"src": "hda", "id": "c8960aaeee5e5b0c"}
    inputs["2"] = {"src": "hda", "id": "56d20db643753f34"}
    inputs["3"] = {"src": "hdca", "id": collection_id}
    invocation = gi.workflows.invoke_workflow(
        WORKFLOW_ID, inputs=inputs, history_id=history_id, import_inputs_to_history=True
    )
    print(invocation)
    time.sleep(10)
