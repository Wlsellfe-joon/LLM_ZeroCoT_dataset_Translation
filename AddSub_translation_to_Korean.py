from googletrans import Translator
import json

def translate_text(text, src_language='en', dest_language='ko'):
    translator = Translator()
    try:
        if isinstance(text, list):
            # 리스트의 각 원소를 개별적으로 번역
            translated_text = [translator.translate(item, src=src_language, dest=dest_language).text if translator.translate(item, src=src_language, dest=dest_language).text is not None else item for item in text]
        else:
            # 단일 텍스트인 경우에는 그대로 번역
            translated_text = translator.translate(text, src=src_language, dest=dest_language).text
        return translated_text
    except Exception as e:
        print(f"Translation failed for text: {text}")
        print(f"Error: {e}")
        return text

def translate_json(json_data):
    # 각 문장을 한국어로 번역
    translated_data = {}
    for key, value in json_data.items():
        if key in ["sQuestion"]:
            translated_data[key] = translate_text(value)
        else:
            translated_data[key] = value

    return translated_data

def translate_and_save(input_file, output_file):
    # JSON 파일 읽기
    with open(input_file, 'r', encoding='utf-8') as file:
        json_list = json.load(file)

    translated_data_list = []
    count = 0
    for json_data in json_list:
        count+=1
        print("Process: ", count)
        translated_data = translate_json(json_data)
        translated_data_list.append(translated_data)

    with open(output_file, 'w', encoding='utf-8') as file:
        # 데이터가 None이 아닌 경우에만 JSON으로 저장
        filtered_data_list = [data for data in translated_data_list if data is not None]
        json.dump(filtered_data_list, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 입력 파일 및 출력 파일명 지정
    input_file_name = "./dataset/AddSub/AddSub.json"
    output_file_name = "./AddSub_translated_output_file.json"

    # 번역하고 저장
    translate_and_save(input_file_name, output_file_name)