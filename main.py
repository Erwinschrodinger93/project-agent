import requests

def search_jobs(keyword, preferred_location):
    url = "https://remoteok.com/api"

    headers = {
        "User-Agent": "Project-Agent/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        print(f"\nJob service unavailable: {error}")
        return None
    except ValueError:
        print("\nJob service returned invalid data.")
        return None

    jobs = []

    for item in data[1:]:
        title = item.get("position", "")
        location = item.get("location", "Remote")

        location_matches = (
            preferred_location.lower() == "remote"
            or preferred_location.lower() in location.lower()
            or "remote" in location.lower()
            or "worldwide" in location.lower()
        )

        if keyword.lower() in title.lower() and location_matches:
            jobs.append({
                "title": title,
                "company": item.get("company", "Unknown"),
                "location": location,
                "url": item.get("url", "No URL available"),
            })
        if len(jobs) == 5:
            break


    return jobs

print("Project Agent Online.")
print("Hello, Erwin.")

task = input("What would you like me to do?")

if "job" in task.lower():
    keyword = input("What job title should I search for? ")
    preferred_location = input("What location do you prefer? ")
    results = search_jobs(keyword, preferred_location)

    if results is None:
        pass
    elif not results:
        print("\nNo matching jobs found. Try another title or location.")
    else:
        print("\nJobs found:\n")

        for job in results:
            print(job["title"])
            print(job["company"])
            print(job["location"])
            print(job["url"])
            print("---")
else:
    print("I don't know how to handle that task yet.")
