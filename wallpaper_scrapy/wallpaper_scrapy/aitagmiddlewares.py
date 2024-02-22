from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import deepl
import os

# 设置 Azure 计算机视觉服务的密钥和终结点
subscription_key = '7d4d53d103874e07918590d43ae49a5e'
endpoint = 'https://vision-tag.cognitiveservices.azure.com/'

# Azure 文本分析服务凭据
text_analytics_key = '07164b6048d34911bf09b716f38ff67e'
text_analytics_endpoint = 'https://aitextanalytics2tag.cognitiveservices.azure.com/'

# 初始化计算机视觉客户端
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
# 初始化文本分析客户端
text_analytics_client = TextAnalyticsClient(text_analytics_endpoint, AzureKeyCredential(text_analytics_key))

# 替换为您自己的Azure订阅密钥和终结点
translator_key = '5387c78d-cf8e-0421-2989-7282a5a03c84:fx'

# 创建Translator Text客户端
translation_client = translator = deepl.Translator(translator_key)


# 加载图像
image_path = '/Users/alison/WorkSpace/Personal/Wallpaper/static/bing/LincolnSunset.jpg'


# 分析图像内容
image_stream = open(image_path, "rb")
image_analysis = computervision_client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.tags], language="zh")

# 结合图像内容和文字信息
image_tags = [tag.name for tag in image_analysis.tags]
# 假设这里有一个变量 text_from_image 包含从图像中提取的文字信息
# 这里只是一个示例，实际情况可能更复杂

text_from_image = """
美利坚合众国曾有 46 位总司令，今天，二月的第三个星期一，我们纪念他们的丰功伟绩。总统日最初是为了纪念乔治-华盛顿（George Washington）的生日而设立的，如今已发展成为庆祝所有总统的节日。亚伯拉罕-林肯是美国历史上备受尊敬的人物，他领导美国经历了南北战争，并废除了美国的奴隶制。林肯纪念堂位于华盛顿特区国家广场西端，俯瞰倒影池。林肯纪念堂采用新古典主义风格设计，是美国总统日期间及之后人们追寻美国历史的一个重要景点。
"""
#The United States of America has had 46 commanders in chief, and today, the third Monday of February, we commemorate their legacies. Initially established to honor George Washington's birthday, Presidents Day has evolved into a celebration of all presidents. Revered among them is Abraham Lincoln, a towering figure in American history, who guided the country through the Civil War and abolished slavery in America. The Lincoln Memorial, seen in today's image, overlooks the Reflecting Pool at the west end of the National Mall in Washington, DC. Designed in a neoclassical style, the memorial is a poignant destination for those seeking to connect with American history during Presidents Day, and beyond.
#"""

# 调用翻译方法进行文本翻译
target_languages = "ZH"

response = translation_client.translate_text(text_from_image, target_lang=target_languages)

documents = [
    ",".join(image_tags),
    response.text
]

response = text_analytics_client.recognize_entities(documents=documents)
sorted_response = sorted(response, key=lambda x: x.entities[0].confidence_score, reverse=True)


tags = set()
# 遍历排序后的结果
for item in sorted_response:
    for entity in item.entities:
        print(entity.text, entity.category, entity.confidence_score)
        if entity.confidence_score > 0.9:
            tags.add(entity.text)    

print(tags)
