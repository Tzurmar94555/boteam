def change(text):
    """
    將所有種類的斜線（正斜線 /、反斜線 \\、全角正斜線 ／、全角反斜線 ＼ 等）
    轉換為底線（_）
    """
    # 替換所有常見的斜線字符為底線 _
    return (text.replace('/', '_')  # 替換正斜線
               .replace('\\', '_')  # 替換反斜線
               .replace('／', '_')  # 替換全角正斜線
               .replace('＼', '_')  # 替換全角反斜線
               .replace('⧸', '_')  # 其他特殊斜線
               )

# 範例使用：
# original_text = "這是一個/包含/正斜線、反斜線\\、全角斜線／和＼的例子"
# processed_text = replace_all_slashes_with_underscore(original_text)
# print(f"處理後的文字: {processed_text}")
