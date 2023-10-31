import pandas as pd
from tabula import read_pdf as pdftable

def read_pdf(pdfname):
    raw_df = None
    for page_df in pdftable(pdfname, pages="all"):
        if "gr.bilgileri" in str(page_df.head()).lower():
            if type(raw_df) == type(None): raw_df = page_df.iloc[2:]
            else: raw_df = pd.concat([raw_df, page_df.iloc[2:]])

    df = pd.DataFrame.from_dict({"Index": raw_df[raw_df.columns[-1]]}).set_index("Index")
    df["Numara"] = [int(float(str(i).replace(" ","").split("-")[0])) for i in raw_df[raw_df.columns[1]]]
    df["İsim"] = [str(i).split("-")[1].strip() for i in raw_df[raw_df.columns[1]]]
    df["Sınıf"] = [" / ".join(str(i).strip().replace(" ","").split("/")) for i in raw_df[raw_df.columns[2]]]
    df["D (Toplam)"] = [int(float(i)) for i in raw_df[raw_df.columns[13]]]
    df["Y (Toplam)"] = [int(float(i)) for i in raw_df[raw_df.columns[14]]]
    df["N (Toplam)"] = [float(i) for i in raw_df[raw_df.columns[15]]]
    df["D (Türkçe)"] = [int(float(i)) for i in raw_df[raw_df.columns[3]]]
    df["Y (Türkçe)"] = [int(float(i)) for i in raw_df[raw_df.columns[4]]]
    df["N (Türkçe)"] = [float(i) for i in raw_df[raw_df.columns[5]]]
    df["D (Sosyal)"] = [int(float(i)) for i in raw_df[raw_df.columns[6]]]
    df["Y (Sosyal)"] = [int(float(str(i).split()[0])) for i in raw_df[raw_df.columns[7]]]
    df["N (Sosyal)"] = [float(str(i).split()[1]) for i in raw_df[raw_df.columns[7]]]
    df["D (Matematik)"] = [int(float(str(i).split()[0])) for i in raw_df[raw_df.columns[9]]]
    df["Y (Matematik)"] = [int(float(str(i).split()[1])) for i in raw_df[raw_df.columns[9]]]
    df["N (Matematik)"] = [float(str(i).split()[2]) for i in raw_df[raw_df.columns[9]]]
    df["D (Fen)"] = [int(float(i)) for i in raw_df[raw_df.columns[10]]]
    df["Y (Fen)"] = [int(float(str(i).split()[0])) for i in raw_df[raw_df.columns[11]]]
    df["N (Fen)"] = [float(str(i).split()[1]) for i in raw_df[raw_df.columns[11]]]
    df["Kurum"] = raw_df[raw_df.columns[-1]].tolist()
    df["İlçe"] = raw_df[raw_df.columns[-2]].tolist()
    df["İl"] = raw_df[raw_df.columns[-3]].tolist()
    df["Genel"] = raw_df[raw_df.columns[-4]].tolist()

    return df