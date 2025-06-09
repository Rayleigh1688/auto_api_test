import cbor2

# 粘贴你的原始字符串，注意要用原始字符串 r"" 包裹防止转义问题
hex_str = r"\xb8(cuidp2486786399927364jcreated_at\x1a\xff\xff\xff\xffjupdated_at\x1a\xff\xff\xff\xffephone`jfirst_namegKrislynkmiddle_namehKakilalailast_namedOraahbirthdayj1998-07-05lcountry_code`nnearest_branch`gid_typejPHILSYS_IDiid_number`fgenderffemalekattachments`mextra_details`nplace_of_birth`knationality`ocurrent_address`qpermanent_address`nnature_of_work`psource_of_income`joccupation`ftokens`pblacklist_status\x00eissue`iissue_msg`lissue_fields`fstatushapprovedgcommenta0hreviewer`lreview_times\x00jocr_status\x00cocr`texternal_information`gversiona1fsource`hnickname`husername`nreg_created_at\x00freg_ip`"

# 转成真正的字节流
try:
    raw_bytes = bytes(hex_str, "utf-8").decode("unicode_escape").encode("latin1")
except Exception as e:
    print("转为 bytes 失败：", e)
    exit()

# 用 cbor2 解码
try:
    data = cbor2.loads(raw_bytes)
    from pprint import pprint
    pprint(data)
except Exception as e:
    print("CBOR 解析失败：", e)