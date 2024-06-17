import openai
import os

# OpenAI API 키 설정
openai.api_key = 'YOUR_API_KEY_HERE'

def split_srt(file_path, ranges):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    parts = []
    for start, end in ranges:
        part = []
        in_range = False
        for line in lines:
            if line.strip().isdigit():
                current_index = int(line.strip())
                if start <= current_index <= end:
                    in_range = True
                else:
                    in_range = False
            if in_range:
                part.append(line)
        parts.append(part)
    return parts

def translate_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Translate the following Korean text to English."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message['content'].strip()

def translate_srt_parts(srt_parts):
    translated_parts = []
    for part in srt_parts:
        korean_text = ''.join(part)
        english_text = translate_text(korean_text)
        translated_parts.append(english_text.split('\n'))
    return translated_parts

def save_translated_srt(translated_parts, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for part in translated_parts:
            for line in part:
                file.write(line + '\n')

# Define the ranges
ranges = [(1, 56), (57, 107), (108, 166), (167, 230), (231, 258), (259, 284), (285, 323), (324, 385), (386, 443)]

# Split the SRT file into parts
srt_parts = split_srt('viviz.srt', ranges)

# Translate each part using GPT-4
translated_parts = translate_srt_parts(srt_parts)

# Save the translated parts to a new SRT file
save_translated_srt(translated_parts, 'viviz_eng.srt')

print("Translation completed. The translated file is saved as 'viviz_eng.srt'.")
