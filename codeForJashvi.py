import dropbox
import pandas as pd
import io
import os

REFRESH_TOKEN = "J9mhZSVMJZ0AAAAAAAAAATohs-HAoC9R-Seg2AgMgLRcr2fzAkPORPDpPWXq8Gsh"
DROPBOX_ACCESS_TOKEN = "sl.BgwvMRp9a-wUPP630XSQdK-brMgHem13smaepOxslxGctmZyxKvj0LV9c5U0twc9EPNZul6oNt_bbWZo2SHWAgdbTfPNCpZHCy8iX-h2ncn8q6Hi5cIAjmQAX-bQ9XnqZSAIghg"
APP_SECRET = "ix3p9uqnhcad14g"
APP_KEY = "1kb7q5hkbwqn9w6"
dbx = dropbox.Dropbox(
    oauth2_access_token=DROPBOX_ACCESS_TOKEN,
    oauth2_refresh_token=REFRESH_TOKEN,
    app_secret=APP_SECRET,
    app_key=APP_KEY,
)

def CodeforJashvi():
    result = dbx.files_list_folder(
        "/orf467/index_html/NationWideModule1NNPersonFilesByCounty'18Kyle"
    )
    local_destination_folder = os.path.expanduser("~/Desktop/MyPersonFiles")
    
    # Create the local destination folder if it doesn't exist
    if not os.path.exists(local_destination_folder):
        os.makedirs(local_destination_folder)
    
    while True:
        for entry in result.entries:
            data, contents = dbx.files_download(entry.path_display)
            with io.BytesIO(contents.content) as stream:
                sheet = pd.read_csv(stream)

                # Process your data here using Pandas

                # Save the processed data as CSV to the local destination folder
                output_file_name = os.path.join(local_destination_folder, f"{entry.name}_processed.csv")
                sheet.to_csv(output_file_name, index=False)

        if not result.has_more:
            break
        result = dbx.files_list_folder_continue(result.cursor)

CodeforJashvi()