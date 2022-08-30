from bs4 import BeautifulSoup
import pandas as pd
import requests

# número de issue

run = True
issue = 1
columns = ["issue", "author", "state", "assignees"]
df = pd.DataFrame(columns=columns)

while run:
    url_name = "https://github.com/pescap/WebScrapingMDS/issues/" + str(issue)

    # Recuperar el html
    url = requests.get(url_name)
    soup = BeautifulSoup(url.text, "html.parser")

    if str(soup) == "Not Found":
        run = False

    state = None

    isOpen = soup.find("span", attrs={"title": "Status: Open"})
    if isOpen:
        ### ver si está el octicon octicon octicon-issue-opened
        if isOpen.findChildren("svg", attrs={"class": "octicon octicon-issue-opened"}):
            state = "open"

    if soup.find(
        "span", attrs={"title": "Status: Closed", "class": "State State--merged"}
    ):
        state = "closed"

    if state is not None:
        author = soup.find(
            "a", attrs={"class": "author text-bold Link--secondary"}
        ).get_text()

        assignees = (
            soup.find("span", attrs={"class": "css-truncate js-issue-assignees"})
            .get_text()
            .replace("\n", "")
            .split()
        )

        if assignees == ["No", "one", "assigned"]:
            assignees = ["No one assigned"]

        for l in range(len(assignees)):
            df = df.append(
                {
                    "issue": issue,
                    "author": author,
                    "state": state,
                    "assignees": assignees[l],
                },
                ignore_index=True,
            )
    issue += 1
    print(df)


df.to_csv("issues.csv", index=False)
