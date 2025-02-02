import simplekml
from github import Github

def generateKmlFile(points): # points is a list of tuples
    kml = simplekml.Kml()
    kml.newlinestring(name="Path", coords = points)
    kml.save("path.kml")
    return "path.kml"

def addToGit():
    GITHUB_TOKEN = "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"  #GitHub PAT
    REPO_NAME = "magrey0/map"   #repository name
    FILE_PATH = "file_path"          #path to local file
    UPLOAD_PATH = "path.kml"  #path in the repository

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    with open(FILE_PATH, "r") as file:
        file_content = file.read()

    try:
        repo.create_file(
            path=UPLOAD_PATH,
            message="Upload file via Python script",
            content=file_content,
            branch="main"
        )

        return f"https://raw.githubusercontent.com/{REPO_NAME}/main/{UPLOAD_PATH}"

    except Exception as e:
        print(f"Error uploading file: {e}")
