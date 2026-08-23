import json
import os
import networkx as nx
import matplotlib.pyplot as plt
from google import genai
from google.colab import userdata

# Initialize Gemini Client
try:
    api_key = userdata.get('GEMINI_API_KEY')
except:
    api_key = input("Enter your Gemini API Key: ")

client = genai.Client(api_key=api_key)

# Complex Enterprise Corpus with indirect connections
corpus_text = """
TechCorp manufactures the flagship Smartphone X1. 
Smartphone X1 relies on the M2-Microchip for AI processing.
The M2-Microchip is designed by QuantumDesign Inc and manufactured by SiliconFoundry Ltd.
SiliconFoundry Ltd depends on UltraPure Silicon raw materials supplied by MiningCo Global.
In July 2025, MiningCo Global suffered a major flood at its primary refinery in Queensland.
Due to the flood, MiningCo Global halted UltraPure Silicon shipments for 6 months.
As a result of raw material shortages, SiliconFoundry Ltd reduced chip production by 70%.
This reduction caused severe supply delays for TechCorp's Smartphone X1 launch.
"""

print("Corpus loaded successfully!")
