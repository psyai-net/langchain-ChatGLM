FROM  nvidia/cuda:11.8.0-runtime-ubuntu20.04
LABEL MAINTAINER="chatGLM"

COPY . /chatGLM/

WORKDIR /chatGLM

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone
RUN apt-get update -y && apt-get install python3 python3-pip curl libgl1 libglib2.0-0 -y  && apt-get clean
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && python3 get-pip.py 

RUN pip3 install -r requirements_api.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
RUN pip3 install -r requirements_webui.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && rm -rf `pip3 cache dir`

CMD ["python3","startup.py", "--all-webui"]