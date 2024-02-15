# 使用 hugo 基础镜像
FROM klakegg/hugo:latest

# 设置工作目录
WORKDIR /home/app

#RUN apk install git
RUN hugo new site /home/app

# 设置 CMD
CMD ["server"]
