import os
from fastapi import File, Form, UploadFile
from configs.model_config import (DEFAULT_VS_TYPE, EMBEDDING_MODEL, VECTOR_SEARCH_TOP_K, SCORE_THRESHOLD)
from server.utils import BaseResponse
from server.knowledge_base.utils import validate_kb_name, KnowledgeFile
from server.knowledge_base.kb_service.base import KBServiceFactory
from configs.model_config import EMBEDDING_MODEL, DEFAULT_VS_TYPE



async def create_kb_with_doc(file: UploadFile = File(..., description="上传文件"),
                     knowledge_base_id: str = Form(..., description="知识库名称", examples=["kb1"])
                     ):
    if not validate_kb_name(knowledge_base_id):
        return BaseResponse(code=403, msg="Don't attack me")
    
    kb = KBServiceFactory.get_service_by_name(knowledge_base_id)
    kb_exists = False
    if kb is None:
        kb = KBServiceFactory.get_service(knowledge_base_id, DEFAULT_VS_TYPE, EMBEDDING_MODEL)
        kb.create_kb()
    else:
        kb_exists = True        

    file_ext = os.path.splitext(file.filename)[-1].lower()
    #if file extension is blank, make it to be .txt
    if file_ext == "":
        file_ext = ".txt"
        file.filename = file.filename + file_ext

    file_content = await file.read()  # 读取上传文件的内容

    kb_file = KnowledgeFile(filename=file.filename,
                            knowledge_base_name=knowledge_base_id)

    if (os.path.exists(kb_file.filepath)
            and os.path.getsize(kb_file.filepath) == len(file_content)
    ):
        # TODO: filesize 不同后的处理
        file_status = f"文件 {kb_file.filename} 已存在。"
        return BaseResponse(code=404, msg=file_status)

    try:
        with open(kb_file.filepath, "wb") as f:
            f.write(file_content)
    except Exception as e:
        return BaseResponse(code=500, msg=f"{kb_file.filename} 文件上传失败，报错信息为: {e}")

    if kb_exists:
        kb.clear_vs()

    kb.add_doc(kb_file)
    return BaseResponse(code=200, msg=f"成功上传文件 {kb_file.filename}")