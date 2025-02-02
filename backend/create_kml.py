import simplekml
from github import Github

def generateKmlFile(points): # points is a list of tuples
    kml = simplekml.Kml()
    lin = kml.newlinestring(name="Path", coords = points)
    lin.style.linestyle.color = simplekml.Color.red  # Red
    lin.style.linestyle.width = 2  # 2 pixels
    kml.save("path.kml")

def addToGit(token):
    GITHUB_TOKEN = token  #GitHub PAT
    REPO_NAME = "magrey0/map"   #repository name
    FILE_PATH = "path.kml"    #path to local file

    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file = repo.get_contents("", ref="main")[0]

    num = file.path[4:-4]

    upload_path = f"path{int(num)+1}.kml"  #path in the repository

    # Remove file
    repo.delete_file(file.path, "Remove all files", file.sha, branch="main")
    print(f"Deleted {file.path}")

    with open(FILE_PATH, "r") as file:
        file_content = file.read()

    try:
        repo.create_file(
            path=upload_path,
            message="Upload file via Python script",
            content=file_content,
            branch="main"
        )

        print("File uploaded successfully!")

    except Exception as e:
        print(f"Error uploading file: {e}")

    return "https://raw.githubusercontent.com/{REPO_NAME}/main/{UPLOAD_PATH}"