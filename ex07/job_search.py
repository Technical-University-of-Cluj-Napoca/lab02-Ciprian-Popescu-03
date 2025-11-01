import requests
from bs4 import BeautifulSoup

def fetch_jobs():
    url = "https://www.juniors.ro/jobs/experienta:200"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("❌ Failed to retrieve job listings.")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    job_list = soup.find("ul", class_="job_list")
    if not job_list:
        print("⚠️ No job list found in the page HTML.")
        return []

    jobs = job_list.find_all("li", class_="job")
    print(f"✅ Found {len(jobs)} jobs.")

    job_listings = []
    for job in jobs:

        header = job.find("div", class_="job_header_title")
        title_tag = header.find("h3") if header else None
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        tech_tags = header.select(".job_tags li a") if header else []
        technologies = [tag.get_text(strip=True) for tag in tech_tags]

        job_content = job.find("div", class_="job_content")

        company_tag = job_content.find("ul", class_="job_requirements")
        company = "N/A"
        if company_tag:
            first_li = company_tag.find("li")
            if first_li:
                company = first_li.get_text(strip=True).replace("Companie:", "").strip()

        location_info_tag = job.find("strong")
        location = "N/A"
        date_posted = "N/A"
        work_type = "N/A"

        if location_info_tag:
            text = location_info_tag.get_text(strip=True)
            parts = [p.strip() for p in text.split("|") if p.strip()]
            for part in parts:
                if "zi" in part or "zile" in part or "săptămână" in part or "săptămâni" in part or "lună" in part or "oră" in part:
                    date_posted = part
                elif part.lower() in ["remote", "hibrid", "hybrid"]:
                    work_type = part
                else:
                    location = part

        job_listings.append({
            "Title": title,
            "Company": company,
            "Location": location,
            "Work Type": work_type,
            "Technologies": ", ".join(technologies),
            "Date Posted": date_posted
        })

    return job_listings


def display_jobs(jobs):
    if not jobs:
        print("No job listings found.")
        return

    for idx, job in enumerate(jobs, 1):
        print(f"Job {idx}: {job['Title']}")
        print(f"  Company: {job['Company']}")
        print(f"  Location: {job['Location']}")
        print(f"  Work Type: {job['Work Type']}")
        print(f"  Technologies: {job['Technologies']}")
        print(f"  Date Posted: {job['Date Posted']}")
        print("-" * 60)


if __name__ == "__main__":
    jobs = fetch_jobs()
    display_jobs(jobs)
