from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
import polars as pl
import matplotlib.pyplot as plt
import io
import base64

app = FastAPI()

@app.post("/analyze")
async def analyze_titanic(file: UploadFile = File(...)):
    # 1. Read CSV data using Polars
    content = await file.read()
    df = pl.read_csv(content)

    # 2. Group by Pclass and calculate Mean Survival
    # (Polars syntax is different from Pandas!)
    stats = df.group_by("Pclass").agg(
        pl.col("Survived").mean().alias("Survival_Rate")
    ).sort("Pclass")

    # 3. Generate Plot
    plt.figure(figsize=(8, 6))
    # We define colors: Red for low survival, Green for high
    colors = ['#ff9999' if rate < 0.5 else '#99ff99'
    for rate in stats['Survival_Rate']]

    plt.bar(stats['Pclass'], stats['Survival_Rate'],
    color=colors, edgecolor='black')
    plt.xlabel("Passenger Class (1st, 2nd, 3rd)")
    plt.ylabel("Survival Rate (0.0 to 1.0)")
    plt.title("Titanic: Survival Rate by Class")
    plt.xticks(stats['Pclass'])
    plt.ylim(0, 1)

    # 4. Save to Buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    # 5. Return HTML
    return HTMLResponse(content=f"""
        <div style="text-align:center; font-family:sans-serif;">
            <h1>Analysis Result</h1>
            <p>Based on {df.height} passenger records.</p>
            <img src="data:image/png;base64,{img_str}" />
            <br><br>
            <a href="/">Analyze Another File</a>
        </div>
    """)
