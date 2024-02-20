# 导入必要的库
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


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
translator_key = '3fc1274301664a6ab753d766ae91c95f'
translator_endpoint = 'https://api.cognitive.microsofttranslator.com/'

# 创建认证对象
credential = AzureKeyCredential(translator_key)

# 创建Translator Text客户端
translation_client = TextTranslationClient(credential = TranslatorCredential(translator_key, translator_endpoint));



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
The United States of America has had 46 commanders in chief, and today, the third Monday of February, we commemorate their legacies. Initially established to honor George Washington's birthday, Presidents Day has evolved into a celebration of all presidents. Revered among them is Abraham Lincoln, a towering figure in American history, who guided the country through the Civil War and abolished slavery in America. The Lincoln Memorial, seen in today's image, overlooks the Reflecting Pool at the west end of the National Mall in Washington, DC. Designed in a neoclassical style, the memorial is a poignant destination for those seeking to connect with American history during Presidents Day, and beyond.
"""


# 指定目标语言
target_language = 'zh-Hans'

# 调用翻译方法进行文本翻译
result = translation_client.transliterate(text_from_image, target_language)


# 提取翻译后的文本
translated_text = result.translations[0].text

print(f"Translated Text: {translated_text}")

# 将图像标签和文字信息结合在一起
combined_text = ",".join(image_tags) + translated_text

# 提取标签
response = text_analytics_client.extract_key_phrases(documents=[combined_text], language="zh")

for document in response:
    if not document.is_error:
        print("Document Key Phrases:")
        for phrase in document.key_phrases:
            print("\t", phrase)
    else:
        print("Error: ", document.id, document.error)



# 在这里，您可以根据需要进一步处理和利用生成的标签信息
