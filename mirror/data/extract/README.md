# Data Extraction

This directory contains utilities for extracting data to personalize your model. There can be many sources of this data including data that already exists and utilities to elicit new data from the user.

The tools provided in this directory should make it easy to extract those existing data sources and run programs to facilitate gathering of new data.

Existing Data Sources
1. Internet Accounts - Social Media (Twitter/Facebook/Instagram), Shopping (Amazon/DoorDash)
2. Text messages - Apple Messages, Facebook Messenger, WhatsApps
3. Rewind.ai database
4. Mem X

New Data
1. Mock conversations with the user
2. Targetted interview questions - "Are you gluten-free?"

Tools for getting this data
1. getgather.xyz
2. Data loaders in existing libraries like langchain, UnstructuredIO

## Contribution Wishlist
- [X] (Manual copy) LinkedIn + Transforming into fact statements
- [X] getgather.xyz JSON export
- [ ] Rewind.ai integration
- [ ] Apple desktop apps - Notes, Messages, etc.