"""
This file contains code for image analysis and text extraction using Azure Cognitive Services.
"""
import os
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import baidu_translate as fanyi
from  scrapy import signals
import nltk
from nltk.corpus import stopwords


class AitagMiddlewares:
    def __init__(self, computer_key, computer_endpoint,
                  text_analytics_key, text_analytics_endpoint):
        self.computer_key = computer_key
        self.computer_endpoint = computer_endpoint
        # Set Azure Text Analytics service key and endpoint
        self.text_analytics_key = text_analytics_key
        self.text_analytics_endpoint = text_analytics_endpoint

        # Initialize Computer Vision client
        self.computervision_client = ComputerVisionClient(computer_endpoint, CognitiveServicesCredentials(computer_key))
        # Initialize Text Analytics client
        self.text_analytics_client = TextAnalyticsClient(text_analytics_endpoint, AzureKeyCredential(text_analytics_key))
    

    def load_custom_stopwords(self, file_path):
        """
        Load custom stopwords from a file.
        """
        with open(file_path, 'r') as file:
            stopwords = [line.strip() for line in file]
        return set(stopwords)
        def analyze_image_in_stream(self, image_path):
            """
            Analyze image content using Computer Vision service.
            """
            image_stream = open(image_path, "rb")
            image_analysis = self.computervision_client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.tags], language="zh")
            return [tag.name for tag in image_analysis.tags]

    def extract_key_phrases(self, text):
        """
        Extract key phrases from text using Text Analytics service.
        """
        baidu_response = fanyi.translate_text(text, to=fanyi.Lang.ZH)
        documents = [baidu_response]
        response = self.text_analytics_client.extract_key_phrases(documents=documents, language="zh")
        nltk_stopwords = set(stopwords.words('chinese'))
        custom_stopwords = self.load_custom_stopwords('./stopwords/baidu_stopwords.txt')
        all_chinese_stopwords = nltk_stopwords.union(custom_stopwords)

        filtered_words = [word for word in response[0].key_phrases if word not in all_chinese_stopwords]

        return filtered_words

