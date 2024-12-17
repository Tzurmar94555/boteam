# import google.generativeai as generativeai

# generativeai.configure(api_key="AIzaSyDlx27YgDO_MT0_w5mF_sVi2NcAMH2Y7P")
# model_id = "gemini-1.0-flash-ape"

import os
import google.generativeai as generativeai

generativeai.configure(api_key="AIzaSyAt5UWjPfwRQlyKDl_idjIXCrLy-BK-Bd4")
response = generativeai.GenerativeModel("gemini-2.0-flash-exp").generate_content("解釋1+1")
print(response.text)
