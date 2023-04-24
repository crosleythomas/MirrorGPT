# Data Sources

The best way to make your Mirror Agent more personalized to you is to give it access to more data about you. To give it more data you need to
1. Collect the data in a usable format
2. Load it into a datastore
3. Give the Mirror Agent access to the data through a Tool

There can be a wide range of implementations for these steps (different data sources, different data stores, and different Agent tools), so we will give two concrete examples below and leave other approaches to users and contributors.

## Data Examples

### LinkedIn Professional Data
1. Profile data is exported manually
2. Profile PDF is transformed into atomic sentences of text using `extract.py`
3. Profile text sentences are loaded into a Chroma datstore using `load.py`
4. The Chroma tool is used by the MirrorAgent to look up via vector search information loaded in from steps 1-3 when asked questions about professional or educational experience

### Importing Gather Data
[GetGather.xyz](https://getgather.xyz/) is an exciting new startup building tools to help you download your data from sites across the internet like Google, Uber Eats, Strava, and YouTube. They have an option to export your data as a single JSON file that works great with Mirror.

If you have set up Gather,
1. Click "Create Your Own"
2. "Download to JSON"
3. Move the exported file into `data/local/loaded`
4. The Gather tool is used by the MirrorAgent to extract relevant information from the JSON blob to answer questions

Example:
```
python entrypoints/run_mirror.py --data-path data/local/loaded -g "Hi what's your name?" -t chroma gather
```

Under the hood this is connecting the whole exported JSON file to the [Langchain JSON Agent](https://python.langchain.com/en/latest/modules/agents/toolkits/examples/json.html).

## Adding Data Sources
The [Main README](https://github.com/crosleythomas/MirrorGPT#create-your-mirror) gives an overview of the existing ETL-style tools available for collecting data into usable formats.

Depending on the data source you want to use there may be some combination of manual steps you will need to do but some steps you can also script in one of the ETL scripts.

All existing data sources and Tools are able to use the local filesystem. If you want to build something more complex, you may need to set up a custom storage solution as well.