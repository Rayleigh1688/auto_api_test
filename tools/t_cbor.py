import base64
import cbor2
import json


def main():
    raw_input = input("请输入带前缀的响应数据：").strip()

    try:
        if ',' in raw_input:
            _, base64_data = raw_input.split(',', 1)
        else:
            base64_data = raw_input

        cbor_bytes = base64.b64decode(base64_data)


        cbor_obj = cbor2.loads(cbor_bytes)

        json_str = json.dumps(cbor_obj, ensure_ascii=False, indent=2)

        print("解析后的JSON结果：")
        print(json_str)
    except Exception as e:
        print(f"解析失败: {e}")

# 解析CBOR
if __name__ == "__main__":
    main()