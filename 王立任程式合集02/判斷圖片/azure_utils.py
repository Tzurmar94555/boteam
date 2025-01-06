import os
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

class AzurePredictor:
    def __init__(self):
        # 從環境變數中讀取 Azure 配置
        self.prediction_key = os.getenv("AZURE_PREDICTION_KEY")
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        self.project_id = os.getenv("AZURE_PROJECT_ID")
        self.iteration_name = os.getenv("AZURE_ITERATION_NAME")

        # 初始化 Azure Custom Vision 客戶端
        credentials = ApiKeyCredentials(in_headers={"Prediction-key": self.prediction_key})
        self.predictor = CustomVisionPredictionClient(self.endpoint, credentials)

    async def handle_image(self, attachment):
        try:
            # 下載圖片字節
            image_bytes = await attachment.read()

            # 調用 Azure Custom Vision 進行預測
            results = self.predictor.classify_image(self.project_id, self.iteration_name, image_bytes)

            # 找出最高機率的標籤
            top_prediction = max(results.predictions, key=lambda p: p.probability)

            # 返回結果
            if top_prediction.tag_name.lower() in ["cat", "dog"] and top_prediction.probability >= 0.9:
                return f"這張圖片是 {top_prediction.tag_name}"
            else:
                return "這張圖片既不是貓也不是狗"
        except Exception as e:
            return f"處理圖片時發生錯誤: {e}"
