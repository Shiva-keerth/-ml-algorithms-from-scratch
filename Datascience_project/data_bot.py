import os
import time
import random
import pandas as pd
import pathlib  # <-- This safely handles Windows/Mac file paths!
from playwright.sync_api import sync_playwright

DATASET_FILE = "intern dataset.csv"


def create_fake_lms_website():
    """Reads the CSV and dynamically builds a fake website for ALL employees."""
    print("🏗️ Building simulated company grading portal...", flush=True)

    try:
        df = pd.read_csv(DATASET_FILE)
        all_emp_ids = df['Employee_ID'].tolist()
    except Exception as e:
        print(f"⚠️ Error reading CSV: {e}. Using fallback data.", flush=True)
        all_emp_ids = ["EMP_00001"]

    html_content = """
    <html>
    <head>
        <title>Company LMS Portal</title>
        <style>body { font-family: Arial; padding: 20px; } table { border-collapse: collapse; } th, td { border: 1px solid black; padding: 8px; }</style>
    </head>
    <body>
        <h1>Weekly Intern Tracking Database</h1>
        <table id="score-table">
            <tr>
                <th>Employee_ID</th><th>Task_Comp_%</th><th>Attendance_%</th>
                <th>Learning_Hrs</th><th>Screen_Time</th><th>Stress(0-10)</th>
                <th>Engagement</th><th>Mentor_Feedback</th>
            </tr>
    """

    for emp_id in all_emp_ids:
        if str(emp_id) == "nan" or str(emp_id).strip() == "":
            continue

        task = round(random.uniform(60.0, 99.0), 1)
        att = round(random.uniform(75.0, 100.0), 1)
        learn = round(random.uniform(5.0, 20.0), 1)
        screen = round(random.uniform(4.0, 10.0), 1)
        stress = round(random.uniform(2.0, 9.0), 1)
        eng = round(random.uniform(50.0, 95.0), 1)
        mentor = round(random.uniform(2.5, 5.0), 1)

        row_html = f"""
            <tr class="intern-row">
                <td class="emp-id">{emp_id}</td><td class="task">{task}</td><td class="att">{att}</td>
                <td class="learn">{learn}</td><td class="screen">{screen}</td><td class="stress">{stress}</td>
                <td class="eng">{eng}</td><td class="mentor">{mentor}</td>
            </tr>
        """
        html_content += row_html

    html_content += """
        </table>
    </body>
    </html>
    """

    with open("fake_lms.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # THIS IS THE MAGIC FIX: It generates a perfect file URL for any operating system
    return pathlib.Path("fake_lms.html").absolute().as_uri()


def run_rpa_bot():
    fake_website_url = create_fake_lms_website()
    print("🤖 Booting up the RPA Bot...", flush=True)
    scraped_data = []

    try:
        with sync_playwright() as p:
            print("🌐 Opening browser...", flush=True)
            # You can change headless=True if you don't even want to see the window pop up!
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            print(f"🔗 Navigating to company portal...", flush=True)
            page.goto(fake_website_url)

            print("📊 Scooping all data instantly...", flush=True)

            # --- THE MAGIC FIX: Scoop all data instantly using internal JavaScript ---
            scraped_data = page.evaluate("""() => {
                const rows = document.querySelectorAll('.intern-row');
                const data = [];
                for (const row of rows) {
                    data.push({
                        "Employee_ID": row.querySelector('.emp-id').innerText,
                        "Task_Completion_Rate": parseFloat(row.querySelector('.task').innerText),
                        "Attendance_Rate": parseFloat(row.querySelector('.att').innerText),
                        "Weekly_Learning_Hours": parseFloat(row.querySelector('.learn').innerText),
                        "Daily_Screen_Time_Hours": parseFloat(row.querySelector('.screen').innerText),
                        "Stress_Level": parseFloat(row.querySelector('.stress').innerText),
                        "Engagement_Score": parseFloat(row.querySelector('.eng').innerText),
                        "Mentor_Feedback_Rating": parseFloat(row.querySelector('.mentor').innerText)
                    });
                }
                return data;
            }""")

            print(f"✅ Successfully extracted {len(scraped_data)} intern records.", flush=True)

            print("🚪 Closing browser...", flush=True)
            browser.close()

    except Exception as e:
        print(f"\n🚨 CRITICAL ERROR: {e}\n", flush=True)

    finally:
        # Always clean up the fake website file
        if os.path.exists("fake_lms.html"):
            os.remove("fake_lms.html")

    if len(scraped_data) > 0:
        update_csv(scraped_data)
    else:
        print("🛑 No data was extracted. Database update skipped.", flush=True)


def update_csv(scraped_data):
    print("📝 Updating the main database...", flush=True)
    try:
        df = pd.read_csv(DATASET_FILE)
    except FileNotFoundError:
        print(f"❌ Error: Cannot find {DATASET_FILE}.", flush=True)
        return

    # 1. Convert the scraped data straight into a Pandas DataFrame
    new_df = pd.DataFrame(scraped_data)

    # 2. Tell Pandas to mark all these new rows as "Pending"
    new_df["Performance_Trend"] = "Pending AI Assessment"

    # 3. Lock the Employee_ID as the index for both tables to link them
    df.set_index("Employee_ID", inplace=True)
    new_df.set_index("Employee_ID", inplace=True)

    # 4. MAGIC: Update the entire massive database instantly in one command
    df.update(new_df)

    # 5. Unlock the index so it goes back to normal
    df.reset_index(inplace=True)

    df.to_csv(DATASET_FILE, index=False)
    print("🎉 Database updated! Start your Streamlit app to see the fresh data.", flush=True)


if __name__ == "__main__":
    run_rpa_bot()