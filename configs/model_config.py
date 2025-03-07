import os
import logging
import torch
# 日志格式
LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)


# 在以下字典中修改属性值，以指定本地embedding模型存储位置
# 如将 "text2vec": "GanymedeNil/text2vec-large-chinese" 修改为 "text2vec": "User/Downloads/text2vec-large-chinese"
# 此处请写绝对路径
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    #"text2vec": "GanymedeNil/text2vec-large-chinese",
    "text2vec": "/data/hujiaxin/repository/text2vec-large-chinese",
    #"text2vec-paraphrase": "shibing624/text2vec-base-chinese-paraphrase",
    "text2vec-paraphrase": "/data/hujiaxin/repository/text2vec-base-chinese-paraphrase",
    "text2vec-sentence": "shibing624/text2vec-base-chinese-sentence",
    "text2vec-multilingual": "shibing624/text2vec-base-multilingual",
    "m3e-small": "moka-ai/m3e-small",
    #"m3e-base": "moka-ai/m3e-base",
    "m3e-base": "/data/hujiaxin/repository/m3e-base",
    "m3e-large": "moka-ai/m3e-large",
    "bge-small-zh": "BAAI/bge-small-zh",
    "bge-base-zh": "BAAI/bge-base-zh",
    "bge-large-zh": "BAAI/bge-large-zh"
}

# 选用的 Embedding 名称
EMBEDDING_MODEL = "m3e-base"

# Embedding 模型运行设备
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"


llm_model_dict = {
    "chatglm-6b": {
        "local_model_path": "THUDM/chatglm-6b",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

    "chatglm-6b-int4": {
        "local_model_path": "THUDM/chatglm-6b-int4",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

    "chatglm2-6b": {
        #"local_model_path": "THUDM/chatglm2-6b",
        "local_model_path": "/data/hujiaxin/repository/chatglm2-6b",
        "api_base_url": "http://127.0.0.1:8888/v1",  # URL需要与运行fastchat服务端的server_config.FSCHAT_OPENAI_API一致
        "api_key": "EMPTY"
    },

    "chatglm2-6b-32k": {
        # "local_model_path": "THUDM/chatglm2-6b-32k",
        "local_model_path": "/data/hujiaxin/repository/chatglm2-6b-32k",
        "api_base_url": "http://127.0.0.1:8888/v1",  # "URL需要与运行fastchat服务端的server_config.FSCHAT_OPENAI_API一致
        "api_key": "EMPTY"
    },

    "vicuna-13b-hf": {
        "local_model_path": "",
        "api_base_url": "http://localhost:8888/v1",  # "name"修改为fastchat服务中的"api_base_url"
        "api_key": "EMPTY"
    },

    # 调用chatgpt时如果报出： urllib3.exceptions.MaxRetryError: HTTPSConnectionPool(host='api.openai.com', port=443):
    #  Max retries exceeded with url: /v1/chat/completions
    # 则需要将urllib3版本修改为1.25.11
    # 如果依然报urllib3.exceptions.MaxRetryError: HTTPSConnectionPool，则将https改为http
    # 参考https://zhuanlan.zhihu.com/p/350015032

    # 如果报出：raise NewConnectionError(
    # urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPSConnection object at 0x000001FE4BDB85E0>:
    # Failed to establish a new connection: [WinError 10060]
    # 则是因为内地和香港的IP都被OPENAI封了，需要切换为日本、新加坡等地
    "gpt-3.5-turbo": {
        "local_model_path": "gpt-3.5-turbo",
        "api_base_url": "https://api.openai.com/v1",
        "api_key": os.environ.get("OPENAI_API_KEY")
    },
}


# LLM 名称
LLM_MODEL = "chatglm2-6b"

# LLM 运行设备
LLM_DEVICE = "cuda" if torch.cuda.is_available() else "mps" if torch.backends.mps.is_available() else "cpu"

# 日志存储路径
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)

# 知识库默认存储路径
KB_ROOT_PATH = os.path.join("/data", "knowledge_base")

# 数据库默认存储路径。
# 如果使用sqlite，可以直接修改DB_ROOT_PATH；如果使用其它数据库，请直接修改SQLALCHEMY_DATABASE_URI。
DB_ROOT_PATH = os.path.join(KB_ROOT_PATH, "info.db")
SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_ROOT_PATH}"

# 可选向量库类型及对应配置
kbs_config = {
    "faiss": {
    },
    "milvus": {
        "host": "127.0.0.1",
        "port": "19530",
        "user": "",
        "password": "",
        "secure": False,
    },
    "pg": {
        "connection_uri": "postgresql://postgres:postgres@127.0.0.1:5432/langchain_chatchat",
    }
}

# 默认向量库类型。可选：faiss, milvus, pg.
DEFAULT_VS_TYPE = "faiss"

# 缓存向量库数量
CACHED_VS_NUM = 1

# 知识库中单段文本长度
CHUNK_SIZE = 250

# 知识库中相邻文本重合长度
OVERLAP_SIZE = 50

# 知识库匹配向量数量
VECTOR_SEARCH_TOP_K = 5

# 知识库匹配相关度阈值，取值范围在0-1之间，SCORE越小，相关度越高，取到1相当于不筛选，建议设置在0.5左右
SCORE_THRESHOLD = 0.9

# 搜索引擎匹配结题数量
SEARCH_ENGINE_TOP_K = 5

# nltk 模型存储路径
NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

# 基于本地知识问答的提示词模版
PROMPT_TEMPLATE = """【指令】根据已知信息，简洁和专业的来回答问题。如果无法从中得到答案，请说 “根据已知信息无法回答该问题”，不允许在答案中添加编造成分，答案请使用中文。 

【已知信息】{context} 

【问题】{question}"""

# 基于本地知识库的重写提示词模版
REWRITE_PROMPT_TEMPLATE = """【指令】{query} 

【已知信息】{context} 

【问题】{topic}"""

# API 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = False

# Bing 搜索必备变量
# 使用 Bing 搜索需要使用 Bing Subscription Key,需要在azure port中申请试用bing search
# 具体申请方式请见
# https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/create-bing-search-service-resource
# 使用python创建bing api 搜索实例详见:
# https://learn.microsoft.com/en-us/bing/search-apis/bing-web-search/quickstarts/rest/python
BING_SEARCH_URL = "https://api.bing.microsoft.com/v7.0/search"
# 注意不是bing Webmaster Tools的api key，

# 此外，如果是在服务器上，报Failed to establish a new connection: [Errno 110] Connection timed out
# 是因为服务器加了防火墙，需要联系管理员加白名单，如果公司的服务器的话，就别想了GG
BING_SUBSCRIPTION_KEY = ""

# 是否开启中文标题加强，以及标题增强的相关配置
# 通过增加标题判断，判断哪些文本为标题，并在metadata中进行标记；
# 然后将文本与往上一级的标题进行拼合，实现文本信息的增强。
ZH_TITLE_ENHANCE = False