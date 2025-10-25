import pandas as pd

def export_to_xlsx(signals, filepath):
    df = pd.DataFrame(signals)
    df.to_excel(filepath, index=False)
