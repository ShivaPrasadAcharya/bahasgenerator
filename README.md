# Bahas Generator

The existing interface, licence lookup, party fields, text generation, saved forms,
copying, and document exports are retained.

## Practitioner data

`advocatedata.json` is the complete JSON dataset exported from Adhivaktako Kundali:
25,062 records, including the 2,952 practitioners with licences 21559–24510.
The added English names are common Nepali transliterations, rather than official
English spellings supplied by the Nepal Bar Council. All available fields,
including remarks where present, are retained in the JSON.

Edit `advocatedata.json` to update the data. Each push to `main` runs
`.github/workflows/deploy-pages.yml`, validates the JSON, generates the data script,
and publishes the site through GitHub Pages. Invalid input stops the build before
deployment. In Settings → Pages, the publishing source must be **GitHub Actions**.

The published data script has a content-based filename so browsers load the new
records after each data update. The page's interface and application code are
unchanged.

## Local or offline use

Open `index.html` beside the included `advocatedata.js`, as before. After changing
the JSON locally, refresh this script and build a publishable `dist` directory:

```sh
python3 scripts/build_site.py --sync-data
```

The public JSON is also included in the deployed site as `advocatedata.json`.
